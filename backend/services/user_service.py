from flask_jwt_extended import create_access_token, create_refresh_token

import db.models as models


class UserService:
    def __init__(self, repos):
        self.repos = repos

    def login(self, username, password):
        access_token = create_access_token(identity = username)
        refresh_token = create_refresh_token(identity = username)
        return {"access_token": access_token, "refresh_token": refresh_token}

    def save_user(self, model):
        self.repos.save(model)
        access_token = create_access_token(identity = model.username)
        refresh_token = create_refresh_token(identity = model.username)
        return {"user": model, "access_token": access_token, "refresh_token": refresh_token}

    def remove_user(self, username):
        return self.repos.remove(username)

    def to_user(self, json):
        return models.User(json["username"], json["password"], json["email"], json["status"])
