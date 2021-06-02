from abc import ABC, abstractmethod
import db.models as m

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
            "table_name": "discipline_work_program"
        }

    def save(self, model):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {self._meta['table_name']} VALUES (%s, %s, %s, %s)",
                (model.id, model.name, model.author, model.competency),
            )

            self.connection.commit()

    def get_by_id(self, model_id):
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"SELECT * FROM {self._meta['table_name']} WHERE id = %s", (str(model_id))
            )

            raw = cursor.fetchall()[0]
            return m.DisciplineWorkProgram(*raw)


    def get_all(self):
        pass

    def remove(self, id):
        pass

    def edit(self, *args, **kwargs):
        pass


class LearningOutcomesRepo(AbstractRepo):
    def __init__(self, connection):
        self.connection = connection
        self._meta = {
            "table_name": "learning_outcomes"
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
            "table_name": "educational_program"
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
            "table_name": "discipline_scope_semester"
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
            "table_name": "discipline_module"
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
            "table_name": "discipline_material"
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
