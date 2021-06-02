import json
from abc import ABC, abstractmethod

class DisciplineWorkProgram():
    def __init__(
        self, id, name, author, competency,
        learning_outcomes=None, educational_program=None, scope=None, module=None, material=None
    ):
        self.id = id
        self.name = name
        self.author = author
        self.competency = competency
        self.learning_outcomes = learning_outcomes
        self.educational_program = educational_program
        self.discipline_scope = scope
        self.discipline_module = module
        self.discipline_material = material


class LearningOutcomes():
    def __init__(self, id, discipline_id, competency, formulation, results, methods):
        self.id = id
        self.discipline_id = discipline_id
        self.competency_code = competency
        self.formulation = formulation
        self.results = results
        self.forms_and_methods = methods


class EducationalProgram():
    def __init__(self, id, name):
        self.id = id
        self.name = name


class DisciplineScope():
    def __init__(
        self, id, discipline_id, sem_n, credit_units,
        total_h, lectures_h, seminars_h, laboratory_h, independent_h, certification_type
    ):
        self.id = id
        self.discipline_id = discipline_id
        self.semester_number = sem_n
        self.credit_units = credit_units
        self.total_hours = total_h
        self.lectures_hours = lectures_h
        self.seminars_hours = seminars_h
        self.laboratory_hour = laboratory_h
        self.independent_hours = independent_h
        self.certification_type = certification_type


class DisciplineModule():
    def __init__(
        self, id, discipline_id, name, sem_n, lectures_h, classroom_h,
        seminars_h, laboratory_h, independent_h, min_score, max_score, competency_code
    ):
        self.id = id
        self.discipline_id = discipline_id
        self.name = name
        self.sem_number = sem_n
        self.lectures_hours = lectures_h
        self.classroom_hours = classroom_h
        self.seminars_hours = seminars_h
        self.laboratory_hours = laboratory_h
        self.independent_hours = independent_h
        self.min_score = min_score
        self.max_score = max_score
        self.competency_code = competency_code


class DisciplineMaterial():
    def __init__(self, id, discipline_id, material):
        self.id = id
        self.discipline_id = discipline_id
        self.material = material
