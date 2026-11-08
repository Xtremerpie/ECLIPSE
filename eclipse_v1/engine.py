"""Offline-first progression engine for ECLIPSE V1.

Progress is awarded only for explicitly completed quests. Refreshing or
regenerating the daily board never grants XP.
"""
from __future__ import annotations

import json
import random
import sqlite3
from datetime import date, datetime
from pathlib import Path
from typing import Any

RANKS = [
    (1, "F"), (5, "E"), (10, "D"), (20, "C"),
    (35, "B"), (55, "A"), (80, "S"), (120, "SS"),
]
ATTRIBUTES = ("Knowledge", "Focus", "Discipline", "Creativity",
              "Courage", "Social", "Resilience", "Awareness")
QUEST_POOL = [
    ("Knowledge", "Study one topic with full attention", 20, "Knowledge"),
    ("Focus", "Complete one focused work session", 20, "Focus"),
    ("Discipline", "Organise one small part of your workspace", 15, "Discipline"),
    ("Creativity", "Build, sketch, or improve something", 25, "Creativity"),
    ("Courage", "Take one reasonable step you've been postponing", 20, "Courage"),
    ("Social", "Have one meaningful, respectful conversation", 15, "Social"),
    ("Resilience", "Return to a task after a setback", 20, "Resilience"),
    ("Awareness", "Reflect on what worked today", 15, "Awareness"),
]
STORY = [
    ("PROLOGUE · THE UNKNOWN", "A quiet signal appears in the noise. It does not command you. It offers a question: what will you choose to become?"),
    ("CHAPTER 01 · FIRST SYNCHRONIZATION", "The System learns your chosen goals. Every record is a fragment of a larger map. Nothing is unlocked by pretending; the world responds to real effort."),
    ("CHAPTER 02 · THE AWAKENING", "The first milestone is not power. It is awareness: seeing your actions clearly and choosing the next useful step."),
    ("CHAPTER 03 · THE ARCHIVE", "Across the hidden archive, small completed promises become a pattern. The origin of the signal remains unknown."),
]

class EclipseEngine:
    def __init__(self, db_path: str | Path = "eclipse_v1.db", legacy_path: str | Path = "eclipse_save.json"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._schema()
        self._seed()
        self._import_legacy(Path(legacy_path))

    def _schema(self) -> None:
        self.conn.executescript("""
        PRAGMA foreign_keys=ON;
        CREATE TABLE IF NOT EXISTS player (
            id INTEGER PRIMARY KEY CHECK(id=1), name TEXT NOT NULL DEFAULT 'Player',
            xp INTEGER NOT NULL DEFAULT 0, coins INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS attributes (
            name TEXT PRIMARY KEY, value INTEGER NOT NULL DEFAULT 1
        );
        CREATE TABLE IF NOT EXISTS quests (
            id INTEGER PRIMARY KEY AUTOINCREMENT, day TEXT NOT NULL,
            title TEXT NOT NULL, category TEXT NOT NULL, xp INTEGER NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0, completed_at TEXT,
            UNIQUE(day, title)
        );
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT NOT NULL,
            detail TEXT NOT NULL, created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL,
            completed INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL
        );
        """)
        self.conn.commit()

    def _seed(self) -> None:
        self.conn.execute("INSERT OR IGNORE INTO player(id, name, created_at) VALUES(1, 'Player', ?)",
                          (datetime.now().isoformat(timespec="seconds"),))
        for attr in ATTRIBUTES:
            self.conn.execute("INSERT OR IGNORE INTO attributes(name, value) VALUES(?, 1)", (attr,))
        self.conn.commit()
        self.ensure_daily_quests()

    def _import_legacy(self, path: Path) -> None:
        marker = self.conn.execute("SELECT 1 FROM events WHERE kind='legacy_import' LIMIT 1").fetchone()
        if marker or not path.exists():
            return
        try:
            data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
            xp = max(0, int(data.get("xp", 0)))
            coins = max(0, int(data.get("coins", 0)))
            name = str(data.get("name", "Player"))[:40]
            self.conn.execute("UPDATE player SET name=?, xp=?, coins=? WHERE id=1", (name, xp, coins))
            stats = data.get("stats", {})
            for key, value in stats.items():
                if key in ATTRIBUTES:
                    self.conn.execute("UPDATE attributes SET value=? WHERE name=?",
                                      (max(1, min(999, int(value))), key))
            self._event("legacy_import", "Imported compatible profile data from eclipse_save.json")
            self.conn.commit()
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            self._event("legacy_import_skipped", "Legacy save could not be safely imported")
            self.conn.commit()

    def _event(self, kind: str, detail: str) -> None:
        self.conn.execute("INSERT INTO events(kind, detail, created_at) VALUES(?,?,?)",
                          (kind, detail, datetime.now().isoformat(timespec="seconds")))

    def ensure_daily_quests(self) -> None:
        today = date.today().isoformat()
        count = self.conn.execute("SELECT COUNT(*) FROM quests WHERE day=?", (today,)).fetchone()[0]
        if count:
            return
        rng = random.Random(today)
        for title, category, xp, _attribute in rng.sample(QUEST_POOL, 5):
            self.conn.execute("INSERT OR IGNORE INTO quests(day,title,category,xp) VALUES(?,?,?,?)",
                              (today, title, category, xp))
        self.conn.commit()

    def player(self) -> dict[str, Any]:
        p = dict(self.conn.execute("SELECT * FROM player WHERE id=1").fetchone())
        level = 1
        xp_remaining = p["xp"]
        while xp_remaining >= level * 100:
            xp_remaining -= level * 100
            level += 1
        rank = "F"
        for threshold, label in RANKS:
            if level >= threshold:
                rank = label
        p.update(level=level, level_xp=xp_remaining, next_xp=level * 100, rank=rank)
        p["attributes"] = {r["name"]: r["value"] for r in self.conn.execute("SELECT * FROM attributes")}
        return p

    def quests(self) -> list[dict[str, Any]]:
        self.ensure_daily_quests()
        return [dict(r) for r in self.conn.execute(
            "SELECT * FROM quests WHERE day=? ORDER BY id", (date.today().isoformat(),))]

    def complete_quest(self, quest_id: int) -> bool:
        row = self.conn.execute("SELECT * FROM quests WHERE id=? AND day=?",
                                (quest_id, date.today().isoformat())).fetchone()
        if not row or row["completed"]:
            return False
        self.conn.execute("UPDATE quests SET completed=1, completed_at=? WHERE id=?",
                          (datetime.now().isoformat(timespec="seconds"), quest_id))
        self.conn.execute("UPDATE player SET xp=xp+?, coins=coins+5 WHERE id=1", (row["xp"],))
        self.conn.execute("UPDATE attributes SET value=value+1 WHERE name=?", (row["category"],))
        self._event("quest_completed", f'{row["title"]} (+{row["xp"]} XP)')
        self.conn.commit()
        return True

    def add_goal(self, title: str) -> None:
        title = title.strip()
        if title:
            self.conn.execute("INSERT INTO goals(title,created_at) VALUES(?,?)",
                              (title[:120], datetime.now().isoformat(timespec="seconds")))
            self.conn.commit()

    def goals(self) -> list[dict[str, Any]]:
        return [dict(r) for r in self.conn.execute("SELECT * FROM goals ORDER BY id DESC")]

    def complete_goal(self, goal_id: int) -> bool:
        cur = self.conn.execute("UPDATE goals SET completed=1 WHERE id=? AND completed=0", (goal_id,))
        if cur.rowcount:
            self.conn.execute("UPDATE player SET xp=xp+30, coins=coins+10 WHERE id=1")
            self._event("goal_completed", f"Goal #{goal_id} completed (+30 XP)")
            self.conn.commit()
            return True
        return False

    def recent_events(self, limit: int = 12) -> list[dict[str, Any]]:
        return [dict(r) for r in self.conn.execute(
            "SELECT * FROM events ORDER BY id DESC LIMIT ?", (limit,))]

    def close(self) -> None:
        self.conn.close()
