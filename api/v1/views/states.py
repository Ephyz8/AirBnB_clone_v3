#!/usr/bin/python3
"""
State objects and operations handling route
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """
    All State objects retrieving script.
    return: json of all states
    """
    list_state = []
    state_object = storage.all("State")
    for object in state_object.values():
        list_state.append(object.to_json())

    return jsonify(list_state)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """
    Create state route
    return: new state object
    """
    json_state = request.get_json(silent=True)
    if json_state is None:
        abort(400, 'Not a JSON')
    if "name" not in json_state:
        abort(400, 'Missing name')

    state_nw = State(**json_state)
    state_nw.save()
    respns = jsonify(state_nw.to_json())
    respns.status_code = 201

    return respns


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    State object by specific ID getting script
    param state_id: state object id
    return: state object with the specified id or error
    """

    object_fetched = storage.get("State", str(state_id))

    if object_fetched is None:
        abort(404)

    return jsonify(object_fetched.to_json())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """
    State object by specific ID updating script
    param state_id: state object ID
    return: state object and 200 on success, or 400 or 404 on failure
    """
    json_state = request.get_json(silent=True)
    if json_state is None:
        abort(400, 'Not a JSON')
    object_fetched = storage.get("State", str(state_id))
    if object_fetched is None:
        abort(404)
    for k, v in json_state.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(object_fetched, k, v)
    object_fetched.save()
    return jsonify(object_fetched.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """
    Deletes State by id
    param state_id: state object id
    return: empty dict with 200 or 404 if not found
    """

    object_fetched = storage.get("State", str(state_id))

    if object_fetched is None:
        abort(404)

    storage.delete(object_fetched)
    storage.save()

    return jsonify({})
