# Spektral Krew — Livestream Simulator

A self-contained HTML tool for running **Viral** (the Call of Cthulhu scenario) with a live, reactive "streaming chat" as a prop at the table. No install, no server, no internet connection required — everything (emotes, sounds, images) is embedded directly in the file. Just open it in a browser.

## Quick start

1. Download `spektral-krew-livestream.html`.
2. Open it in Chrome (recommended — see the dual-screen note below).
3. You'll see a stream layout on the left/center (chat + a night-vision video panel) and a control panel on the right.

That's it for solo/single-screen use. For the intended table setup, see below.

## Recommended setup: TV + laptop controller

The tool is built to run as **two synced windows**:

1. Open the file normally — this is your **main window**. Drag it onto the TV and go fullscreen. This is what your players see: chat, video panel, donation banners, nothing else.
2. Click **"Pop Out Controller ⧉"** in the top-right corner. This opens a **second window** containing only the control panel — drag this to your own laptop screen.
3. Everything you do in the controller window (change location, change mood, trigger donations, glitch the signal, etc.) is sent live to the main window on the TV. The two windows sync over `BroadcastChannel`, so no internet is needed — they just need to be the same file open in the same browser.

If you only have one screen, you can also just use the single window and click **"Hide Controls ▸"** to collapse the sidebar before showing it to players, and un-hide it when you need to make changes.

## How the chat works

Chat is generated automatically and constantly adapts to two independent settings you control:

- **Location** (left panel) — sets the *baseline* chat: text pulled from a pool written specifically for wherever the investigators currently are (14 story locations, plus two special end-game states — see below). A few emotes get mixed in naturally.
- **Mood** (below it) — an optional *overlay* on top of the location chat. Pick a mood and a second, faster stream of reactions (mostly emotes, some text) layers on top — the busier chat gets, the more obviously something is happening.
  - **Normal** = no overlay, just the calm location chat.
  - **Hype, Cool, Panicked, Scared, Spotted Smth, Fighting, RIP, Sad** run at full speed.
  - Everything else (Hacking/Tech, Thinking, Weird, Tucking In Bed, Horny, Fake/CGI) runs a bit calmer — roughly 85% mood content / 15% location content.
  - **Boring** is deliberately slow and drains viewers the whole time it's active — good for genuinely dead moments.
  - **Fake/CGI** is chat accusing the crew of faking everything — useful when players start hamming it up.

Location and Mood are independent — pick a location once, then swap moods freely as the scene develops without losing your place in the story.

### Special Situations
Three dedicated one-click triggers below the mood grid:
- **🍋 Eat the Lemon** / **⚰️ Get in the Morgue** — chat aggressively pushing the investigators toward a specific dare, text-heavy so it reads clearly.
- **🎉 1M Subs (Crypt)** — the "we just went viral" moment. Snaps subscribers to exactly 1,000,000, fires the celebration banner, and switches chat to 100% pure hype (no location chatter at all) at max speed.

### The two special locations
- **Crypt: After the Collapse** — chat is restricted to just two "users": most comments fail with `ERROR 401`, and only `UltimaUnum` gets through occasionally, in Latin.
- **Catacombs (Feed Cut)** — a big red **CONNECTION LOST** banner covers the screen; the signal glitches briefly every 30–120 seconds, same as the Collapse state, but otherwise nothing else happens.

## Donations

- **Super Chat (manual)** — type a name/amount/message or use a preset (including the two Morgue dare presets) and hit **Trigger Donation**. This is the only kind that pops the big banner, plays a sound, and (for $100+) adds screen shake/particles. Dismiss early with the × on the banner or the button in the control panel.
- **Passive donations** — small ($1–10, more in Cool/Hype moods) donations fire automatically in the background, tied to viewer count and mood. These are silent and just appear as a normal line in chat — the spectacle is reserved for donations you trigger yourself.
- The **Donated** counter in the top bar tracks the running total of both kinds combined.

## Viewers & Subscribers

- Both numbers drift naturally over time rather than jumping around.
- **Viewers** ease toward an "attractor" value — each location has its own default, shown and editable live in the control panel. Mood affects the drift too (Hype/Cool/Fighting pull it up, Sad/RIP/Scared/Panicked/Boring pull it down).
- **Subscribers** never decrease — the attractor only ever ratchets upward, though the actual displayed number wobbles gently around it rather than sitting frozen. You can also type an exact subscriber count directly if you need to set a specific number.
- The little spinner arrows step Viewers by 100 and Subs by 1,000.

## Other controls

- **Signal Glitch** — a 3-second visual/audio glitch, plus chat spends the next 12 seconds reacting to it ("wait did anyone else's stream just glitch??").
- **Interrupt Stream / Back Online** — for when something happens you don't want the audience to see. Interrupt shows a red "Stream Interrupted" banner and pauses/clears chat; Back Online resumes normally, with ~8 seconds of confused "what just happened" reactions first.
- **Sound Effects On** — toggle if you'd rather run it silently.

## Notes

- The file is fully offline — safe to run with no wifi at the table.
- Works best in Chrome, especially for the two-window controller setup (the sync relies on `BroadcastChannel`, which is most reliable there).
- Everything resets if you reload the page — there's no save/load, so avoid refreshing mid-session.
