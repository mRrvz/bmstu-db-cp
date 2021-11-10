""" Just a controller """

import os

from db.repos.postgres import *
from db.repos.tarantool import *
from db.utils import PostgresConnection, TarantoolConnection


class Controller():
    def __init__(self):
        self.postgres_conn = PostgresConnection(
            os.getenv("POSTGRES_DB"),
            os.getenv("POSTGRES_USER"),
            os.getenv("POSTGRES_PASSWORD"),
            os.getenv("POSTGRES_HOST")
        )

        self.tarantool_conn = TarantoolConnection(
            os.getenv("TARANTOOL_USER"),
            os.getenv("TARANTOOL_PASSWORD"),
            os.getenv("TARANTOOL_HOST"),
            os.getenv("TARANTOOL_PORT")
        )

        self.discipline_work_program_repo_psql = DisciplineWorkProgramRepoPSQL(self.postgres_conn.get())
        self.learning_outcomes_repo_psql = LearningOutcomesRepoPSQL(self.postgres_conn.get())
        self.educational_program_repo_psql = EducationalProgramRepoPSQL(self.postgres_conn.get())
        self.discipline_scope_repo_psql = DisciplineScopeRepoPSQL(self.postgres_conn.get())
        self.discipline_module_repo_psql = DisciplineModuleRepoPSQL(self.postgres_conn.get())
        self.discipline_material_repo_psql = DisciplineMaterialRepoPSQL(self.postgres_conn.get())
        self.user_repo_psql = UserRepoPSQL(self.postgres_conn.get())

        self.discipline_work_program_repo_tarantool = DisciplineWorkProgramRepoTarantool(self.tarantool_conn.get())
        self.learning_outcomes_repo_tarantool = LearningOutcomesRepoTarantool(self.tarantool_conn.get())
        self.educational_program_repo_tarantool = EducationalProgramRepoTarantool(self.tarantool_conn.get())
        self.discipline_scope_repo_tarantool = DisciplineScopeRepoTarantool(self.tarantool_conn.get())
        self.discipline_module_repo_tarantool = DisciplineModuleRepoTarantool(self.tarantool_conn.get())
        self.discipline_material_repo_tarantool = DisciplineMaterialRepoTarantool(self.tarantool_conn.get())

        self.psql_repos = {
            "discipline_work_program": self.discipline_work_program_repo_psql,
            "learning_outcomes": self.learning_outcomes_repo_psql,
            "educational_program": self.educational_program_repo_psql,
            "discipline_scope_semester": self.discipline_scope_repo_psql,
            "discipline_module": self.discipline_module_repo_psql,
            "discipline_material": self.discipline_material_repo_psql,
            "user": self.user_repo_psql,
        }

        self.tarantool_repos = {
            "discipline_work_program": self.discipline_work_program_repo_tarantool,
            "learning_outcomes": self.learning_outcomes_repo_tarantool,
            "educational_program": self.educational_program_repo_tarantool,
            "discipline_scope_semester": self.discipline_scope_repo_tarantool,
            "discipline_module": self.discipline_module_repo_tarantool,
            "discipline_material": self.discipline_material_repo_tarantool,
        }
