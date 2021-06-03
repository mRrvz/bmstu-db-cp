""" Tarantool repos """

import logging
from db.utils import Utils
from db.repos.abstract import AbstractRepo
import db.models as models

class DisciplineWorkProgramRepoTarantool(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "space_name": "discipline_work_program",
            "field_names": {"id": 1, "name": 2, "author": 3, "competency": 4}
        }

        self.space = connection.space(self._meta['space_name'])

    def save(self, model):
        if not isinstance(model, models.DisciplineWorkProgram):
            logging.error("Trying to save DisciplineWorkProgram object of invalid type")
            raise TypeError("Expected object is instance of DisciplineWorkProgram")

        print((model.id, model.name, model.author, model.competency))
        self.space.insert((model.id, model.name, model.author, model.competency))

    def get_by_id(self, model_id):
        obj = self.space.select(int(model_id))
        if len(obj) == 0:
            return None

        return models.DisciplineWorkProgram(*obj[0])

    def get_all(self):
        selected = self.space.select()
        if len(selected) == 0:
            return None

        objects = list()
        for obj in selected:
            objects.append(models.DisciplineWorkProgram(*obj))

        return objects

    def remove(self, id):
        return self.space.delete(int(id))[0]

    def edit(self, *args, **kwargs):
        obj_id = kwargs['id']
        updated_args = Utils.get_tarantool_update_args(kwargs['fields'], self._meta['field_names'])

        return self.space.update(obj_id, updated_args)[0]


class LearningOutcomesRepoTarantool(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "table_name": "learning_outcomes",
            "field_names": {
                "id": 1,
                "discipline_id": 2,
                "competency_code": 3,
                "formulation": 4,
                "results": 5,
                "forms_and_methods": 6,
            }
        }

    def save(self):
        raise NotImplementedError

    def get_by_id(self, model_id):
        return NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def remove(self, id):
        raise NotImplementedError

    def edit(self, *args, **kwargs):
        raise NotImplementedError


class EducationalProgramRepoTarantool(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "table_name": "educational_program",
            "field_names": {
                "id": 1,
                "name": 2
            }
        }

    def save(self):
        raise NotImplementedError

    def get_by_id(self, model_id):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def remove(self, id):
        raise NotImplementedError

    def edit(self, *args, **kwargs):
        raise NotImplementedError

class DisciplineScopeRepoTarantool(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "table_name": "discipline_scope_semester",
            "field_names": {
                "id": 1,
                "discipline_id": 2,
                "semester_number": 3,
                "credit_units": 4,
                "total_hours": 5,
                "lectures_hours": 6,
                "laboratory_work_hours": 7,
                "independent_work_hours": 8,
                "certification_type": 9
            }
        }

    def save(self):
        raise NotImplementedError

    def get_by_id(self, model_id):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def remove(self, id):
        raise NotImplementedError

    def edit(self, *args, **kwargs):
        raise NotImplementedError


class DisciplineModuleRepoTarantool(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "table_name": "discipline_module",
            "field_names": {
                "id": 1,
                "discipline_id": 2,
                "name": 3,
                "semester_number": 4,
                "lectures_hours": 5,
                "seminars_hours": 6,
                "laboratory_work_hours": 7,
                "independent_work_hours": 8,
                "min_scores": 9,
                "max_scores": 10,
                "competency_codes": 11
            }
        }

    def save(self):
        raise NotImplementedError

    def get_by_id(self, model_id):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def remove(self, id):
        raise NotImplementedError

    def edit(self, *args, **kwargs):
        raise NotImplementedError


class DisciplineMaterialRepoTarantool(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "table_name": "discipline_material",
            "field_names": {"id": 1, "discipline_id": 2, "materials": 3}
        }

    def save(self):
        raise NotImplementedError

    def get_by_id(self, model_id):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def remove(self, id):
        raise NotImplementedError

    def edit(self, *args, **kwargs):
        raise NotImplementedError
