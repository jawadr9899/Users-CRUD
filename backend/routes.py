from functools import lru_cache
from uuid import uuid4
from flask import Response, jsonify,Request
from api_types import User
from db import init_db

# handle db
db = init_db("database")

#helpers
@lru_cache
def to_dict(record:list[str]) -> dict:
    return dict(zip(db.get_cols(),record))

def hash(data:str):
    import hashlib
    sha256_hash = hashlib.sha256()
    sha256_hash.update(data.encode('utf-8'))
    return sha256_hash.hexdigest()

     
# Handlers
def get_users(_:Request) -> Response:
    try:
        o = [to_dict(r) for r in db.fetch("SELECT * FROM users")]
        if o is not None:
            return jsonify(o)
        return jsonify([])
    except Exception as e:
        print("Error get_users():\n", e)
        res = jsonify({"success": False})
        res.status_code = 500
        return res


def post_user(_:Request, users: list[User]) -> Response:
    try:
        for user in users:
            db.execute_one(f"INSERT INTO users (id,name,email,password) VALUES ('{uuid4().hex}','{user.get("name")}','{user.get("email")}','{hash(user.get("password"))}')")
        return jsonify( {"success":True})
    except Exception as e:
        print("Error post_user():\n", e)
        res = jsonify({"success": False})
        res.status_code = 500
        return res


def update_user(_:Request, id:str,update:User) -> Response:
    try:
        if "password" in update.keys():
            update["password"] = hash(update.get("password"))
        db.execute_one(f"UPDATE users SET ({",".join(update.keys())}) = ({",".join(list(map(lambda v:f"'{v}'",update.values())))})")
        return jsonify({ "success":True })
    except Exception as e:
        print("Error put_user():\n", e)
        res = jsonify({"success": False})
        res.status_code = 500
        return res


def delete_user(_:Request,id:str) -> Response:
    try:
        db.execute_one(f"DELETE FROM users WHERE id = '{id}'")
        return jsonify({ "success":True })
    except Exception as e:
        print("Error delete_user():\n", e)
        res = jsonify({"success": False})
        res.status_code = 500
        return res
    
def get_one_user(_:Request,id:str) -> Response:
    try:
        o = to_dict(db.fetch(f"SELECT * FROM users WHERE id = '{id}'",one=True))
        return jsonify( o|{ "success":True })
    except Exception as e:
        print("Error get_one_user():\n", e)
        res = jsonify({"success": False})
        res.status_code = 500
        return res    

def invalid_route() -> Response:
    res = jsonify({"success:": False})
    res.status_code = 400
    return res
