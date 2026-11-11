# ECLIPSE 3.1 — Release notes

## Complete Personal Progression Command Centre

### Interface
- Dark command-centre layout with persistent navigation and scrollable pages.
- Generated app icon and custom ECLIPSE crescent mark.
- Dashboard progression, XP, rank, metrics, and eight live attribute bars.
- Dedicated screens for directives, objectives, habits, focus, intelligence, story, journal, history, and settings.

### Progression and focus
- Daily generated and custom directives with one-time rewards.
- Objectives remain active until the user manually confirms completion.
- Daily habit check-ins, achievements, skills, and original story unlocks.
- 5/15/25/45/60-minute focus timer.
- Completed focus sessions are recorded; interrupted sessions of at least one minute are stored as stopped.

### Daily System Intelligence
- Optional once-per-date launch pulse. Skipping does not cause repeat prompts that same day.
- Mood, energy and focus ratings, plus a win, challenge, and priority.
- 7/14/30-day analysis windows and comparison with the previous equal-length period.
- Recent daily activity timeline and average self-reported pulse ratings.
- Separate controls for including focus, habits, pulse ratings, and objective completions.
- Journal text is always excluded.

### Desktop and data
- Optional Windows sign-in startup through the current user's Startup folder.
- Local SQLite database and V2 migration.
- SQLite backups and portable JSON format 3 export.
- Format 2 JSON import compatibility; restore creates a safety database backup.
- No cloud account, API key, external Python packages, GPU, or network requirement.

### Boundaries
ECLIPSE analyses only actions and check-ins explicitly recorded inside the app. It does not monitor the screen, keyboard, other applications, browsing, or messages. It cannot verify offline work or infer feelings. Analysis is descriptive, not a diagnosis or judgement.
