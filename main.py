from pawpal_system import AppointmentTask, FeedingTask, MedicationTask, Owner, Pet, Scheduler


def render_schedule_dashboard(owner: Owner) -> None:
    """Render the owner's pet schedule as a markdown-style table."""
    scheduler = Scheduler(owner)
    schedule = scheduler.build_schedule()

    print("# PawPal+ Schedule Dashboard")
    print("")
    print("| Time | Pet | Task | Priority | Status |")
    print("| --- | --- | --- | --- | --- |")
    for task in schedule:
        pet_name = next(pet.name for pet in owner.pets if task in pet.tasks)
        status = "Completed" if task.is_completed else "Pending"
        print(f"| {task.due_time} | {pet_name} | {task.description} | {task.priority} | {status} |")


if __name__ == "__main__":
    owner = Owner(id="owner-1", name="Alex")
    luna = Pet(id="pet-1", name="Luna", species="Dog", age=4)
    maple = Pet(id="pet-2", name="Maple", species="Cat", age=2)

    owner.add_pet(luna)
    owner.add_pet(maple)

    luna.add_task(FeedingTask(id="task-1", description="Morning feeding", priority=1, due_time="08:00"))
    luna.add_task(MedicationTask(id="task-2", description="Daily vitamin", priority=3, due_time="09:30"))
    maple.add_task(AppointmentTask(id="task-3", description="Vet checkup", priority=2, due_time="11:00"))
    maple.add_task(FeedingTask(id="task-4", description="Evening feeding", priority=1, due_time="18:00"))

    render_schedule_dashboard(owner)
