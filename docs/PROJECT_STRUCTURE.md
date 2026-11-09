# Project structure

ECLIPSE 3.0 is a local-first Tkinter desktop application.

- eclipse/app.py: redesigned command-center UI, daily pulse, focus timer, Windows startup, and settings.
- eclipse/engine.py: SQLite schema, progression rules, daily check-ins, focus sessions, analytics, backup and migration.
- eclipse/brain.py: explainable daily reports based on explicitly recorded information.
- tests/: automated engine and System Brain tests.
- assets/eclipse-mark.svg: vector identity mark.
- docs/: testing, release notes, and architecture.
- legacy/: original prototype.

The active database lives under the user's home directory in .eclipse/. No cloud services or external Python dependencies are used.
