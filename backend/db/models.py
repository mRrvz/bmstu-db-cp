""" Database models """

class DisciplineWorkProgram():
    def __init__(
        self, id, name, author, competency, learning_outcomes=None,
        educational_program=None, scope=None, module=None, material=None
    ):
        if id is not None:
            self.id = int(id)
        else:
            self.id = None

        self.name = name
        self.author = author
        self.competency = competency
        self.learning_outcomes = learning_outcomes
        self.educational_program = educational_program
        self.discipline_scope_semester = scope
        self.discipline_module = module
        self.discipline_material = material

    def serialize(self):
        dictionary = {}
        for field in self.__dict__.keys():
            value = getattr(self, field)

            if type(value) == list:
                dictionary[field] = self.serialize_list_field(field)[0]
            else:
                dictionary[field] = value

        return dictionary

    def serialize_list_field(self, field):
        return None if getattr(self, field) is None else list(map(lambda x: x.serialize(), getattr(self, field))),


class LearningOutcomes():
    def __init__(self, id, discipline_id, competency, formulation, results, methods):
        if id is not None:
            self.id = int(id)
        else:
            self.id = None

        self.discipline_id = int(discipline_id)
        self.competency_code = competency
        self.formulation = formulation
        self.results = results
        self.forms_and_methods = methods

    def serialize(self):
        return self.__dict__


class EducationalProgram():
    def __init__(self, id, name):
        self.id = str(id)
        self.name = name

    def serialize(self):
        return self.__dict__


class DisciplineScope():
    def __init__(
        self, id, discipline_id, sem_n, credit_units,
        total_h, lectures_h, seminars_h, laboratory_h, independent_h, certification_type
    ):
        if id is not None:
            self.id = int(id)
        else:
            self.id = None

        self.discipline_id = int(discipline_id)
        self.semester_number = int(sem_n)
        self.credit_units = int(credit_units)
        self.total_hours = int(total_h)
        self.lectures_hours = int(lectures_h)
        self.seminars_hours = int(seminars_h)
        self.laboratory_hours = int(laboratory_h)
        self.independent_hours = int(independent_h)
        self.certification_type = certification_type

    def serialize(self):
        return self.__dict__


class DisciplineModule():
    def __init__(
        self, id, discipline_id, name, sem_n, lectures_h, seminars_h,
        laboratory_h, independent_h, min_score, max_score, competency_code
    ):
        if id is not None:
            self.id = int(id)
        else:
            self.id = None

        self.discipline_id = int(discipline_id)
        self.name = name
        self.semester_number = int(sem_n)
        self.lectures_hours = int(lectures_h)
        self.seminars_hours = int(seminars_h)
        self.laboratory_hours = int(laboratory_h)
        self.independent_hours = int(independent_h)
        self.min_score = int(min_score)
        self.max_score = int(max_score)
        self.competency_code = competency_code

    def serialize(self):
        return self.__dict__


class DisciplineMaterial():
    def __init__(self, id, discipline_id, material):
        if id is not None:
            self.id = int(id)
        else:
            self.id = None

        self.discipline_id = int(discipline_id)
        self.material = material

    def serialize(self):
        return self.__dict__


class User():
    def __init__(self, username, password, email, status):
        self.username = username
        self.password = password
        self.email = email
        self.status = status

    def serialize(self):
        return self.__dict__
