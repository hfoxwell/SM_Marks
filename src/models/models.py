"""
    Author:     Hayden Foxwell
    Date:       16/08/2024
    Purpose:
        The data models which are responsible for storing the
        data returned from the SM Marks API.

    Change log:
        - [H Foxwell (16/08/24)] Currently all values are set to defaults
        - [H Foxwell (19/08/24)] Changed all classes to dataclasses
"""

# External Imports
from dataclasses import dataclass


# Classes
@dataclass
class MarkBook:
    """Represents a markbook"""

    key: str
    name: str
    owner: str
    year: str
    course: str


@dataclass
class User:
    """Represents a User such as a teacher"""

    key: str
    name: str
    login_id: str
    email: str


@dataclass
class Task:
    """Represents a single assessable task"""

    key: str
    name: str
    maximum: str
    decimal_places: int


@dataclass
class Student:
    """Represents a student in a markbook"""

    key: str
    student_ID: str
    family_name: str
    given_name: str
    preferred_name: str
    raw_results: list[str]
    rounded_results: list[str]


@dataclass
class Outcome:
    """Represents an assessable outcome"""

    key: str
    code: str
    name: str
    outcome: str
    task_list: list[Task]
