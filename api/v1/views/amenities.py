#!/usr/bin/python3
"""
Amenity objects and operations handling route
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """
    Amenity objects retrieving script
    :return: all states - json
    """
    list_ammen = []
    objs = storage.all("Amenity")
    for object in objs.values():
        list_ammen.append(object.to_json())

    return jsonify(list_ammen)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """
    Amenity route:
    return: new amenity object
    """
    json_ammen = request.get_json(silent=True)
    if json_ammen is None:
        abort(400, 'Not a JSON')
    if "name" not in json_ammen:
        abort(400, 'Missing name')

    ammen_new = Amenity(**json_ammen)
    ammen_new.save()
    respns = jsonify(ammen_new.to_json())
    respns.status_code = 201

    return respns


@app_views.route("/amenities/<amenity_id>",  methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """
    Amenity object by specific ID
    :param amenity_id: amenity object id
    :return: state object with the specified id or error
    """

    object_fetched = storage.get("Amenity", str(amenity_id))

    if object_fetched is None:
        abort(404)

    return jsonify(object_fetched.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """
    updates specific Amenity object by ID
    :param amenity_id: amenity object ID
    :return: amenity object and 200 on success, or 400 or 404 on failure
    """
    json_ammen = request.get_json(silent=True)
    if json_ammen is None:
        abort(400, 'Not a JSON')
    object_fetched = storage.get("Amenity", str(amenity_id))
    if object_fetched is None:
        abort(404)
    for key, val in json_ammen.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(object_fetched, key, val)
    object_fetched.save()
    return jsonify(object_fetched.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete_by_id(amenity_id):
    """
    deletes Amenity by id
    :param amenity_id: Amenity object id
    :return: empty dict with 200 or 404 if not found
    """

    object_fetched = storage.get("Amenity", str(amenity_id))

    if object_fetched is None:
        abort(404)

    storage.delete(object_fetched)
    storage.save()

    return jsonify({})
