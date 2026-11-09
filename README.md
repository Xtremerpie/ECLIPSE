# ECLIPSE 2.0 — The Complete System

A lightweight, offline-first desktop progression system by **Xtremerpie**.

## Run on Windows
1. Download and extract this branch.
2. Install Python 3.10+ with Tkinter.
3. Double-click **START_ECLIPSE_V2.bat**.
4. Or run: `py -3.14 -m eclipse_v1`

No pip packages, GPU, API key, or internet connection are required.

## Features
- Dashboard, player profile, levels, XP, ranks, coins, and eight attributes.
- Daily directives and custom quests with one-time rewards.
- Long-term objectives and habit check-ins.
- Focus timer, private daily journal, and event history.
- System Brain, achievements, starter skills, and five original story chapters.
- Settings, six local system checks, SQLite backup, portable JSON export, and restore.
- One-time compatible migration from the V1 SQLite database without modifying the original file.

## Data and privacy
V2 stores progress locally in `%USERPROFILE%\\.eclipse\\eclipse_v2.db`. No screen monitoring, keylogging, private-message reading, cloud account, or automatic device control. The Brain uses only records you enter.

## Documentation
- [Full V2 setup and feature guide](README_V2.md)
- [Windows feature test checklist](TEST_CHECKLIST_V2.md)
- [V2 release notes](V2_0_NOTES.md)

## Automated tests
`py -3.14 -m unittest discover -s tests -v`

The code and automated tests have been exercised in a development environment. Complete the Windows checklist on your PC before treating the desktop build as fully verified.
