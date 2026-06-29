from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional


@dataclass
class Task:
    id: str
    description: str
    priority: int
    due_time: str
    is_completed: bool = False
    frequency: str = "none"

    def mark_complete(self, pet: Optional["Pet"] = None) -> None:
        """Mark the task as completed and optionally create a recurring copy."""
        self.is_completed = True

        if self.frequency == "daily" and pet is not None:
            try:
                current_due = datetime.strptime(self.due_time, "%Y-%m-%d %H:%M")
                next_due = current_due + timedelta(days=1)
                next_task = Task(
                    id=f"{self.id}_next",
                    description=self.description,
                    priority=self.priority,
                    due_time=next_due.strftime("%Y-%m-%d %H:%M"),
                    is_completed=False,
                    frequency=self.frequency,
                )
                pet.add_task(next_task)
            except ValueError:
                pass


@dataclass
class FeedingTask(Task):
    pass


@dataclass
class MedicationTask(Task):
    pass


@dataclass
class AppointmentTask(Task):
    pass


@dataclass
class Pet:
    id: str
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to the pet's task list."""
        self.tasks.append(task)

    def get_daily_agenda(self) -> List[Task]:
        """Return incomplete tasks for the pet."""
        return [task for task in self.tasks if not task.is_completed]


@dataclass
class Owner:
    id: str
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        self.pets.append(pet)


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for an owner."""
        self.owner = owner

    def _time_sort_key(self, due_time: str) -> tuple:
        """Convert a due-time string into a consistent sortable value."""
        for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %I:%M %p", "%H:%M", "%I:%M %p"):
            try:
                parsed = datetime.strptime(due_time, fmt)
                return (parsed.year, parsed.month, parsed.day, parsed.hour, parsed.minute)
            except ValueError:
                continue

        return (0, 0, 0, 0, 0, due_time)

    def get_all_tasks(self) -> List[Task]:
        """Collect all incomplete tasks from the owner's pets."""
        tasks: List[Task] = []
        for pet in self.owner.pets:
            tasks.extend(pet.get_daily_agenda())
        return tasks

    def filter_tasks(self, pet_name: Optional[str] = None, completion_status: Optional[bool] = None) -> List[Task]:
        """Filter the aggregate schedule by pet name and/or completion status."""
        tasks = self.get_all_tasks()

        if pet_name is not None:
            tasks = [task for task in tasks if any(pet.name == pet_name for pet in self.owner.pets if task in pet.tasks)]

        if completion_status is not None:
            tasks = [task for task in tasks if task.is_completed is completion_status]

        return tasks

    def detect_conflicts(self) -> List[str]:
        """Return friendly warning strings when two active tasks share the same due time."""
        conflicts: List[str] = []

        try:
            tasks = self.get_all_tasks()
            by_time: dict[str, List[Task]] = {}
            for task in tasks:
                by_time.setdefault(task.due_time, []).append(task)

            for due_time, task_group in by_time.items():
                if len(task_group) < 2:
                    continue

                pet_names = []
                for task in task_group:
                    pet_name = next((pet.name for pet in self.owner.pets if task in pet.tasks), "Unknown")
                    pet_names.append(pet_name)

                unique_pets = sorted(set(pet_names))
                if len(unique_pets) >= 2:
                    conflicts.append(f"⚠️ Conflict: {', '.join(unique_pets)} all have tasks at {due_time}")
        except Exception:
            return []

        return conflicts

    def build_schedule(self) -> List[Task]:
        """Build a chronological schedule sorted by due time."""
        return sorted(self.get_all_tasks(), key=lambda task: self._time_sort_key(task.due_time))


__all__ = [
    "Task",
    "FeedingTask",
    "MedicationTask",
    "AppointmentTask",
    "Pet",
    "Owner",
    "Scheduler",
]
