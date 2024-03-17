"""User api controller module."""

import datetime

import jwt
from flask import jsonify, make_response, request
from sqlalchemy import and_

from api.base import ApiController, instance_method_route
from api.common import delete_row, make_query
from app import app
from models.candidate.candidate import Candidate as TCandidate
from models.professional.professional import Professional as TProfessional


class User(ApiController):
    """User Api Controller"""

    def __init__(self):
        self.user_group_tables_map = {
            "professional": TProfessional,
            "candidate": TCandidate,
        }

    @staticmethod
    def encode_auth_token(user_id, secret_key):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(days=0, seconds=5),
                "iat": datetime.datetime.utcnow(),
                "sub": user_id,
            }
            return jwt.encode(payload, secret_key, algorithm="HS256")
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token, secret_key):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, secret_key, algorithms=["HS256"])
            return True, payload["sub"]
        except jwt.ExpiredSignatureError:
            return False, "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return False, "Invalid token. Please log in again."

    @instance_method_route("user/<user_group>", methods=["GET"])
    def user(self, user_group):
        """Get a user to login."""
        auth_header = request.headers.get("Authorization")
        table = self.user_group_tables_map[user_group]
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            succeed, resp = self.decode_auth_token(
                auth_token, app.config.get("SECRET_KEY")
            )
            if succeed:
                user = make_query(table, filters=table.username == resp).first()
                response_object = {
                    "status": "success",
                    "data": {
                        "username": user.username,
                        "email": user.email,
                        "id": str(user.id),
                    },
                }
                return make_response(jsonify(response_object)), 200
            response_object = {"status": "fail", "message": resp}
            return make_response(jsonify(response_object)), 401
        response_object = {
            "status": "fail",
            "message": "Authentication token is missing or invalid.",
        }
        return make_response(jsonify(response_object)), 401

    @instance_method_route("delete_user_account/<user_group>", methods=["GET"])
    def delete_user_account(self, user_group):
        """Delete user route."""
        auth_header = request.headers.get("Authorization")
        table = self.user_group_tables_map[user_group]
        if auth_header:
            auth_token = auth_header.split(" ")[1]
            succeed, resp = self.decode_auth_token(
                auth_token, app.config.get("SECRET_KEY")
            )
            if succeed:
                delete_row(
                    table,
                    [table.email == resp],
                )
                response_object = {"status": "success"}
                return make_response(jsonify(response_object)), 200
            response_object = {"status": "fail", "message": resp}
            return make_response(jsonify(response_object)), 401
        response_object = {
            "status": "fail",
            "message": "Authentication token is missing or invalid.",
        }
        return make_response(jsonify(response_object)), 401

    @instance_method_route("user_authentication_token/<user_group>", methods=["POST"])
    def user_authentication_token(self, user_group):
        """Authentication token route."""
        input_json = request.get_json(force=True)
        table = self.user_group_tables_map[user_group]
        username = input_json["username"]
        password = input_json["password"]
        query_result = make_query(
            table,
            filters=and_(table.username == username),
        ).first()
        if query_result and query_result.check_password(password):
            token = self.encode_auth_token(username, app.config.get("SECRET_KEY"))
            result = jsonify({"token": token})
            result.status_code = 200
        else:
            result = jsonify({})
            result.status_code = 401
        return result
