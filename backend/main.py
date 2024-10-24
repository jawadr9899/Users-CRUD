from flask import Flask, request
from routes import (
    get_users,
    post_user,
    update_user,
    get_one_user,
    delete_user,
    invalid_route,
)
from flask_cors import CORS

# create app
app = Flask(__name__)
CORS(app)


# Routes
@app.route("/users", methods=["GET"])
def get():
    if request.method == "GET":
        return get_users(request)
    else:
        return invalid_route()


@app.route("/users", methods=["POST"])
def post():
    if request.method == "POST":
        return post_user(request, [request.get_json()])
    else:
        return invalid_route()


@app.route("/users/<string:id>", methods=["GET", "PUT", "DELETE"])
def put(id: str):
    if request.method == "PUT":
        return update_user(request, id, request.get_json())
    elif request.method == "DELETE":
        return delete_user(request, id)
    elif request.method == "GET":
        return get_one_user(request, id)
    else:
        return invalid_route()


app.run(debug=True, port=3000)
