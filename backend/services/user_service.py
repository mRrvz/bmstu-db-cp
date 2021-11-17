from flask_jwt_extended import create_access_token, create_refresh_token

import db.models as models


class UserService:
    def __init__(self, repos):
        self.repos = repos

    def login(self, data):
        access_token = create_access_token(identity = data['username'])
        refresh_token = create_refresh_token(identity = data['username'])
        return {"access_token": access_token, "refresh_token": refresh_token}

    def save_user(self, user):
        model = models.User(user["username"], user["password"], user["email"], user["status"])
        self.repos.save(model)
        access_token = create_access_token(identity = user['username'])
        refresh_token = create_refresh_token(identity = user['username'])
        return {"user": model, "access_token": access_token, "refresh_token": refresh_token}

    def remove_user(self, username):
        return self.repos.remove(username)
