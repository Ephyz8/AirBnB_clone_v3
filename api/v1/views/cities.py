#!/usr/bin/python3
"""State objects and operations handling route"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def city_by_state(state_id):
    """
    retrieves all City objects from a specific state
    :return: json of all cities in a state or 404 on error
    """
    lst_cty = []
    object_state = storage.get("State", state_id)

    if object_state is None:
        abort(404)
    for obj in object_state.cities:
        lst_cty.append(obj.to_json())

    return jsonify(lst_cty)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def city_create(state_id):
    """
    City route creation script
    param: state_id - state id
    return: new city object
    """
    json_cty = request.get_json(silent=True)
    if json_cty is None:
        abort(400, 'Not a JSON')

    if not storage.get("State", str(state_id)):
        abort(404)

    if "name" not in json_cty:
        abort(400, 'Missing name')

    json_cty["state_id"] = state_id

    city_nw = City(**json_cty)
    city_nw.save()
    respns = jsonify(city_nw.to_json())
    respns.status_code = 201

    return respns


@app_views.route("/cities/<city_id>",  methods=["GET"],
                 strict_slashes=False)
def city_by_id(city_id):
    """
    City object by specific ID
    param city_id: city object id
    return: city object with the specified id or error
    """

    object_fetched = storage.get("City", str(city_id))

    if object_fetched is None:
        abort(404)

    return jsonify(object_fetched.to_json())


@app_views.route("cities/<city_id>",  methods=["PUT"], strict_slashes=False)
def city_put(city_id):
    """
    City object by specific ID
    param city_id: city object ID
    return: city object and 200 on success, or 400 or 404 on failure
    """
    json_cty = request.get_json(silent=True)
    if json_cty is None:
        abort(400, 'Not a JSON')
    object_fetched = storage.get("City", str(city_id))
    if object_fetched is None:
        abort(404)
    for key, val in json_cty.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(object_fetched, key, val)
    object_fetched.save()
    return jsonify(object_fetched.to_json())


@app_views.route("/cities/<city_id>",  methods=["DELETE"],
                 strict_slashes=False)
def city_delete_by_id(city_id):
    """
    Deletes City by id
    param city_id: city object id
    return: empty dictionary with 200 or 404 if not found
    """

    object_fetched = storage.get("City", str(city_id))

    if object_fetched is None:
        abort(404)

    storage.delete(object_fetched)
    storage.save()

    return jsonify({})
