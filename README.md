# ECLIPSE 3.0 — Personal Progression System

**A polished, offline-first Windows desktop progression system by Xtremerpie.**

ECLIPSE combines a Solo-Leveling-inspired progression interface with daily reflection and explainable personal analytics. It records only what you choose to do inside the app.

## What's new in 3.0
- Redesigned command-center UI with navigation sidebar, dashboard cards, progress display, and custom ECLIPSE mark.
- Daily pulse check-in on launch (once per day, optional): mood, energy, focus, a small win, a challenge, and today's priority.
- Daily intelligence report based on check-ins and in-app activity.
- 7, 14, or 30-day analysis windows.
- Focus sessions recorded when the timer completes.
- Optional Windows sign-in startup setting.
- Settings for automatic check-ins and analysis inputs.
- Existing V2 data is preserved; new database tables are added automatically.

## Features
- Dashboard, directives, objectives, habits, focus room, System Intelligence, story archive, journal, activity log, and settings.
- XP, levels, ranks, coins, eight attributes, achievements, and skills.
- Local SQLite storage, backups, portable JSON export/restore, and diagnostics.

## Quick start on Windows
1. Download this repository using Code → Download ZIP and extract it.
2. Install Python 3.10+ with Tkinter enabled (Python 3.14 is supported).
3. Double-click START_ECLIPSE.bat.

PowerShell command from the extracted project folder: py -3.14 -m eclipse

No pip packages, API key, GPU, or internet connection are required.

## Daily analysis: what it can and cannot do
When ECLIPSE opens, it records an app-open event. If enabled, it asks for one short daily pulse. The System combines self-reported mood, energy and focus with completed directives, goals, habit check-ins, and completed focus timer sessions. It can identify simple trends and suggest a realistic next step.

It cannot know what you did outside the app, verify a goal, read other apps, monitor keystrokes, capture your screen, or infer your feelings. Goal completion remains an explicit confirmation. Journal text is always excluded from analysis.

## Windows sign-in startup
Open System Settings → Windows Startup and enable the option. ECLIPSE adds a launcher to your Windows Startup folder. Disable the same option to remove it. This currently supports Windows only.

## Data and privacy
The active database is stored at %USERPROFILE%\.eclipse\eclipse_v2.db.
ECLIPSE is local-first and does not require a cloud account or make network requests.

## Tests
Run: py -3.14 -m unittest discover -s tests -v
Then complete the Windows GUI checklist in docs/TESTING.md.

## Project layout
- eclipse/ — application, progression engine, and System Brain.
- tests/ — automated engine and Brain tests.
- docs/ — testing, release notes, and architecture.
- assets/ — ECLIPSE vector logo.
- legacy/ — archived original prototype.
- START_ECLIPSE.bat — Windows launcher.
