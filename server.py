import argparse
import json
import queue
import socket
import threading
from collections import deque
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent
APP_FILE = "spektral-krew-livestream_final.html"


class EventHub:
    def __init__(self):
        self._clients = set()
        self._chat_history = deque(maxlen=120)
        self._latest_state = None
        self._lock = threading.Lock()

    def subscribe(self):
        client = queue.Queue(maxsize=256)
        with self._lock:
            self._clients.add(client)
            initial_events = [
                {"type": "chat", "payload": message}
                for message in self._chat_history
            ]
            if self._latest_state is not None:
                initial_events.append({"type": "state", "payload": self._latest_state})
        return client, initial_events

    def unsubscribe(self, client):
        with self._lock:
            self._clients.discard(client)

    def publish(self, event):
        event_type = event.get("type")
        payload = event.get("payload")

        with self._lock:
            if event_type == "chat":
                self._chat_history.append(payload)
            elif event_type == "clear-chat":
                self._chat_history.clear()
            elif event_type == "state":
                self._latest_state = payload

            clients = list(self._clients)

        for client in clients:
            try:
                client.put_nowait(event)
            except queue.Full:
                self.unsubscribe(client)


EVENTS = EventHub()


class AppHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        path = urlsplit(self.path).path
        if path == "/display":
            self.send_response(302)
            self.send_header("Location", "/?display=1")
            self.end_headers()
            return
        if path == "/events":
            self.stream_events()
            return
        if path in {"/", "/index.html"}:
            self.path = f"/{APP_FILE}"
        super().do_GET()

    def do_POST(self):
        if urlsplit(self.path).path != "/broadcast":
            self.send_error(404)
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_error(400, "Invalid Content-Length")
            return

        if length <= 0 or length > 4 * 1024 * 1024:
            self.send_error(400, "Invalid event size")
            return

        try:
            event = json.loads(self.rfile.read(length))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self.send_error(400, "Invalid JSON")
            return

        if not isinstance(event, dict) or not isinstance(event.get("type"), str):
            self.send_error(400, "Invalid event")
            return

        EVENTS.publish(event)
        self.send_response(204)
        self.end_headers()

    def stream_events(self):
        client, initial_events = EVENTS.subscribe()
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()

        try:
            for event in initial_events:
                self.write_event(event)

            while True:
                try:
                    event = client.get(timeout=15)
                    self.write_event(event)
                except queue.Empty:
                    self.wfile.write(b": keep-alive\n\n")
                    self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            EVENTS.unsubscribe(client)

    def write_event(self, event):
        data = json.dumps(event, separators=(",", ":")).encode("utf-8")
        self.wfile.write(b"data: " + data + b"\n\n")
        self.wfile.flush()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, format, *args):
        if self.path != "/broadcast":
            super().log_message(format, *args)


def get_lan_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("192.0.2.1", 80))
        return sock.getsockname()[0]
    except OSError:
        return None
    finally:
        sock.close()


def main():
    parser = argparse.ArgumentParser(description="Host Spektral Krew on the local network.")
    parser.add_argument("--port", type=int, default=8000, help="Port to use (default: 8000)")
    args = parser.parse_args()

    if not (ROOT / APP_FILE).is_file():
        raise SystemExit(f"Cannot find {APP_FILE} next to server.py")

    server = ThreadingHTTPServer(("0.0.0.0", args.port), AppHandler)
    lan_ip = get_lan_ip()

    print("Spektral Krew is available at:")
    print(f"  Main controls: http://localhost:{args.port}")
    if lan_ip:
        print(f"  Audience display: http://{lan_ip}:{args.port}/display")
    else:
        print(f"  Audience display: use http://<IPv4 address>:{args.port}/display")
        print("  Find the laptop's IPv4 address with ipconfig")
    print("Press Ctrl+C to stop the server.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
