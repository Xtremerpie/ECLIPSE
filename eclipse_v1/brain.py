"""Deterministic, local System Brain for ECLIPSE V1.1.

This module only reasons over records the player explicitly creates in ECLIPSE.
It does not monitor the device or infer activity outside the application.
"""
from __future__ import annotations

from collections import Counter
from typing import Any

from .engine import ATTRIBUTES, STORY


class SystemBrain:
    """Produces explainable insights, milestones, and story unlocks."""

    def __init__(self, engine):
        self.engine = engine

    def snapshot(self) -> dict[str, Any]:
        player = self.engine.player()
        events = self.engine.conn.execute(
            "SELECT kind, detail, created_at FROM events ORDER BY id"
        ).fetchall()
        counts = Counter(row["kind"] for row in events)
        quest_total = counts["quest_completed"]
        goal_total = counts["goal_completed"]
        attributes = player["attributes"]
        weakest = min(ATTRIBUTES, key=lambda name: (attributes.get(name, 1), name))
        strongest = max(ATTRIBUTES, key=lambda name: (attributes.get(name, 1), name))

        if quest_total == 0:
            recommendation = "Choose one small directive and complete it honestly. The System needs a first record before it can identify patterns."
        elif quest_total < 3:
            recommendation = "Build a little consistency. Complete a few different kinds of directives before drawing conclusions about your patterns."
        else:
            recommendation = (
                f"Your least-practised recorded attribute is {weakest}. "
                f"Consider one manageable activity in that area; your strongest recorded area is {strongest}."
            )

        achievements = [
            self._achievement("first_record", "First Signal", "Complete your first daily directive.", quest_total >= 1),
            self._achievement("three_records", "Signal Detected", "Complete three daily directives.", quest_total >= 3),
            self._achievement("ten_records", "Pattern Recognition", "Complete ten daily directives.", quest_total >= 10),
            self._achievement("first_goal", "A Chosen Destination", "Complete your first long-term objective.", goal_total >= 1),
            self._achievement("five_goals", "Milestone Maker", "Complete five long-term objectives.", goal_total >= 5),
        ]

        chapters = []
        for index, (title, body) in enumerate(STORY):
            required = (0, 1, 3, 8)[index] if index < 4 else index * 3
            chapters.append({
                "title": title,
                "body": body,
                "required_records": required,
                "unlocked": quest_total >= required,
            })

        unlocked_skills = []
        skill_rules = [
            ("Focused Initiate", "Focus", 3, "A first foundation in focused work."),
            ("Knowledge Seeker", "Knowledge", 3, "A first foundation in deliberate learning."),
            ("Creative Spark", "Creativity", 3, "A first foundation in making and improving."),
            ("Resilient Return", "Resilience", 3, "A first foundation in returning after setbacks."),
        ]
        for title, attribute, threshold, description in skill_rules:
            value = attributes.get(attribute, 1)
            unlocked_skills.append({
                "title": title, "attribute": attribute, "value": value,
                "description": description, "unlocked": value >= threshold,
            })

        return {
            "player": player,
            "quest_records": quest_total,
            "goal_records": goal_total,
            "event_count": len(events),
            "strongest_attribute": strongest,
            "weakest_attribute": weakest,
            "recommendation": recommendation,
            "achievements": achievements,
            "skills": unlocked_skills,
            "chapters": chapters,
        }

    @staticmethod
    def _achievement(key: str, title: str, description: str, unlocked: bool) -> dict[str, Any]:
        return {"key": key, "title": title, "description": description, "unlocked": unlocked}
