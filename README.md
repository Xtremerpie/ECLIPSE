# ECLIPSE 3.1 — Personal Progression System

**A polished, offline-first Windows desktop progression system by Xtremerpie.**

ECLIPSE is a private, local-first command centre inspired by RPG progression systems. It combines real-world directives, objectives, habits, focus sessions, daily reflection, and transparent analysis.

## Complete feature set

### Command-centre interface
- Custom ECLIPSE app mark and dark command-centre theme.
- Persistent navigation rail and scrollable screens for smaller displays.
- Dashboard with level/XP progress, rank, activity metrics, and live attribute matrix.
- Dedicated pages for directives, objectives, habits, focus, System Intelligence, story archive, journal, activity history, and settings.

### Progression
- XP, levels, ranks, coins, and eight practice attributes.
- Daily generated directives plus custom directives.
- Long-range objectives with explicit manual completion confirmation.
- Daily habit check-ins with no streak punishment.
- Achievements, skill unlocks, and original story archive.
- Rewards are granted once per accepted completion.

### Daily System Intelligence
- Optional daily pulse when ECLIPSE launches (once per date, including when skipped).
- Self-reported mood, energy, focus, a win, a challenge, and one priority.
- 7, 14, or 30-day analysis window.
- Comparison with the previous equal-length period.
- Daily activity timeline, average pulse scores, and practical suggestions.
- Separate settings to include/exclude focus, habits, daily pulse, and objectives.
- Journal text is never included in analysis.

### Focus and desktop integration
- 5, 15, 25, 45, and 60-minute focus timer.
- Completed sessions are recorded; interrupted sessions of at least one minute are recorded as stopped.
- Optional Windows sign-in startup through the current user's Startup folder.
- Custom app icon and local status/diagnostics.

### Data protection
- Local SQLite database, automatic V2 database migration, legacy save import.
- SQLite backup and portable JSON export/restore.
- JSON format 3 export with format 2 import compatibility.
- Restore creates a safety database backup first.

## Run on Windows
1. Download the repository using Code → Download ZIP and extract it.
2. Install Python 3.10+ with Tkinter enabled (Python 3.14 is supported).
3. Double-click START_ECLIPSE.bat.

Or run py -3.14 -m eclipse from PowerShell in the extracted folder.

No pip packages, API key, GPU, or internet connection are required.

## Windows sign-in startup
Open System Settings → Windows Startup and enable **Start ECLIPSE when I sign in**. The app creates a launcher in your current user's Startup folder. Disable the option to remove it. This feature is Windows-only.

## Daily analysis and privacy boundaries
When ECLIPSE starts, it records an app-open event. If enabled, it asks for one daily pulse. If you skip, it will not repeatedly interrupt you that day. The System analyses only information you explicitly record in ECLIPSE.

It cannot verify offline work, read other apps, monitor keystrokes, capture your screen, or infer your feelings. Objectives are never auto-completed. Journal contents remain private and excluded.

## Data location
%USERPROFILE%\.eclipse\eclipse_v2.db

## Tests
Run py -3.14 -m unittest discover -s tests -v, then follow docs/TESTING.md for the local Windows GUI smoke test.

## Project layout
- eclipse/ — UI, progression engine, and System Brain.
- tests/ — automated engine and Brain tests.
- docs/ — testing, release notes, and architecture.
- assets/ — ECLIPSE vector identity mark.
- legacy/ — archived original prototype.
- START_ECLIPSE.bat — Windows launcher.
