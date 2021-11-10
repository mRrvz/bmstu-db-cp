""" PostrgreSQL repos """

import logging

import db.models as models
import psycopg2
from db.repos.abstract import AbstractRepo
from db.utils import Utils


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
            insert_names = Utils.get_insert_fields(self._meta["field_names"])
            cursor.execute(
                f"INSERT INTO {self._meta['table_name']} {insert_names} VALUES (%s, %s, %s) RETURNING id",
                (model.name, model.author, model.competency),
            )

            self.connection.commit()
            return cursor.fetchone()[0] # Return id of new row in database

    def get_by_id(self, model_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']} WHERE id = %s", (model_id,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                raise ValueError(f"Work program of discipline with id = {model_id} doesn't exists")

        return models.DisciplineWorkProgram(*orm_objects[0])

    def get_by_filter(self, filter, keys):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']} WHERE {filter}", keys)

            orm_objects = cursor.fetchall()
            if len(orm_objects) == 0:
                return None, None

        models_list = list()
        primary_keys = list()
        for obj in orm_objects:
            model = models.DisciplineWorkProgram(*obj)
            models_list.append(model)
            primary_keys.append(model.id)

        return models_list, primary_keys

    def get_objects_count_by_filter(self, field, key):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {self._meta['table_name']} WHERE {field} = %s", (key,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                return None

        return orm_objects[0][0]

    def get_all(self):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']}")
            orm_objects = cursor.fetchall()

        models_list = list()
        for obj in orm_objects:
            models_list.append(models.DisciplineWorkProgram(*obj))

        return models_list

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
                (*updated_args, obj_id,)
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

    def save(self, model):
        if not isinstance(model, models.LearningOutcomes):
            logging.error("Trying to save LearningOutcomes object of invalid type")
            raise TypeError("Expected object is instance of LearningOutcomes")

        with self.connection.cursor() as cursor:
            insert_names = Utils.get_insert_fields(self._meta["field_names"])
            cursor.execute(
                f"INSERT INTO {self._meta['table_name']} {insert_names} VALUES (%s, %s, %s, %s, %s) RETURNING id", (
                    model.discipline_id, model.competency_code,
                    model.formulation, model.results, model.forms_and_methods
                ),
            )

            self.connection.commit()
            return cursor.fetchone()[0]

    def get_by_id(self, model_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']} WHERE id = %s", (model_id,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                raise ValueError(f"Learning outcomes of discipline with id = {model_id} doesn't exists")

        return models.LearningOutcomes(*orm_objects[0])

    def get_by_filter(self, filter, keys):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']} WHERE {filter}", keys)

            orm_objects = cursor.fetchall()
            if len(orm_objects) == 0:
                return None, None

        models_list = list()
        primary_keys = list()
        for obj in orm_objects:
            model = models.LearningOutcomes(*obj)
            models_list.append(model)
            primary_keys.append(model.id)

        return models_list, primary_keys

    def get_objects_count_by_filter(self, field, key):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {self._meta['table_name']} WHERE {field} = %s", (key,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                return None

        return orm_objects[0][0]

    def get_all(self):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']}")
            orm_objects = cursor.fetchall()

        models_list = list()
        for obj in orm_objects:
            models_list.append(models.LearningOutcomes(*obj))

        return models_list

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
                (*updated_args, obj_id,)
            )

            self.connection.commit()


class EducationalProgramRepoPSQL(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "table_name": "educational_program",
            "interconnection_table_name": "discipline_educational_program",
            "ict_field_name": "educational_program_id",
            "field_names": {
                "id": int,
                "name": str
            }
        }

    def save(self, model):
        if not isinstance(model, models.EducationalProgram):
            logging.error("Trying to save EducationalProgram object of invalid type")
            raise TypeError("Expected object is instance of EducationalProgram")

        with self.connection.cursor() as cursor:
            try:
                cursor.execute(
                    f"INSERT INTO {self._meta['table_name']} VALUES (%s, %s) RETURNING id",
                        (model.id, model.name))
            except psycopg2.errors.UniqueViolation:
                self.connection.commit()
                model.id = self.get_by_id(model.id).id

            cursor.execute(f"INSERT INTO {self._meta['interconnection_table_name']} \
                    VALUES (%s, %s)", (model.discipline_id, model.id))

            self.connection.commit()
            return model.id

    def get_by_id(self, model_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']} WHERE id = %s", (model_id,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                raise ValueError(f"Educational program with id = {model_id} doesn't exists")

        return models.EducationalProgram(*orm_objects[0])

    def get_by_filter(self, filter, keys):
        with self.connection.cursor() as cursor:
            cursor.execute(f"\
                SELECT id, name FROM {self._meta['interconnection_table_name']} \
                JOIN {self._meta['table_name']} ON (id = {self._meta['ict_field_name']}) \
                WHERE {filter}", keys)

            orm_objects = cursor.fetchall()
            if len(orm_objects) == 0:
                return None, None

        models_list = list()
        primary_keys = list()
        for obj in orm_objects:
            model = models.EducationalProgram(*obj)
            model.discipline_id = keys[0]
            models_list.append(model)
            primary_keys.append(model.id)

        return models_list, primary_keys

    def get_objects_count_by_filter(self, field, key):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {self._meta['table_name']} WHERE {field} = %s", (key,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                return None

        return orm_objects[0][0]

    def get_all(self):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']}")
            orm_objects = cursor.fetchall()

        models_list = list()
        for obj in orm_objects:
            models_list.append(models.EducationalProgram(*obj))

        return models_list

    def remove(self, id, *args, **kwargs):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"DELETE FROM {self._meta['interconnection_table_name']} WHERE discipline_id = %s",
                (kwargs['discipline_id'],))

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
                (*updated_args, obj_id,)
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
                "seminars_hours": int,
                "laboratory_work_hours": int,
                "independent_work_hours": int,
                "certification_type": str
            }
        }

    def save(self, model):
        if not isinstance(model, models.DisciplineScope):
            logging.error("Trying to save DisciplineScope object of invalid type")
            raise TypeError("Expected object is instance of DisciplineScope")

        with self.connection.cursor() as cursor:
            insert_names = Utils.get_insert_fields(self._meta["field_names"])
            cursor.execute(
                f"INSERT INTO {self._meta['table_name']} {insert_names} VALUES \
                 (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id", (
                    model.discipline_id, model.semester_number, model.credit_units,
                    model.total_hours, model.lectures_hours, model.seminars_hours,
                    model.laboratory_hours, model.independent_hours, model.certification_type
                ),
            )

            self.connection.commit()
            return cursor.fetchone()[0]

    def get_by_id(self, model_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']} WHERE id = %s", (model_id,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                raise ValueError(f"Scope of discipline with id = {model_id} doesn't exists")

        return models.DisciplineScope(*orm_objects[0])

    def get_by_filter(self, filter, keys):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']} WHERE {filter}", keys)

            orm_objects = cursor.fetchall()
            if len(orm_objects) == 0:
                return None, None

        models_list = list()
        primary_keys = list()
        for obj in orm_objects:
            model = models.DisciplineScope(*obj)
            models_list.append(model)
            primary_keys.append(model.id)

        return models_list, primary_keys

    def get_objects_count_by_filter(self, field, key):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {self._meta['table_name']} WHERE {field} = %s", (key,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                return None

        return orm_objects[0][0]

    def get_all(self):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']}")
            orm_objects = cursor.fetchall()

        models_list = list()
        for obj in orm_objects:
            models_list.append(models.DisciplineScope(*obj))

        return models_list

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
                (*updated_args, obj_id,)
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

    def save(self, model):
        if not isinstance(model, models.DisciplineModule):
            logging.error("Trying to save DisciplineModule object of invalid type")
            raise TypeError("Expected object is instance of DisciplineModule")

        with self.connection.cursor() as cursor:
            insert_names = Utils.get_insert_fields(self._meta["field_names"])
            cursor.execute(
                f"INSERT INTO {self._meta['table_name']} {insert_names} VALUES \
                 (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id", (
                    model.discipline_id, model.name, model.semester_number,
                    model.lectures_hours, model.seminars_hours,
                    model.laboratory_hours, model.independent_hours, model.min_score,
                    model.max_score, model.competency_code
                ),
            )

            self.connection.commit()
            return cursor.fetchone()[0]

    def get_by_id(self, model_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']} WHERE id = %s", (model_id,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                raise ValueError(f"Module of discipline with id = {model_id} doesn't exists")

        return models.DisciplineModule(*orm_objects[0])

    def get_by_filter(self, filter, keys):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']} WHERE {filter}", keys)

            orm_objects = cursor.fetchall()
            if len(orm_objects) == 0:
                return None, None

        models_list = list()
        primary_keys = list()
        for obj in orm_objects:
            model = models.DisciplineModule(*obj)
            models_list.append(model)
            primary_keys.append(model.id)

        return models_list, primary_keys

    def get_objects_count_by_filter(self, field, key):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {self._meta['table_name']} WHERE {field} = %s", (key,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                return None

        return orm_objects[0][0]

    def get_all(self):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']}")
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                return None

        models_list = list()
        for obj in orm_objects:
            models_list.append(models.DisciplineModule(*obj))

        return models_list

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
                (*updated_args, obj_id,)
            )

            self.connection.commit()


class DisciplineMaterialRepoPSQL(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "table_name": "discipline_material",
            "field_names": {"id": int, "discipline_id": int, "material": str}
        }

    def save(self, model):
        if not isinstance(model, models.DisciplineMaterial):
            logging.error("Trying to save DisciplineMaterial object of invalid type")
            raise TypeError("Expected object is instance of DisciplineMaterial")

        with self.connection.cursor() as cursor:
            insert_names = Utils.get_insert_fields(self._meta["field_names"])
            cursor.execute(
                f"INSERT INTO {self._meta['table_name']} {insert_names} VALUES (%s, %s) RETURNING id", (
                    model.discipline_id, model.material
                ),
            )

            self.connection.commit()
            return cursor.fetchone()[0]

    def get_by_id(self, model_id):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']} WHERE id = %s", (model_id,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                raise ValueError(f"Material's of discipline with id = {model_id} doesn't exists")

        return models.DisciplineMaterial(*orm_objects[0])

    def get_by_filter(self, filter, keys):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']} WHERE {filter}", keys)

            orm_objects = cursor.fetchall()
            if len(orm_objects) == 0:
                return None, None

        models_list = list()
        primary_keys = list()
        for obj in orm_objects:
            model = models.DisciplineMaterial(*obj)
            models_list.append(model)
            primary_keys.append(model.id)

        return models_list, primary_keys

    def get_objects_count_by_filter(self, field, key):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT COUNT(*) FROM {self._meta['table_name']} WHERE {field} = %s", (key,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                return None

        return orm_objects[0][0]

    def get_all(self):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']}")
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                return None

        models_list = list()
        for obj in orm_objects:
            models_list.append(models.DisciplineMaterial(*obj))

        return models_list

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
                (*updated_args, obj_id,)
            )

            self.connection.commit()


class UserRepoPSQL(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "table_name": "userdb",
            "field_names": {"username": str, "password": str, "email": str, "status": str}
        }

    def save(self, model):
        if not isinstance(model, models.User):
            logging.error("Trying to save User object of invalid type")
            raise TypeError("Expected object is instance of User")

        with self.connection.cursor() as cursor:
            insert_names = Utils.get_insert_fields(self._meta["field_names"])
            cursor.execute(
                f"INSERT INTO {self._meta['table_name']} {insert_names} VALUES (%s, %s, %s, %s)",
                (model.username, model.password, model.email, model.status),
            )

            self.connection.commit()

    def get_by_id(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']} WHERE username = %s", (username,))
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                raise ValueError(f"User with id = {username} doesn't exists")

        return models.DisciplineMaterial(*orm_objects[0])

    def get_by_filter(self, filter, keys):
        raise NotImplementedError

    def get_objects_count_by_filter(self, filter, keys):
        raise NotImplementedError

    def get_all(self):
        with self.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {self._meta['table_name']}")
            orm_objects = cursor.fetchall()

            if len(orm_objects) == 0:
                return None

        models_list = list()
        for obj in orm_objects:
            models_list.append(models.DisciplineMaterial(*obj))

    def remove(self, username):
        with self.connection.cursor() as cursor:
            cursor.execute(f"DELETE FROM {self._meta['table_name']} WHERE username = %s", (username,))
            if cursor.rowcount == 0:
                raise ValueError(f"User with username '{username}' doesn't exists.")

            self.connection.commit()

    def edit(self, *args, **kwargs):
        raise NotImplementedError