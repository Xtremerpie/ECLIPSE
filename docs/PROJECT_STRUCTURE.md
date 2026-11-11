# Project structure — ECLIPSE 3.1

ECLIPSE 3.1 is a local-first Tkinter desktop application.

- eclipse/app.py: command-centre UI, scrollable navigation, app icon, daily pulse, focus timer, Windows startup, settings, backup and diagnostics.
- eclipse/engine.py: SQLite schema, progression rules, daily check-ins, focus records, period analytics, daily timeline, backup, import/export and migration.
- eclipse/brain.py: explainable daily reports, previous-period comparisons, attributes, achievements, skills and story unlocks.
- assets/eclipse-mark.svg: vector identity mark.
- tests/: automated engine and System Brain tests.
- docs/: testing, release notes and architecture.
- legacy/: archived original prototype.

The active database lives in the user's home directory under .eclipse/. No cloud services or external Python dependencies are used.
