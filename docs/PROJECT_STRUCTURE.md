# Project structure

ECLIPSE 2.0 is a small, local-first Tkinter desktop application.

- `eclipse/engine.py`: SQLite schema, progression rules, quest/goal/habit operations, backup and migration.
- `eclipse/brain.py`: read-only, explainable recommendations and unlock calculations.
- `eclipse/app.py`: Tkinter user interface.
- `tests/`: automated tests for the engine and System Brain.
- `docs/`: manual Windows test checklist, release notes, and architecture.
- `legacy/`: original single-file prototype, retained for reference.

The active database lives under the user's home directory in `.eclipse/`. No cloud services or external Python dependencies are used.
