#!/usr/bin/python3
"""
User objects and operations handling route.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_get_all():
    """
    All User objects retrieving script
    return: json of all users
    """
    lst_user = []
    user_object = storage.all("User")
    for object in user_object.values():
        lst_user.append(object.to_json())

    return jsonify(lst_user)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_create():
    """
    User route creating script.
    return: new user object
    """
    json_user = request.get_json(silent=True)
    if json_user is None:
        abort(400, 'Not a JSON')
    if "email" not in json_user:
        abort(400, 'Missing email')
    if "password" not in json_user:
        abort(400, 'Missing password')

    user_nw = User(**json_user)
    user_nw.save()
    respns = jsonify(user_nw.to_json())
    respns.status_code = 201

    return respns


@app_views.route("/users/<user_id>",  methods=["GET"], strict_slashes=False)
def user_by_id(user_id):
    """
    User object by specific ID getting script
    param user_id: user object id
    return: user object with the specified id or error
    """

    object_fetched = storage.get("User", str(user_id))

    if object_fetched is None:
        abort(404)

    return jsonify(object_fetched.to_json())


@app_views.route("/users/<user_id>",  methods=["PUT"], strict_slashes=False)
def user_put(user_id):
    """
    User object by specific ID updating script
    param user_id: user object ID
    return: user object and 200 on success, or 400 or 404 on failure
    """
    json_user = request.get_json(silent=True)

    if json_user is None:
        abort(400, 'Not a JSON')

    object_fetched = storage.get("User", str(user_id))

    if object_fetched is None:
        abort(404)

    for key, val in json_user.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(object_fetched, key, val)

    object_fetched.save()

    return jsonify(object_fetched.to_json())


@app_views.route("/users/<user_id>",  methods=["DELETE"], strict_slashes=False)
def user_delete_by_id(user_id):
    """
    Deletes User by id
    param user_id: user object id
    return: empty dictionary with 200 or 404 if not found
    """

    object_fetched = storage.get("User", str(user_id))

    if object_fetched is None:
        abort(404)

    storage.delete(object_fetched)
    storage.save()

    return jsonify({})
