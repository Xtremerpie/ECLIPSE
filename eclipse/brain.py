"""Explainable, local System Intelligence for ECLIPSE."""
from collections import Counter
from .engine import ATTRIBUTES, STORY


class SystemBrain:
    """Read-only analysis of information explicitly recorded in ECLIPSE."""

    def __init__(self, engine):
        self.engine = engine

    def snapshot(self):
        p = self.engine.player()
        events = self.engine.conn.execute("SELECT kind FROM events").fetchall()
        counts = Counter(r["kind"] for r in events)
        attrs = p["attributes"]
        weakest = min(ATTRIBUTES, key=lambda n: (attrs.get(n, 1), n))
        strongest = max(ATTRIBUTES, key=lambda n: (attrs.get(n, 1), n))
        q = counts["quest_completed"]
        advice = (
            "Start with one small directive. The System needs a real record before it can identify patterns."
            if q == 0 else
            "Keep recording a few different kinds of activity before drawing conclusions."
            if q < 3 else
            f"Your most-practised recorded attribute is {strongest}. Consider a manageable activity in {weakest}."
        )
        achievements = [
            ("First Signal", "Complete your first directive.", q >= 1),
            ("Signal Detected", "Complete three directives.", q >= 3),
            ("Pattern Recognition", "Complete ten directives.", q >= 10),
            ("A Chosen Destination", "Complete an objective.", counts["goal_completed"] >= 1),
            ("Milestone Maker", "Complete five objectives.", counts["goal_completed"] >= 5),
            ("Daily Rhythm", "Complete ten habit check-ins.", counts["habit_completed"] >= 10),
        ]
        skills = [
            ("Focused Initiate", "Focus"), ("Knowledge Seeker", "Knowledge"),
            ("Creative Spark", "Creativity"), ("Resilient Return", "Resilience")
        ]
        chapters = []
        for i, (title, body) in enumerate(STORY):
            req = (0, 1, 3, 8, 15)[i]
            chapters.append({"title": title, "body": body, "required_records": req, "unlocked": q >= req})
        return {
            "player": p, "quest_records": q, "goal_records": counts["goal_completed"],
            "event_count": len(events), "strongest_attribute": strongest,
            "weakest_attribute": weakest, "recommendation": advice,
            "achievements": [{"title": a, "description": d, "unlocked": u} for a, d, u in achievements],
            "skills": [{"title": n, "attribute": a, "value": attrs.get(a, 1), "unlocked": attrs.get(a, 1) >= 3} for n, a in skills],
            "chapters": chapters
        }

    def daily_report(self, days=7, include_focus=True, include_habits=True, include_checkins=True, include_goals=True):
        d = self.engine.analytics_snapshot(days)
        pulse = self.engine.daily_checkin()
        habits = d["habit_count"] if include_habits else 0
        prev_habits = d["previous_habit_count"] if include_habits else 0
        focus = d["focus_minutes"] if include_focus else 0
        prev_focus = d["previous_focus_minutes"] if include_focus else 0
        goal_count = d["goal_count"] if include_goals else 0
        previous_goal_count = d["previous_goal_count"] if include_goals else 0
        checkin_count = d["checkin_count"] if include_checkins else 0
        lines = [
            f"ANALYSIS WINDOW  ·  LAST {d['days']} DAYS",
            f"{d['start']}  →  {d['end']}",
            "",
            "RECORDED ACTIVITY",
            f"Directives completed       {d['quest_count']}  (previous period: {d['previous_quest_count']})",
            f"Habit check-ins            {habits}  (previous period: {prev_habits})",
            f"Completed focus time       {focus} min  (previous period: {prev_focus} min)",
            f"Objectives completed       {goal_count}  (previous period: {previous_goal_count})",
            f"Daily pulses recorded      {checkin_count}",
            ""
        ]
        def trend(current, previous):
            delta = current - previous
            if delta > 0:
                return f"up by {delta} compared with the previous period"
            if delta < 0:
                return f"down by {abs(delta)} compared with the previous period"
            return "unchanged compared with the previous period"
        lines += [
            "PERIOD COMPARISON",
            f"Directive activity is {trend(d['quest_count'], d['previous_quest_count'])}.",
            f"Habit activity is {trend(habits, prev_habits)}.",
            f"Focus time is {trend(focus, prev_focus)}.",
            ""
        ]
        if include_checkins and d["checkin_count"]:
            lines.append(
                f"AVERAGE SELF-REPORTED PULSE  ·  Mood {d['avg_mood']}/5  ·  Energy {d['avg_energy']}/5  ·  Focus {d['avg_focus']}/5"
            )
        if include_checkins and pulse:
            lines += [
                "", "TODAY'S SELF-REPORTED PULSE",
                f"Mood {pulse['mood']}/5  ·  Energy {pulse['energy']}/5  ·  Focus {pulse['focus']}/5",
                f"Win: {pulse['win'] or 'Not recorded'}",
                f"Challenge: {pulse['challenge'] or 'Not recorded'}",
                f"Priority: {pulse['priority'] or 'Not recorded'}", ""
            ]
            if pulse["energy"] <= 2 or pulse["mood"] <= 2:
                lines.append("SYSTEM SUGGESTION: Consider a lighter plan and one manageable priority today.")
            elif pulse["focus"] >= 4 and pulse["energy"] >= 4:
                lines.append("SYSTEM SUGGESTION: Protect one focused block, then take a proper break.")
            else:
                lines.append("SYSTEM SUGGESTION: Choose one clear priority. A realistic plan beats an overloaded one.")
        elif include_checkins:
            lines.append("No daily pulse has been recorded today. The System will not guess how you feel.")
        else:
            lines.append("Daily pulse analysis is disabled in System Settings.")
        activity = self.engine.activity_by_day(min(days, 7))
        if activity:
            lines += ["", "RECENT DAILY ACTIVITY  ·  Q=directives  H=habits  F=focus minutes"]
            for item in activity:
                q = item["quests"]
                h = item["habits"] if include_habits else 0
                f = item["focus_minutes"] if include_focus else 0
                lines.append(f"{item['day']}   Q {q:>2}   H {h:>2}   F {f:>3}m")
        if d["quest_count"] == 0 and habits == 0 and focus == 0 and goal_count == 0:
            lines += ["", "SIGNAL STATUS: Not enough recent activity to identify a pattern. Start with one small action."]
        else:
            lines += ["", "SIGNAL STATUS: Records are available. Trends are descriptive, not a judgement or diagnosis."]
        lines += [
            "", "DATA BOUNDARY",
            "ECLIPSE uses only check-ins and actions recorded inside this app.",
            "It cannot verify offline work or know what you did in other applications.",
            "Journal contents are never included in this analysis."
        ]
        return "\n".join(lines)

    def full_report(self, include_focus=True, include_habits=True, days=7, include_checkins=True, include_goals=True):
        s = self.snapshot()
        attrs = s["player"]["attributes"]
        lines = [
            "ECLIPSE SYSTEM INTELLIGENCE", "=" * 36,
            self.daily_report(days, include_focus, include_habits, include_checkins, include_goals),
            "", "CHARACTER PROFILE",
            f"Player: {s['player']['name']}",
            f"Level {s['player']['level']} · Rank {s['player']['rank']} · {s['player']['xp']} total XP",
            f"Most practised recorded attribute: {s['strongest_attribute']}",
            f"Least practised recorded attribute: {s['weakest_attribute']}",
            "", "ATTRIBUTE MATRIX"
        ]
        lines += [f"{k}: {v}" for k, v in attrs.items()]
        lines += ["", "ACHIEVEMENTS"] + [
            f"{'UNLOCKED' if a['unlocked'] else 'LOCKED'} · {a['title']} — {a['description']}"
            for a in s["achievements"]
        ]
        lines += ["", "SKILL EVOLUTION"] + [
            f"{'UNLOCKED' if x['unlocked'] else 'LOCKED'} · {x['title']} ({x['attribute']} {x['value']}/3)"
            for x in s["skills"]
        ]
        lines += [
            "", "ANALYSIS OPTIONS",
            "Focus sessions: included" if include_focus else "Focus sessions: excluded",
            "Habit check-ins: included" if include_habits else "Habit check-ins: excluded",
            "Journal contents: always private and excluded"
        ]
        return "\n".join(lines)
