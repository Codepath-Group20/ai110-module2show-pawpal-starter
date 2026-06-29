from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Task:
    id: str
    description: str
    priority: int
    due_time: str
    is_completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.is_completed = True


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

    def _time_sort_key(self, due_time: str) -> tuple[int, int, int, str]:
        """Convert a due-time string into a sortable tuple."""
        for fmt in ("%H:%M", "%I:%M %p", "%Y-%m-%d %H:%M", "%Y-%m-%d %I:%M %p"):
            try:
                parsed = datetime.strptime(due_time, fmt)
                return (parsed.year, parsed.month, parsed.day, parsed.strftime("%H:%M"))
            except ValueError:
                continue
        return (0, 0, 0, due_time)

    def get_all_tasks(self) -> List[Task]:
        """Collect all incomplete tasks from the owner's pets."""
        tasks: List[Task] = []
        for pet in self.owner.pets:
            tasks.extend(pet.get_daily_agenda())
        return tasks

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
