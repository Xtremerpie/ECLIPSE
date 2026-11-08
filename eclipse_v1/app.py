"""Tkinter desktop interface for ECLIPSE V1.1."""
from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from .engine import EclipseEngine
from .brain import SystemBrain

BG = "#080d18"
PANEL = "#111b2d"
CYAN = "#55e6f2"
TEXT = "#e7f2ff"
MUTED = "#8da3b8"
GOLD = "#e9c46a"


class EclipseApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("ECLIPSE — The Awakening System")
        self.root.geometry("1060x720")
        self.root.minsize(780, 560)
        self.root.configure(bg=BG)
        self.engine = EclipseEngine()
        self.brain = SystemBrain(self.engine)
        self._style()
        self._layout()
        self.refresh()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def _style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=PANEL, fieldbackground=PANEL,
                        foreground=TEXT, rowheight=32, borderwidth=0)
        style.configure("Treeview.Heading", background="#1b2b42", foreground=CYAN,
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#244456")])

    def _layout(self):
        header = tk.Frame(self.root, bg=BG, padx=24, pady=16)
        header.pack(fill="x")
        tk.Label(header, text="E C L I P S E", bg=BG, fg=CYAN,
                 font=("Segoe UI", 23, "bold")).pack(anchor="w")
        tk.Label(header, text="THE AWAKENING SYSTEM  /  LOCAL INSTANCE  /  V1.1",
                 bg=BG, fg=MUTED, font=("Consolas", 9)).pack(anchor="w")
        self.status = tk.Frame(self.root, bg=PANEL, padx=18, pady=12)
        self.status.pack(fill="x", padx=24, pady=(0, 14))
        self.status_text = tk.Label(self.status, bg=PANEL, fg=TEXT,
                                    font=("Segoe UI", 11), justify="left")
        self.status_text.pack(anchor="w")
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", expand=True, padx=24, pady=(0, 14))
        self.quest_tab = tk.Frame(self.tabs, bg=BG)
        self.story_tab = tk.Frame(self.tabs, bg=BG)
        self.goals_tab = tk.Frame(self.tabs, bg=BG)
        self.archive_tab = tk.Frame(self.tabs, bg=BG)
        self.brain_tab = tk.Frame(self.tabs, bg=BG)
        self.tabs.add(self.quest_tab, text="QUEST BOARD")
        self.tabs.add(self.story_tab, text="STORY ARCHIVE")
        self.tabs.add(self.goals_tab, text="GOALS")
        self.tabs.add(self.archive_tab, text="MEMORY")
        self.tabs.add(self.brain_tab, text="SYSTEM BRAIN")
        self._build_quests()
        self._build_story()
        self._build_goals()
        self._build_archive()
        self._build_brain()
        tk.Label(self.root, text="YOUR CHOICES. YOUR PACE. YOUR PROGRESS.",
                 bg=BG, fg=MUTED, font=("Consolas", 9)).pack(pady=(0, 8))

    def _section(self, parent, heading):
        tk.Label(parent, text=heading, bg=BG, fg=CYAN,
                 font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=16, pady=14)

    def _build_quests(self):
        self._section(self.quest_tab, "TODAY'S DIRECTIVES")
        self.quest_tree = ttk.Treeview(self.quest_tab, columns=("type", "xp", "state"),
                                       show="headings", height=9)
        for col, label, width in (("type", "ATTRIBUTE", 180), ("xp", "REWARD", 100),
                                  ("state", "STATUS", 150)):
            self.quest_tree.heading(col, text=label)
            self.quest_tree.column(col, width=width, anchor="center")
        self.quest_tree.pack(fill="both", expand=True, padx=16, pady=8)
        tk.Button(self.quest_tab, text="COMPLETE SELECTED QUEST", command=self.complete_selected,
                  bg="#153b4b", fg=CYAN, activebackground="#24566a", relief="flat",
                  padx=16, pady=10).pack(anchor="e", padx=16, pady=12)

    def _build_story(self):
        self._section(self.story_tab, "THE UNKNOWN EXISTENCE")
        self.story_text = tk.Text(self.story_tab, bg=BG, fg=TEXT, insertbackground=TEXT,
                                  relief="flat", wrap="word", font=("Segoe UI", 10),
                                  padx=16, pady=8)
        self.story_text.pack(fill="both", expand=True, padx=8, pady=4)
        self.story_text.configure(state="disabled")

    def _build_goals(self):
        self._section(self.goals_tab, "LONG-TERM OBJECTIVES")
        self.goal_tree = ttk.Treeview(self.goals_tab, columns=("state",),
                                      show="tree headings", height=10)
        self.goal_tree.heading("#0", text="OBJECTIVE")
        self.goal_tree.heading("state", text="STATUS")
        self.goal_tree.column("state", width=140, anchor="center")
        self.goal_tree.pack(fill="both", expand=True, padx=16, pady=8)
        bar = tk.Frame(self.goals_tab, bg=BG)
        bar.pack(fill="x", padx=16, pady=12)
        tk.Button(bar, text="ADD OBJECTIVE", command=self.add_goal, bg="#153b4b",
                  fg=CYAN, relief="flat", padx=14, pady=9).pack(side="left")
        tk.Button(bar, text="MARK SELECTED COMPLETE", command=self.complete_goal,
                  bg="#263b30", fg="#a8edbd", relief="flat", padx=14, pady=9).pack(side="right")

    def _build_archive(self):
        self._section(self.archive_tab, "SYSTEM MEMORY · RECENT EVENTS")
        self.archive_text = tk.Text(self.archive_tab, bg=PANEL, fg=TEXT, insertbackground=TEXT,
                                    relief="flat", wrap="word", font=("Consolas", 10),
                                    padx=14, pady=12)
        self.archive_text.pack(fill="both", expand=True, padx=16, pady=8)
        self.archive_text.configure(state="disabled")

    def _build_brain(self):
        self._section(self.brain_tab, "LOCAL INTELLIGENCE REPORT")
        self.brain_text = tk.Text(self.brain_tab, bg=PANEL, fg=TEXT, insertbackground=TEXT,
                                  relief="flat", wrap="word", font=("Segoe UI", 10),
                                  padx=16, pady=14)
        self.brain_text.pack(fill="both", expand=True, padx=16, pady=8)
        self.brain_text.configure(state="disabled")

    @staticmethod
    def _set_text(widget, value):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", value)
        widget.configure(state="disabled")

    def refresh(self):
        report = self.brain.snapshot()
        p = report["player"]
        attrs = "  ·  ".join(f"{k[:3].upper()} {v}" for k, v in p["attributes"].items())
        self.status_text.configure(text=(
            f"PLAYER  {p['name']}     RANK  {p['rank']}     LEVEL  {p['level']}\n"
            f"XP  {p['level_xp']} / {p['next_xp']}     TOTAL XP  {p['xp']}     COINS  {p['coins']}\n"
            f"{attrs}"
        ))

        for item in self.quest_tree.get_children():
            self.quest_tree.delete(item)
        for q in self.engine.quests():
            state = "COMPLETED" if q["completed"] else "AVAILABLE"
            self.quest_tree.insert("", "end", iid=str(q["id"]),
                                   values=(q["category"], f"+{q['xp']} XP", state),
                                   tags=("done",) if q["completed"] else ())
        self.quest_tree.tag_configure("done", foreground=MUTED)

        for item in self.goal_tree.get_children():
            self.goal_tree.delete(item)
        for goal in self.engine.goals():
            self.goal_tree.insert("", "end", iid=str(goal["id"]), text=goal["title"],
                                  values=("COMPLETED" if goal["completed"] else "ACTIVE",))

        event_lines = [
            f"[{event['created_at']}] {event['kind'].upper()}\n  {event['detail']}\n"
            for event in self.engine.recent_events()
        ]
        self._set_text(self.archive_text, "\n".join(event_lines) if event_lines else
                       "No recorded events yet. Your journey begins with your first completed action.")

        story_lines = []
        for chapter in report["chapters"]:
            state = "UNLOCKED" if chapter["unlocked"] else (
                f"LOCKED · requires {chapter['required_records']} completed directives"
            )
            story_lines.append(f"{chapter['title']}  [{state}]")
            story_lines.append(chapter["body"] if chapter["unlocked"] else
                               "The archive has not yet released this fragment.")
            story_lines.append("")
        self._set_text(self.story_text, "\n".join(story_lines))

        achievements = "\n".join(
            f"{'[UNLOCKED]' if a['unlocked'] else '[LOCKED]'}  {a['title']} — {a['description']}"
            for a in report["achievements"]
        )
        skills = "\n".join(
            f"{'[UNLOCKED]' if s['unlocked'] else '[LOCKED]'}  {s['title']} "
            f"({s['attribute']}: {s['value']}/3) — {s['description']}"
            for s in report["skills"]
        )
        brain_report = (
            "SYSTEM STATUS: ONLINE · LOCAL MODE\n"
            "INTELLIGENCE SOURCE: EXPLICIT ECLIPSE RECORDS ONLY\n\n"
            f"RECORDED DIRECTIVES: {report['quest_records']}\n"
            f"COMPLETED OBJECTIVES: {report['goal_records']}\n"
            f"ARCHIVED EVENTS: {report['event_count']}\n"
            f"STRONGEST RECORDED ATTRIBUTE: {report['strongest_attribute']}\n"
            f"LEAST PRACTISED RECORDED ATTRIBUTE: {report['weakest_attribute']}\n\n"
            "SYSTEM GUIDANCE\n"
            f"{report['recommendation']}\n\n"
            "ACHIEVEMENTS\n{achievements}\n\n"
            "SKILL EVOLUTION\n{skills}\n\n"
            "The Brain is read-only: it analyses your saved records and never awards XP by itself."
        ).format(achievements=achievements, skills=skills)
        self._set_text(self.brain_text, brain_report)

    def complete_selected(self):
        selected = self.quest_tree.selection()
        if not selected:
            messagebox.showinfo("ECLIPSE", "Select a quest first.")
            return
        if self.engine.complete_quest(int(selected[0])):
            self.refresh()
            messagebox.showinfo("SYSTEM", "Record accepted. Progress updated.")
        else:
            messagebox.showinfo("SYSTEM", "This directive is already completed or no longer available.")

    def add_goal(self):
        title = simpledialog.askstring("New objective",
            "What meaningful objective do you want to work toward?", parent=self.root)
        if title and title.strip():
            self.engine.add_goal(title)
            self.refresh()

    def complete_goal(self):
        selected = self.goal_tree.selection()
        if not selected:
            messagebox.showinfo("ECLIPSE", "Select an objective first.")
            return
        if messagebox.askyesno("Confirm milestone", "Have you genuinely completed this objective?"):
            if self.engine.complete_goal(int(selected[0])):
                self.refresh()
                messagebox.showinfo("SYSTEM", "Milestone recorded. +30 XP")
            else:
                messagebox.showinfo("SYSTEM", "This objective is already complete.")

    def close(self):
        self.engine.close()
        self.root.destroy()


def main():
    root = tk.Tk()
    EclipseApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
