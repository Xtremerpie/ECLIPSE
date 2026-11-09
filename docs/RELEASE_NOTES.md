# ECLIPSE 2.0 release notes

V2.0 consolidates the V1/V1.1 foundation into a complete local desktop experience.

### Included
- Dashboard and player profile controls.
- Daily and custom quests, explicit one-time rewards, and removal of unfinished directives.
- Long-term objectives with create/complete/remove operations.
- Habit tracking with one check-in per day and archive support.
- Focus timer with 5, 15, 25, 45, and 60-minute sessions.
- System Brain, attribute overview, achievements, starter skills, and five original story chapters.
- Daily journal, event history, local diagnostics, SQLite backup, portable JSON export, and confirmed JSON restore.
- One-time migration from compatible V1 SQLite data; original database remains unchanged.

### Verification
- Engine tests cover quests, goals, habits, journal persistence, export/restore, SQLite backup, legacy import, and V1 migration.
- CI workflow checks Python 3.12 and 3.14 on Windows and Ubuntu.
- Interactive Windows GUI behavior must still be smoke-tested on the target PC.
- No cloud services or third-party Python packages are required.
