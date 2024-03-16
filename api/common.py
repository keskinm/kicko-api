import enum
from app import app
from database.database import SessionLocal

def delete_row(handling_class, filters):
    session = SessionLocal()
    session.query(handling_class).filter(*filters).delete()
    session.commit()
    session.close()


def add_row(handling_class, content, end_session=True):
    session = SessionLocal()
    instance = handling_class(**content)
    session.add(instance)
    session.commit()
    if not end_session:
        return instance, session
    else:
        session.close()
        return instance


def make_query(handling_class, filters=None, end_session=True, session=None):
    session = session or SessionLocal()
    if filters is not None:
        query_result = session.query(handling_class).filter(filters)
    else:
        query_result = session.query(handling_class).filter()
    if not end_session:
        return query_result, session
    else:
        session.close()
        return query_result


def row_to_dict(row):
    d = {}
    for column in row.__table__.columns:
        v = getattr(row, column.name)
        if v is not None:
            if column.name.endswith("id"):
                v = str(v)
            if isinstance(v, enum.Enum):
                v = v.value
            d[column.name] = v
    return d


def replace(session, table_row, fields):
    for key, value in fields.items():
        setattr(table_row, key, value)
    session.commit()
    session.close()


def unique(handling_class, column_name, filters=None):
    session = SessionLocal()
    if filters is not None:
        providers_table = session.query(handling_class).filter(filters)
    else:
        providers_table = session.query(handling_class).filter()
    _list = list(map(lambda x: getattr(x, column_name), list(providers_table)))
    _unique = list(dict.fromkeys(_list))
    if column_name.endswith("id"):
        _unique = [str(v) for v in _unique]
    session.close()
    return _unique


# def aggregate_by_column(self, column_name, selection=None):
#     unique_column = self.unique(column_name)
#
#     aggregated = {}
#     for item in unique_column:
#         item_aggregated_list = list(self.session.query(User).filter(getattr(self.handling_class, column_name) == item))
#         if selection:
#             item_aggregated_list = list(map(lambda x: getattr(x, selection), item_aggregated_list))
#         aggregated.update({item: item_aggregated_list})
#
#     return aggregated


from flask import jsonify, make_response
from sqlalchemy import and_

from models import decode_auth_token, encode_auth_token


def delete_user(table, auth_header):
    if auth_header:
        print("AUTH TOKEN NON VIDE")
        auth_token = auth_header.split(" ")[1]

        succeed, resp = decode_auth_token(auth_token, app.config.get("SECRET_KEY"))
        if succeed:
            delete_row(
                table,
                [table.email == resp],
            )
            response_object = {"status": "success"}
            return make_response(jsonify(response_object)), 200
        response_object = {"status": "fail", "message": resp}
        return make_response(jsonify(response_object)), 401

    else:
        # @todo Why a double call everytime with the first one here?
        # Find why and then put fail and 401 response status
        response_object = {
            "status": "success",
            "message": "Provide a valid auth token.",
        }
        return make_response(jsonify(response_object)), 200


def get_user(table, auth_header):
    if auth_header:
        print("AUTH TOKEN NON VIDE")
        auth_token = auth_header.split(" ")[1]

        succeed, resp = decode_auth_token(auth_token, app.config.get("SECRET_KEY"))
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

    else:
        # @todo Why a double call everytime with the first one here?
        # Find why and then put fail and 401 response status
        response_object = {
            "status": "success",
            "message": "Provide a valid auth token.",
        }
        return make_response(jsonify(response_object)), 200


def get_token(table, input_json):
    username = input_json["username"]
    password = input_json["password"]
    query_result = make_query(
        table,
        filters=and_(table.username == username),
    ).first()
    if query_result and query_result.check_password(password):
        token = encode_auth_token(username, app.config.get("SECRET_KEY"))
        result = jsonify({"token": token})
        result.status_code = 200
    else:
        result = jsonify({})
        result.status_code = 401
    return result
