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


@dataclass
class User:

    key: str
    name: str
    login_id: str
    email: str


@dataclass
class Task:

    key: str
    name: str
    maximum: str
    decimal_places: int


@dataclass
class Student:

    key: str
    student_ID: str
    family_name: str
    given_name: str
    preferred_name: str
    raw_results: list[str]
    rounded_results: list[str]


@dataclass
class Outcome:

    key: str
    code: str
    name: str
    outcome: str
    task_list: list[Task]


@dataclass
class MarkBook:

    key: str
    name: str
    owner: str
    year: str
    course: str
    tasks: list[Task]
    students: list[Student]
