import db.models as models
from db.utils import Utils
from document_parser import DocumentParser


class RpdService:
    def __init__(self, repo_psql, repo_tt, cache):
        self.repos = {
            "storage": repo_psql,
            "cache": repo_tt,
        }

        self.cache = cache

    def save_rpd(self, filename):
        parser = DocumentParser(filename)
        model = parser.get_discipline_program()
        model.id = self.repos["storage"]["discipline_work_program"].save(model)
        Utils.save_discipline_fields(model, self.repos["storage"])
        return model

    def get_rpd(self, rpd_id):
        model = self.cache.get_by_primary(rpd_id, "discipline_work_program", self.repos)
        model = Utils.collect_discipline_fields(model, self.cache, self.repos)
        return model

    def update_rpd(self, rpd_id, model):
        for field in model__dict__.keys():
            value = getattr(self, field)
            value.pop("id")
            self.repos["storage"][field].edit(id=rpd_id, fields=value)

    def remove_rpd(self, rpd_id):
        model = self.cache.get_by_primary(rpd_id, "discipline_work_program", self.repos)
        Utils.remove_discipline_fields(model, self.cache, self.repos)
        self.repos["storage"]["discipline_work_program"].remove(model.id)

    def to_rpd(self, json):
        return models.DisciplineWorkProgram(
            json["name"],
            json["author"],
            json["competency"],
            # Это не работает, тут надо вложенный жсон распаковать
            models.LearningOutcomes(json["learning_outcomes"]),
            models.EducationProgram(json["educational_program"]),
            models.DisciplineScopeSemester(json["discipline_scope_semester"]),
            models.DisciplineModule(json["module"]),
            modles.DisciplineMaterial(json["discipline_material"])
        )
