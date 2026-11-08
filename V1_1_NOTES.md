# ECLIPSE V1.1 — System Intelligence

V1.1 builds on the V1 offline-first foundation.

## What's new

- **System Brain:** deterministic local analysis of recorded quests, completed goals, and attribute practice.
- **Actionable guidance:** the Brain suggests a manageable next step based on recorded activity. It does not claim to know what happens outside ECLIPSE.
- **Achievements:** first record, three records, ten records, first objective, and five objectives.
- **Skill evolution:** four starter skills unlock when their related attribute reaches three recorded practice points.
- **Story progression:** archive fragments unlock at 0, 1, 3, and 8 completed directives.
- **New UI tab:** System Brain shows the report, achievements, and skills.
- **No AI dependency:** no API keys, network calls, or paid model required.

## Run

Use the existing START_ECLIPSE_V1.bat launcher from the repository root, or run:

    py -3.14 -m eclipse_v1

Run the tests from the repository root:

    py -3.14 -m unittest discover -s tests -v

## Important

The Brain is read-only. It never awards XP, changes attributes, or completes quests. It only derives reports from the player's explicit local records. ECLIPSE does not monitor the desktop, read private messages, or inspect files.

The current V1.1 branch adds code but has not been runtime-tested on the user's PC. Run the test suite and app locally before treating it as verified.
