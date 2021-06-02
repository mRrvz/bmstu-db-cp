""" Repos for work with database """

from abc import ABC, abstractmethod
import logging
import psycopg2

import db.models as models
from db.utils import Formatter

#logging.basicConfig(filename='logs.txt', level=logging.DEBUG)

class AbstractRepo(ABC):
    @abstractmethod
    def save(self, model):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, model_id):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def remove(self, model_id):
        raise NotImplementedError

    @abstractmethod
    def edit(self, *args, **kwargs):
        raise NotImplementedError


class DisciplineWorkProgramRepo(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "table_name": "discipline_work_program",
            "field_names": {"id": int, "name": str, "author": str, "competency": str}
        }

    def save(self, model):
        if not isinstance(model, models.DisciplineWorkProgram):
            logging.error("Trying to save DisciplineWorkProgram object of invalid type")
            raise TypeError("Expected object is instance of DisciplineWorkProgram")

        with self.connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {self._meta['table_name']} VALUES (%s, %s, %s, %s)",
                (model.id, model.name, model.author, model.competency),
            )

            self.connection.commit()

    def get_by_id(self, model_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']} WHERE id = %s", (model_id,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                raise ValueError(f"Work program of discipline with id = {model_id} doesn't exists")

        return models.DisciplineWorkProgram(*orm_objects[0])

    def get_all(self):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']}")
            orm_objects = cursor.fetchall()

        objects = list()
        for obj in orm_objects:
            objects.append(models.DisciplineWorkProgram(*obj))

        return objects

    def remove(self, id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {self._meta['table_name']} WHERE id = %s", str(id))
            if cursor.rowcount == 0:
                raise ValueError(f"Work program of discipline with id = {id} doesn't exists.")

            self.connection.commit()

    def edit(self, *args, **kwargs):
        obj_id = kwargs['id']
        logging.error("AYE_")
        updated_args_str, updated_args = Formatter.get_update_args(kwargs['fields'])
        logging.error(updated_args_str)

        with self.connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE {self._meta['table_name']} SET {updated_args_str} WHERE id = %s",
                (updated_args, *obj_id,)
            )

            self.connection.commit()


class LearningOutcomesRepo(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "table_name": "learning_outcomes",
            "field_names": {
                "id": int,
                "discipline_id": int,
                "competency_code": str,
                "formulation": str,
                "results": str,
                "forms_and_methods": str,
            }
        }

    def save(self):
        pass

    def get_by_id(self):
        pass

    def get_all(self):
        pass

    def remove(self, id):
        pass

    def edit(self, *args, **kwargs):
        pass


class EducationalProgramRepo(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "table_name": "educational_program",
            "field_names": {
                "id": int,
                "name": str
            }
        }

    def save(self):
        pass

    def get_by_id(self):
        pass

    def get_all(self):
        pass

    def remove(self, id):
        pass

    def edit(self, *args, **kwargs):
        pass


class DisciplineScopeRepo(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "table_name": "discipline_scope_semester",
            "field_names": {
                "id": int,
                "discipline_id": int,
                "semester_number": int,
                "credit_units": int,
                "total_hours": int,
                "lectures_hours": int,
                "laboratory_work_hours": int,
                "independent_work_hours": int,
                "certification_type": str
            }
        }

    def save(self):
        pass

    def get_by_id(self):
        pass

    def get_all(self):
        pass

    def remove(self, id):
        pass

    def edit(self, *args, **kwargs):
        pass


class DisciplineModuleRepo(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "table_name": "discipline_module",
            "field_names": {
                "id": int,
                "discipline_id": int,
                "name": str,
                "semester_number": int,
                "lectures_hours": int,
                "seminars_hours": int,
                "laboratory_work_hours": int,
                "independent_work_hours": int,
                "min_scores": int,
                "max_scores": int,
                "competency_codes": str
            }
        }

    def save(self):
        pass

    def get_by_id(self):
        pass

    def get_all(self):
        pass

    def remove(self, id):
        pass

    def edit(self, *args, **kwargs):
        pass


class DisciplineMaterialRepo(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "table_name": "discipline_material",
            "field_names": {"id": int, "discipline_id": int, "materials": str}
        }

    def save(self):
        pass

    def get_by_id(self):
        pass

    def get_all(self):
        pass

    def remove(self, id):
        pass

    def edit(self, *args, **kwargs):
        pass
