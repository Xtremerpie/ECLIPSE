# ECLIPSE 2.0 — The Complete System

**A lightweight, offline-first personal progression desktop app by Xtremerpie.**

ECLIPSE turns actions you choose to record into quests, XP, levels, attributes, goals, habits, achievements, skills, story unlocks, and a private activity history. It is a motivational tool—not a measure of your worth.

## Quick start (Windows)

1. Download this repository using **Code → Download ZIP**, then extract it.
2. Install Python 3.10+ with **Tkinter** enabled (Python 3.14 is supported).
3. Double-click **START_ECLIPSE.bat**.

Or open PowerShell in the extracted project folder:

```powershell
py -3.14 -m eclipse
```

No pip packages, API key, GPU, or internet connection are required. ECLIPSE uses Python's standard library.

## Features

- **Dashboard:** player profile, level, XP, rank, coins, eight attributes, and activity overview.
- **Quests:** five daily directives, custom quests, attribute progression, and one-time rewards.
- **Goals:** add, complete, and remove long-term objectives.
- **Habits:** daily check-ins, archive support, and no missed-day penalties.
- **Focus Room:** 5, 15, 25, 45, and 60-minute timer with start, pause, and reset.
- **System Brain:** explainable recommendations based only on records you enter.
- **Growth:** achievements, starter skills, attribute statistics, and progression milestones.
- **Story Archive:** five original chapters unlocked through recorded progress.
- **Journal and History:** private daily reflections and a timeline of recorded actions.
- **Settings:** rename player, six local system checks, open data folder, SQLite backup, portable JSON export, and confirmed restore.

## Your data

The app stores its active database locally at:

`%USERPROFILE%\.eclipse\eclipse_v2.db`

If an older `eclipse_v1.db` is present in the project folder, ECLIPSE can import compatible records once without modifying that source database. The legacy `eclipse_save.json` file is also read-only during import. Keep backups before changing or moving old project data.

## Run automated tests

```powershell
py -3.14 -m unittest discover -s tests -v
```

Then complete the [Windows test checklist](docs/TESTING.md).

## Project layout

- `eclipse/` — application, progression engine, and local System Brain.
- `tests/` — automated engine and System Brain tests.
- `docs/` — Windows test checklist, release notes, and architecture.
- `legacy/` — archived original single-file prototype.
- `START_ECLIPSE.bat` — Windows launcher.

## Privacy and limitations

- No cloud account, network calls, screen surveillance, keylogging, or private-message reading.
- No automatic device control or covert verification of activities.
- XP is awarded only after an explicit action inside ECLIPSE.
- The focus timer measures elapsed time; it cannot verify what happened during a session.
- Rafail AI is not required for ECLIPSE 2.0 and is not integrated in this release.

**Target:** lightweight Windows desktop. Automated tests do not replace the manual Windows GUI checklist on your own PC.
