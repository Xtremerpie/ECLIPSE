# ECLIPSE 2.0 — The Complete System

ECLIPSE is a lightweight, desktop-first, offline-first personal progression app. It turns actions you deliberately record into quests, XP, levels, attributes, milestones, skills, story unlocks, and a private history. It is a motivational tool—not a measure of your worth.

## Run on Windows

1. Download the repository ZIP from the eclipse-v2-complete-desktop branch and extract it.
2. Install Python 3.10+ with Tkinter. Python 3.14 is supported.
3. Double-click START_ECLIPSE_V2.bat.
4. Or run in PowerShell from the extracted folder:

   py -3.14 -m eclipse_v1

No pip installation is required. ECLIPSE uses Python's standard library only.

## V2.0 features

- Dashboard: player profile, level progress, XP, rank, coins, eight attributes, activity summary.
- Daily quest board: five rotating directives, one-time rewards, custom quests with selected attribute and bounded XP.
- Objectives: create, complete, and remove active long-term goals.
- Habit tracker: daily check-ins, once per day, archive support, no missed-day penalties.
- Focus Room: 5/15/25/45/60-minute local timer with start, pause, and reset.
- System Brain: explainable recommendations based only on records inside ECLIPSE.
- Growth: achievements, starter skills, attribute progression, and statistics.
- Original story archive: five chapters unlock through completed directives.
- Daily journal and event history.
- Settings: rename player, run six local health checks, open data folder, SQLite backup, portable JSON export, and confirmed JSON restore.
- One-time compatible migration from V1 SQLite data. The old database and eclipse_save.json are not overwritten.

## Data location

V2 data is stored in %USERPROFILE%\.eclipse\ as eclipse_v2.db. If eclipse_v1.db exists in the repository folder, compatible profile, attribute, quest, goal, and event records are copied once. The original V1 file remains unchanged.

Use Settings → Back Up Database for SQLite backup or Export Portable JSON for a portable backup. Restore replaces current records only after confirmation and creates a safety database backup first.

## Tests

Run from the repository root:

    py -3.14 -m unittest discover -s tests -v

Then follow TEST_CHECKLIST_V2.md. Settings → Run System Check validates the database, profile, quest board, XP progression, backup capability, and SQLite integrity.

## Privacy and design

- Local SQLite storage; no account, API key, network call, or cloud sync.
- No screen surveillance, keylogging, private-message reading, or automatic device control.
- XP is awarded only for explicit quest, goal, or habit check-in actions.
- The focus timer cannot verify what happened during a session.
- The local Brain analyses only records entered by the user.
- Rafail AI is not required to run V2.0; optional integration can be added later behind clear permissions.

## Hardware

Tkinter and SQLite; no GPU required. Designed to stay lightweight on a basic Windows PC. Actual performance and display behavior still need to be checked on the target PC.
