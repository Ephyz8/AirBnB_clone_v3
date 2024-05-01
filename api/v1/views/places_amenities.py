#!/usr/bin/python3
"""
Place and amenities linking handling route
"""
from flask import jsonify, abort
from os import getenv

from api.v1.views import app_views, storage


@app_views.route("/places/<place_id>/amenities",
                 methods=["GET"],
                 strict_slashes=False)
def amenity_by_place(place_id):
    """
    All amenities of a place getting script
    param place_id: amenity id
    return: all amenities
    """
    object_fetched = storage.get("Place", str(place_id))

    ammenities_all = []

    if object_fetched is None:
        abort(404)

    for object in object_fetched.amenities:
        ammenities_all.append(object.to_json())

    return jsonify(ammenities_all)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"],
                 strict_slashes=False)
def unlink_amenity_from_place(pAnity_id):
    """ unlinking
    Amenity in a place unlinking
    param place_id: place id
    param amenity_id: amenity id
    return: empty dictionary or error
    """
    if not storage.get("Place", str(place_id)):
        abort(404)
    if not storage.get("Amenity", str(amenity_id)):
        abort(404)

    object_fetched = storage.get("Place", place_id)
    found = 0

    for object in object_fetched.amenities:
        if str(object.id) == amenity_id:
            if getenv("HBNB_TYPE_STORAGE") == "db":
                object_fetched.amenities.remove(object)
            else:
                object_fetched.amenity_ids.remove(object.id)
            object_fetched.save()
            found = 1
            break

    if found == 0:
        abort(404)
    else:
        respns = jsonify({})
        respns.status_code = 201
        return respns

@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["POST"],
                 strict_slashes=False)
def link_amenity_to_place(place_id, amenity_id):
    """
    links a amenity with a place
    :param place_id: place id
    :param amenity_id: amenity id
    :return: return Amenity obj added or error
    """

    object_fetched = storage.get("Place", str(place_id))
    object_ammenity = storage.get("Amenity", str(amenity_id))
    amenity_found = None

    if not object_fetched or not object_ammenity:
        abort(404)

    for obj in object_fetched.amenities:
        if str(obj.id) == amenity_id:
            amenity_found = obj
            break

    if amenity_found is not None:
        return jsonify(amenity_found.to_json())

    if getenv("HBNB_TYPE_STORAGE") == "db":
        object_fetched.amenities.append(object_ammenity)
    else:
        object_fetched.amenities = object_ammenity

    object_fetched.save()

    respns = jsonify(object_ammenity.to_json())
    respns.status_code = 201

    return respns
