import os

import db.repository as repo
from db.utils import Connection

class Controller():
    def __init__(self):
        self.connection = Connection(
            os.getenv("POSTGRES_DB"),
            os.getenv("POSTGRES_USER"),
            os.getenv("POSTGRESS_PASSWORD"),
            os.getenv("POSTGRES_HOST")
        )

        self.discipline_work_program_repo = repo.DisciplineWorkProgramRepo(self.connection.get())
        self.learning_outcomes_repo = repo.DisciplineOutcomesRepo(self.connection.get())
        self.educational_program_repo = repo.EducationalProgramRepo(self.connection.get())
        self.discipline_scope_repo = repo.DisciplineScopeRepo(self.connection.get())
        self.discipline_module_repo = repo.DisciplineModuleRepo(self.connection.get())
        self.discipline_material_repo = repo.DisciplineMaterialRepo(self.connection.get())
