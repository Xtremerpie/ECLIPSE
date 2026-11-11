# ECLIPSE 3.1 test checklist

## First launch
- [ ] Start with START_ECLIPSE.bat.
- [ ] Confirm the app icon, navigation rail, scrollable dashboard, XP progress, and attribute matrix render.
- [ ] Confirm existing V2 profile, XP, goals, habits, and history remain available.
- [ ] If daily check-in is enabled, confirm the pulse opens once on a new date.
- [ ] Skip the pulse, close and reopen ECLIPSE; confirm it does not pop up again that day.
- [ ] Save a pulse and confirm it appears in the dashboard and System Intelligence.

## Progression
- [ ] Complete one directive and confirm XP/coins/attribute update once.
- [ ] Add an objective and confirm it stays active until manually confirmed.
- [ ] Confirm an objective only after completion; verify +30 XP once.
- [ ] Add a habit and record a daily check-in; confirm duplicate same-day check-in is blocked.
- [ ] Unlock an achievement and story fragment through recorded progress.

## Focus
- [ ] Run a timer to completion and confirm a completed focus record.
- [ ] Run a timer for at least one minute, pause, reset, and confirm a stopped record.
- [ ] Resume a paused timer and confirm the countdown continues.
- [ ] Complete a session, press Start again, and confirm a fresh full-duration session begins.

## Analysis and settings
- [ ] Change analysis window between 7, 14, and 30 days.
- [ ] Toggle daily check-in, focus, habits, pulse ratings, and objective analysis.
- [ ] Confirm the previous-period comparison and recent daily activity timeline update.
- [ ] Confirm journal text never appears in System Intelligence.
- [ ] On Windows, enable sign-in startup and verify ECLIPSE_STARTUP.vbs appears in the Startup folder.
- [ ] Disable sign-in startup and verify the launcher is removed.

## Data and diagnostics
- [ ] Run diagnostics and confirm all checks pass.
- [ ] Export JSON, then restore it after creating a safety backup.
- [ ] Confirm V2 JSON export import compatibility.
- [ ] Confirm the app works offline and does not inspect other apps, keyboard, or screen.
- [ ] Confirm the app remains responsive on the target low-spec PC.
