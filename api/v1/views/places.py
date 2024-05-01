#!/usr/bin/python3
"""
Place objects and operations handling route
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def places_by_city(city_id):
    """
    Place objects by city retrieving script.
    return: All Places - json file
    """
    lst_plce = []
    object_city = storage.get("City", str(city_id))
    for object in object_city.places:
        lst_plce.append(object.to_json())

    return jsonify(lst_plce)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def place_create(city_id):
    """
    Place route creating script
    return: newly created Place obj
    """
    json_plce = request.get_json(silent=True)
    if json_plce is None:
        abort(400, 'Not a JSON')
    if not storage.get("User", json_plce["user_id"]):
        abort(404)
    if not storage.get("City", city_id):
        abort(404)
    if "user_id" not in json_plce:
        abort(400, 'Missing user_id')
    if "name" not in json_plce:
        abort(400, 'Missing name')

    json_plce["city_id"] = city_id

    place_nw = Place(**json_plce)
    place_nw.save()
    respns = jsonify(place_nw.to_json())
    respns.status_code = 201

    return respns


@app_views.route("/places/<place_id>",  methods=["GET"],
                 strict_slashes=False)
def place_by_id(place_id):
    """
    Place object by specific ID getting script
    param place_id: place object id
    return: place object with the specified id or error
    """

    object_fetched = storage.get("Place", str(place_id))

    if object_fetched is None:
        abort(404)

    return jsonify(object_fetched.to_json())


@app_views.route("/places/<place_id>",  methods=["PUT"],
                 strict_slashes=False)
def place_put(place_id):
    """
    Place object by specific ID updating script
    :param place_id: Place object ID
    :return: Place object and 200 on success, or 400 or 404 on failure
    """
    json_plce = request.get_json(silent=True)

    if json_plce is None:
        abort(400, 'Not a JSON')

    object_fetched = storage.get("Place", str(place_id))

    if object_fetched is None:
        abort(404)

    for k, v in json_plce.items():
        if k not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(object_fetched, k, v)

    object_fetched.save()

    return jsonify(object_fetched.to_json())


@app_views.route("/places/<place_id>",  methods=["DELETE"],
                 strict_slashes=False)
def place_delete_by_id(place_id):
    """
    Deletes Place by id
    param place_id: Place object id
    return: empty dictionary with 200 or 404 if not found
    """

    object_fetched = storage.get("Place", str(place_id))

    if object_fetched is None:
        abort(404)

    storage.delete(object_fetched)
    storage.save()

    return jsonify({})