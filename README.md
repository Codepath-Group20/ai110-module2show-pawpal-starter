# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```
⚠️ Schedule Health Warnings
Potential scheduling conflicts detected:

⚠️
Conflict: Mini, Wanda all have tasks at 04:30 PM

Chronological Schedule Processed Successfully!

Tasks are displayed in strict chronological order using the scheduler's built-in ordering.

📋 Master Schedule Rows
⏱️ 2027-07-01 :07:00 | 🐾 Mini | 📝 Scolding | 🔴 Priority: 3 | ⏳ Pending

⏱️ 04:30 PM 🔄 | 🐾 Mini | 📝 Beating | 🔴 Priority: 2 | ⏳ Pending

⏱️ 04:30 PM 🔄 | 🐾 Wanda | 📝 Airing | 🔴 Priority: 4 | ⏳ Pending

⚠️ Critical: You have high-priority tasks scheduled.

Wanda: Airing — 04:30 PM
Next up: Mini — Scolding at 2027-07-01 :07:00

Pet Breakdown:

Mini: 2 tasks; next at 2027-07-01 :07:00 — Scolding
Wanda: 1 task; next at 04:30 PM — Airing

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
# pytest
python -m pytest -v

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```
============================= test session starts ==============================
platform linux -- Python 3.11.13, pytest-9.1.1, pluggy-1.6.0
collected 5 items                                                              

tests/test_pawpal.py::test_task_completion_updates_status PASSED         [ 20%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 40%]
tests/test_pawpal.py::test_recurring_daily_task_creates_new_incomplete_copy PASSED [ 60%]
tests/test_pawpal.py::test_scheduler_detects_conflicts_and_filters_tasks PASSED [ 80%]
tests/test_pawpal.py::test_sorting_correctness PASSED                    [100%]

============================== 5 passed in 0.19s ===============================

(venv) [leo@precision ai110-module2show-pawpal-starter]$ python -m pytest --cov=pawpal_system -v
==================================================================================== test session starts =====================================================================================
platform linux -- Python 3.11.13, pytest-9.1.1, pluggy-1.6.0 -- /home/leo/Classes/summer_2026/CodePath_A110/ai110-module2show-pawpal-starter/venv/bin/python
cachedir: .pytest_cache
rootdir: /home/leo/Classes/summer_2026/CodePath_A110/ai110-module2show-pawpal-starter
plugins: anyio-4.14.1, cov-7.1.0
collected 5 items                                                                                                                                                                            

tests/test_pawpal.py::test_task_completion_updates_status PASSED                                                                                                                       [ 20%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED                                                                                                                    [ 40%]
tests/test_pawpal.py::test_recurring_daily_task_creates_new_incomplete_copy PASSED                                                                                                     [ 60%]
tests/test_pawpal.py::test_scheduler_detects_conflicts_and_filters_tasks PASSED                                                                                                        [ 80%]
tests/test_pawpal.py::test_sorting_correctness PASSED                                                                                                                                  [100%]

======================================================================================= tests coverage =======================================================================================
______________________________________________________________________ coverage: platform linux, python 3.11.13-final-0 ______________________________________________________________________

Name               Stmts   Miss  Cover
--------------------------------------
pawpal_system.py      95      6    94%
--------------------------------------
TOTAL                 95      6    94%
===================================================================================== 5 passed in 0.22s ======================================================================================

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_tasks() | Sorts tasks chronologically, then breaks ties using priority levels. |
| Filtering | Scheduler.filter_schedule() | Skips or flags tasks if the owner's available time limit for the day is exceeded. |
| Conflict handling | Scheduler.detect_conflicts() | Detects if multiple tasks or pets overlap at the exact same time slot and flags a health warning. |
| Recurring tasks | Task.create_recurring() or Pet.handle_recurring() |	Automatically generates a new, incomplete copy of a daily care task once the current one is marked done. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
Enter Owner & Pet Profiles: Start by entering your basic owner information and adding your pets (like Mini or Wanda) to the system sidebar or input forms.

2. <!-- Describe this step -->
Input and Configure Tasks: Add care tasks for each pet by specifying the task name (e.g., "Scolding", "Airing", or "Beating"), setting the priority level, and choosing a specific time slot.

3. <!-- Describe this step -->
Generate and View Chronological Schedule: Review the master schedule rows, where the app automatically sorts and displays all pending tasks in strict chronological order using the built-in scheduling engine.

4. <!-- Describe this step -->
Check Schedule Health Warnings: Scan the top of the dashboard for any potential scheduling conflicts (such as multiple pets having tasks scheduled at the exact same time, like 04:30 PM) so you can adjust your plans.

5. <!-- Add more steps as needed -->
Review the Pet Care Breakdown: Check the critical task summary and the pet-by-pet breakdown at the bottom to see exactly how many tasks are remaining for each pet and what needs to be done next.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
https://github.com/Codepath-Group20/ai110-module2show-pawpal-starter/blob/main/Peek-streamlit-UI.gif

https://github.com/Codepath-Group20/ai110-module2show-pawpal-starter/blob/main/Peek_UI.gif

https://github.com/Codepath-Group20/ai110-module2show-pawpal-starter/blob/main/Peek_streaklit.gif
