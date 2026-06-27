from pawpal_system import Pet, Task


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
