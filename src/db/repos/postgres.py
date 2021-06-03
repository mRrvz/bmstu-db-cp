""" PostrgreSQL repos """

import logging
import psycopg2

from db.utils import Utils
from db.repos.abstract import AbstractRepo
import db.models as models

class DisciplineWorkProgramRepoPSQL(AbstractRepo):
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
            cursor.execute(f"DELETE FROM {self._meta['table_name']} WHERE id = %s", (id,))
            if cursor.rowcount == 0:
                raise ValueError(f"Work program of discipline with id = {id} doesn't exists.")

            self.connection.commit()

    def edit(self, *args, **kwargs):
        obj_id = kwargs['id']
        updated_args_str, updated_args = Utils.get_psql_update_args(kwargs['fields'])

        with self.connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE {self._meta['table_name']} SET {updated_args_str} WHERE id = %s",
                (updated_args, *obj_id,)
            )

            self.connection.commit()


class LearningOutcomesRepoPSQL(AbstractRepo):
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
        if not isinstance(model, models.LearningOutcomes):
            logging.error("Trying to save LearningOutcomes object of invalid type")
            raise TypeError("Expected object is instance of LearningOutcomes")

        with self.connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {self._meta['table_name']} VALUES (%s, %s, %s, %s, %s, %s)", (
                    model.id, model.discipline_id, model.competency_code,
                    model.formulation, model.results, model.forms_and_methods
                ),
            )

            self.connection.commit()

    def get_by_id(self, model_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']} WHERE id = %s", (model_id,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                raise ValueError(f"Learning outcomes of discipline with id = {model_id} doesn't exists")

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
            cursor.execute(f"DELETE FROM {self._meta['table_name']} WHERE id = %s", (id,))
            if cursor.rowcount == 0:
                raise ValueError(f"Learning outcomes of discipline with id = {id} doesn't exists.")

            self.connection.commit()

    def edit(self, *args, **kwargs):
        obj_id = kwargs['id']
        updated_args_str, updated_args = Utils.get_psql_update_args(kwargs['fields'])

        with self.connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE {self._meta['table_name']} SET {updated_args_str} WHERE id = %s",
                (updated_args, *obj_id,)
            )

            self.connection.commit()


class EducationalProgramRepoPSQL(AbstractRepo):
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
        if not isinstance(model, models.EducationalProgram(id, name)):
            logging.error("Trying to save EducationalProgram object of invalid type")
            raise TypeError("Expected object is instance of EducationalProgram")

        with self.connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {self._meta['table_name']} VALUES (%s, %s)",  (model.id, model.name)
            )

            self.connection.commit()

    def get_by_id(self, model_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']} WHERE id = %s", (model_id,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                raise ValueError(f"Educational program of discipline with id = {model_id} doesn't exists")

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
            cursor.execute(f"DELETE FROM {self._meta['table_name']} WHERE id = %s", (id,))
            if cursor.rowcount == 0:
                raise ValueError(f"Educational program of discipline with id = {id} doesn't exists.")

            self.connection.commit()

    def edit(self, *args, **kwargs):
        obj_id = kwargs['id']
        updated_args_str, updated_args = Utils.get_psql_update_args(kwargs['fields'])

        with self.connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE {self._meta['table_name']} SET {updated_args_str} WHERE id = %s",
                (updated_args, *obj_id,)
            )

            self.connection.commit()

class DisciplineScopeRepoPSQL(AbstractRepo):
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
        if not isinstance(model, models.DisciplineScope):
            logging.error("Trying to save DisciplineScope object of invalid type")
            raise TypeError("Expected object is instance of DisciplineScope")

        with self.connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {self._meta['table_name']} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                    model.id, model.discipline_id, model.semester_number, model.credit_units,
                    model.total_hours, model.lectures_hours, model.seminars_hours,
                    model.laboratory_hours, model.independent_hours, model.certification_type
                ),
            )

            self.connection.commit()

    def get_by_id(self, model_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']} WHERE id = %s", (model_id,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                raise ValueError(f"Scope of discipline with id = {model_id} doesn't exists")

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
            cursor.execute(f"DELETE FROM {self._meta['table_name']} WHERE id = %s", (id,))
            if cursor.rowcount == 0:
                raise ValueError(f"Scope of discipline with id = {id} doesn't exists.")

            self.connection.commit()

    def edit(self, *args, **kwargs):
        obj_id = kwargs['id']
        updated_args_str, updated_args = Utils.get_psql_update_args(kwargs['fields'])

        with self.connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE {self._meta['table_name']} SET {updated_args_str} WHERE id = %s",
                (updated_args, *obj_id,)
            )

            self.connection.commit()


class DisciplineModuleRepoPSQL(AbstractRepo):
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
        if not isinstance(model, models.DisciplineModule):
            logging.error("Trying to save DisciplineModule object of invalid type")
            raise TypeError("Expected object is instance of DisciplineModule")

        with self.connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {self._meta['table_name']} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                    model.id, model.discipline_id, model.name, model.semester_number,
                    model.lectures_hours, model.classroom_hours, model.seminars_hours,
                    model.laboratory_hours, model.independent_hours, model.min_score,
                    model.max_score, model.competency_code
                ),
            )

            self.connection.commit()

    def get_by_id(self, model_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']} WHERE id = %s", (model_id,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                raise ValueError(f"Module of discipline with id = {model_id} doesn't exists")

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
            cursor.execute(f"DELETE FROM {self._meta['table_name']} WHERE id = %s", (id,))
            if cursor.rowcount == 0:
                raise ValueError(f"Module of discipline with id = {id} doesn't exists.")

            self.connection.commit()

    def edit(self, *args, **kwargs):
        obj_id = kwargs['id']
        updated_args_str, updated_args = Utils.get_psql_update_args(kwargs['fields'])

        with self.connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE {self._meta['table_name']} SET {updated_args_str} WHERE id = %s",
                (updated_args, *obj_id,)
            )

            self.connection.commit()


class DisciplineMaterialRepoPSQL(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "table_name": "discipline_material",
            "field_names": {"id": int, "discipline_id": int, "materials": str}
        }

    def save(self):
        if not isinstance(model, models.DisciplineMaterial):
            logging.error("Trying to save DisciplineMaterial object of invalid type")
            raise TypeError("Expected object is instance of DisciplineMaterial")

        with self.connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {self._meta['table_name']} VALUES (%s, %s, %s)", (
                    model.id, model.discipline_id, model.material
                ),
            )

            self.connection.commit()

    def get_by_id(self, model_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']} WHERE id = %s", (model_id,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                raise ValueError(f"Material's of discipline with id = {model_id} doesn't exists")

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
            cursor.execute(f"DELETE FROM {self._meta['table_name']} WHERE id = %s", (id,))
            if cursor.rowcount == 0:
                raise ValueError(f"Materials of discipline with id = {id} doesn't exists.")

            self.connection.commit()

    def edit(self, *args, **kwargs):
        obj_id = kwargs['id']
        updated_args_str, updated_args = Utils.get_psql_update_args(kwargs['fields'])

        with self.connection.cursor() as cursor:
            cursor.execute(
                f"UPDATE {self._meta['table_name']} SET {updated_args_str} WHERE id = %s",
                (updated_args, *obj_id,)
            )

            self.connection.commit()
