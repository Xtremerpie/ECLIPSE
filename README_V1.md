# ECLIPSE V1 — The Awakening System

A desktop-first, offline-first personal progression system. ECLIPSE turns actions you choose to record into a clear history of progress. It is a motivational game layer, not a measure of your worth.

## Run on Windows

1. Install Python 3.10 or newer with Tkinter.
2. Double-click `START_ECLIPSE_V1.bat`, or run `py -3.14 -m eclipse_v1` from the repository folder.
3. Your V1 database is stored locally in `eclipse_v1.db`.

## V1 features

- Dark, lightweight Tkinter desktop interface.
- Player level, XP, rank, coins, and eight attributes.
- Daily quest board with deterministic daily rotation.
- One-time quest completion; refreshing the app cannot farm XP.
- Long-term objectives with explicit completion confirmation.
- Original story archive: The Unknown Existence.
- Local SQLite event memory.
- Safe, one-time import of compatible player name, XP, coins, and attributes from the older `eclipse_save.json`.
- No cloud account, background surveillance, private-message reading, or automatic actions.

## Design decisions

- **Hybrid personality:** mysterious System presentation with clear, supportive guidance.
- **Hybrid brain:** deterministic local engine is authoritative; an optional Rafail AI adapter is a future integration, never required to launch or use the app.
- **Desktop first:** UI is kept separate from the progression engine and SQLite repository so future clients can reuse the core.
- **Original story:** cosmic mystery and personal evolution, without copying characters, scenes, names, or dialogue from existing franchises.

## Fair progression rules

- XP is awarded only when a quest or objective is explicitly completed.
- Daily quest generation does not reset or reward completed quests again.
- Missed days do not remove XP or punish the player.
- Attributes represent recorded practice, not a judgment of a person's value.
- Goals are user-defined; no covert verification or surveillance is used.

## Data and backup

Keep `eclipse_v1.db` safe to preserve your V1 records. Close ECLIPSE before copying the database for backup. The legacy `eclipse_save.json` is read-only and is never overwritten by V1.

## Current limits

V1 is the foundation: it does not yet include an AI model connection, automatic project scanning, advanced skill trees, cloud sync, or a mobile client. Those belong in later, permission-based releases after the core is tested.
