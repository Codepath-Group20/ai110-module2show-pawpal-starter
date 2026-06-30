from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_updates_status() -> None:
    task = Task(id="task-1", description="Feed pet", priority=1, due_time="08:00")

    task.mark_complete()

    assert task.is_completed is True


def test_add_task_increases_pet_task_count() -> None:
    pet = Pet(id="pet-1", name="Milo", species="Dog", age=3)
    task = Task(id="task-2", description="Walk pet", priority=2, due_time="19:00")

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task


def test_recurring_daily_task_creates_new_incomplete_copy() -> None:
    pet = Pet(id="pet-2", name="Milo", species="Dog", age=3)
    task = Task(
        id="task-3",
        description="Feed pet",
        priority=3,
        due_time="2026-06-28 08:00",
        frequency="daily",
    )
    pet.add_task(task)

    task.mark_complete(pet=pet)

    assert task.is_completed is True
    assert len(pet.tasks) == 2
    assert pet.tasks[1].is_completed is False
    assert pet.tasks[1].due_time == "2026-06-29 08:00"


def test_scheduler_detects_conflicts_and_filters_tasks() -> None:
    owner = Owner(id="owner-1", name="Alex")
    mini = Pet(id="pet-3", name="Mini", species="Cat", age=2)
    max_pet = Pet(id="pet-4", name="Max", species="Dog", age=4)
    owner.add_pet(mini)
    owner.add_pet(max_pet)

    mini.add_task(Task(id="task-4", description="Feed Mini", priority=4, due_time="08:00"))
    max_pet.add_task(Task(id="task-5", description="Walk Max", priority=5, due_time="08:00"))

    scheduler = Scheduler(owner)

    conflicts = scheduler.detect_conflicts()
    filtered = scheduler.filter_tasks(pet_name="Mini", completion_status=False)

    assert conflicts
    assert any("Mini" in warning and "Max" in warning for warning in conflicts)
    assert len(filtered) == 1
    assert filtered[0].description == "Feed Mini"


def test_sorting_correctness() -> None:
    owner = Owner(id="owner-2", name="Taylor")
    pet = Pet(id="pet-5", name="Luna", species="Cat", age=5)
    owner.add_pet(pet)

    later_task = Task(id="task-6", description="Later task", priority=2, due_time="10:00")
    earlier_task = Task(id="task-7", description="Earlier task", priority=1, due_time="08:00")
    pet.add_task(later_task)
    pet.add_task(earlier_task)

    scheduler = Scheduler(owner)
    ordered_tasks = scheduler.build_schedule()

    assert ordered_tasks[0] is earlier_task
    assert ordered_tasks[1] is later_task
