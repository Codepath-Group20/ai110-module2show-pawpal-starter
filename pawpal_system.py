# existing content
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

@dataclass
class Task:
	id: str
	description: str
	priority: int
	due_time: str
	is_completed: bool = False

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
		pass

	def get_daily_agenda(self) -> List[Task]:
		"""Return incomplete tasks for the pet for the day.

		Implementation pending.
		"""
		return []

@dataclass
class Owner:
	id: str
	name: str
	pets: List[Pet] = field(default_factory=list)

	def add_pet(self, pet: Pet) -> None:
		pass

__all__ = [
	"Task",
	"FeedingTask",
	"MedicationTask",
	"AppointmentTask",
	"Pet",
	"Owner",
]
