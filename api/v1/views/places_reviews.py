#!/usr/bin/python3
"""
Review objects and operations handling route
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def reviews_by_place(place_id):
    """
    All Review objects by place retrieving script
    return: json of all reviews
    """
    lst_review = []
    place_object = storage.get("Place", str(place_id))

    if place_object is None:
        abort(404)

    for object in place_object.reviews:
        lst_review.append(object.to_json())

    return jsonify(lst_review)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def review_create(place_id):
    """
    Create Review route
    return: new Review object
    """
    json_review = request.get_json(silent=True)
    if json_review is None:
        abort(400, 'Not a JSON')
    if not storage.get("Place", place_id):
        abort(404)
    if not storage.get("User", json_review["user_id"]):
        abort(404)
    if "user_id" not in json_review:
        abort(400, 'Missing user_id')
    if "text" not in json_review:
        abort(400, 'Missing text')

    json_review["place_id"] = place_id

    review_nw = Review(**json_review)
    review_nw.save()
    respns = jsonify(review_nw.to_json())
    respns.status_code = 201

    return respns


@app_views.route("/reviews/<review_id>",  methods=["GET"],
                 strict_slashes=False)
def review_by_id(review_id):
    """
    Review object by specific ID getting script
    param review_id: place object id
    return: review object with the specified id or error
    """

    object_fetched = storage.get("Review", str(review_id))

    if object_fetched is None:
        abort(404)

    return jsonify(object_fetched.to_json())


@app_views.route("/reviews/<review_id>",  methods=["PUT"],
                 strict_slashes=False)
def review_put(review_id):
    """
    updates specific Review object by ID
    :param review_id: Review object ID
    :return: Review object and 200 on success, or 400 or 404 on failure
    """
    place_json = request.get_json(silent=True)

    if place_json is None:
        abort(400, 'Not a JSON')

    object_fetched = storage.get("Review", str(review_id))

    if object_fetched is None:
        abort(404)

    for key, val in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id",
                       "place_id"]:
            setattr(object_fetched, key, val)

    object_fetched.save()

    return jsonify(object_fetched.to_json())


@app_views.route("/reviews/<review_id>",  methods=["DELETE"],
                 strict_slashes=False)
def review_delete_by_id(review_id):
    """
    Deletes Review by id
    param : Review object id
    return: empty dictionary with 200 or 404 if not found
    """

    object_fetched = storage.get("Review", str(review_id))

    if object_fetched is None:
        abort(404)

    storage.delete(object_fetched)
    storage.save()

    return jsonify({})
