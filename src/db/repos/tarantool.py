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

        self.space.insert((model.id, model.name, model.author, model.competency))

    def get_by_id(self, model_id):
        obj = self.space.select(model_id)
        if len(obj) == 0:
            return None

        return models.DisciplineWorkProgram(*obj[0])

    def get_by_filter(self, index, key):
        raw_objects = self.space.select(key, index=index)
        if len(obj) == 0:
            return None, None

        models_list = list()
        primary_keys = list()
        for obj in raw_objects:
            model = models.DisciplineWorkProgram(*obj)
            models_list.append(model)
            primary_keys.append(model.id)

        return models_list, primary_keys

    def get_objects_count_by_filter(self, field, key):
        raise NotImplementedError

    def get_all(self):
        raw_objects = self.space.select()
        if len(raw_objects) == 0:
            return None

        models_list = list()
        for obj in raw_objects:
            models_list.append(models.DisciplineWorkProgram(*obj))

        return models_list

    def remove(self, id):
        obj = self.space.delete(id)
        if len(obj) == 0:
            return None

        return obj

    def edit(self, *args, **kwargs):
        obj_id = kwargs['id']
        updated_args = Utils.get_tarantool_update_args(kwargs['fields'], self._meta['field_names'])

        return self.space.update(obj_id, updated_args)[0]


class LearningOutcomesRepoTarantool(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "space_name": "learning_outcomes",
            "field_names": {
                "id": 1,
                "discipline_id": 2,
                "competency_code": 3,
                "formulation": 4,
                "results": 5,
                "forms_and_methods": 6,
            }
        }

        self.space = connection.space(self._meta['space_name'])

    def save(self, model):
        if not isinstance(model, models.LearningOutcomes):
            logging.error("Trying to save LeraningOutcomes object of invalid type")
            raise TypeError("Expected object is instance of LearningOutcomes")

        self.space.insert(tuple(model.__dict__.values()))

    def get_by_id(self, model_id):
        return NotImplementedError

    def get_by_filter(self, index, key):
        raw_objects = self.space.select(key, index=index)
        if len(raw_objects) == 0:
            return None, None

        models_list = list()
        primary_keys = list()
        for obj in raw_objects:
            model = models.LearningOutcomes(*obj)
            models_list.append(model)
            primary_keys.append(model.id)

        return models_list, primary_keys

    def get_objects_count_by_filter(self, field, key):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def remove(self, id):
        obj = self.space.delete(id)
        if len(obj) == 0:
            return None

        return obj

    def edit(self, *args, **kwargs):
        raise NotImplementedError


class EducationalProgramRepoTarantool(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "space_name": "educational_program",
            "interconnection_space_name": "discipline_educational_program",
            "isp_field": "educational_program_id",
            "field_names": {
                "id": 1,
                "name": 2
            }
        }

        self.space = connection.space(self._meta['space_name'])

    def save(self, model):
        raise NotImplementedError # TODO

    def get_by_id(self, model_id):
        raise NotImplementedError

    def get_by_filter(self, key, index):
        raise NotImplementedError # TODO

    def get_objects_count_by_filter(self, index, key):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def remove(self, id):
        obj = self.space.delete(id)
        if len(obj) == 0:
            return None

        return obj

    def edit(self, *args, **kwargs):
        raise NotImplementedError

class DisciplineScopeRepoTarantool(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "space_name": "discipline_scope_semester",
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

        self.space = connection.space(self._meta['space_name'])

    def save(self, model):
        if not isinstance(model, models.DisciplineScope):
            logging.error("Trying to save DisciplineScope object of invalid type")
            raise TypeError("Expected object is instance of DisciplineScope")

        self.space.insert(tuple(model.__dict__.values()))

    def get_by_id(self, model_id):
        raise NotImplementedError

    def get_by_filter(self, index, key):
        raw_objects = self.space.select(key, index=index)
        if len(raw_objects) == 0:
            return None, None

        models_list = list()
        primary_keys = list()
        for obj in raw_objects:
            model = models.DisciplineScope(*obj)
            models_list.append(model)
            primary_keys.append(model.id)

        return models_list, primary_keys

    def get_objects_count_by_filter(self, field, key):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def remove(self, id):
        obj = self.space.delete(id)
        if len(obj) == 0:
            return None

        return obj

    def edit(self, *args, **kwargs):
        raise NotImplementedError


class DisciplineModuleRepoTarantool(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "space_name": "discipline_module",
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

        self.space = connection.space(self._meta['space_name'])

    def save(self, model):
        if not isinstance(model, models.DisciplineModule):
            logging.error("Trying to save DisciplineModule object of invalid type")
            raise TypeError("Expected object is instance of DisciplineModule")

        self.space.insert(tuple(model.__dict__.values()))

    def get_by_id(self, model_id):
        raise NotImplementedError

    def get_by_filter(self, index, key):
        raw_objects = self.space.select(key, index=index)
        if len(raw_objects) == 0:
            return None, None

        models_list = list()
        primary_keys = list()
        for obj in raw_objects:
            model = models.DisciplineModule(*obj)
            models_list.append(model)
            primary_keys.append(model.id)

        return models_list, primary_keys

    def get_objects_count_by_filter(self, field, key):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def remove(self, id):
        obj = self.space.delete(id)
        if len(obj) == 0:
            return None

        return obj

    def edit(self, *args, **kwargs):
        raise NotImplementedError


class DisciplineMaterialRepoTarantool(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "space_name": "discipline_material",
            "field_names": {"id": 1, "discipline_id": 2, "materials": 3}
        }

        self.space = connection.space(self._meta['space_name'])

    def save(self, model):
        if not isinstance(model, models.DisciplineMaterial):
            logging.error("Trying to save DisciplineMaterial object of invalid type")
            raise TypeError("Expected object is instance of DisciplineMaterial")

        self.space.insert(tuple(model.__dict__.values()))

    def get_by_id(self, model_id):
        raise NotImplementedError

    def get_by_filter(self, index, key):
        raw_objects = self.space.select(key, index=index)
        if len(raw_objects) == 0:
            return None, None

        models_list = list()
        primary_keys = list()
        for obj in raw_objects:
            model = models.DisciplineMaterial(*obj)
            models_list.append(model)
            primary_keys.append(model.id)

        return models_list, primary_keys

    def get_objects_count_by_filter(self, field, key):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def remove(self, id):
        obj = self.space.delete(id)
        if len(obj) == 0:
            return None

        return obj

    def edit(self, *args, **kwargs):
        raise NotImplementedError
