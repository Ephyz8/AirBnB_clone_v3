#!/usr/bin/python3
"""
Script for index
"""

from flask import jsonify
from api.v1.views import app_views

from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    status route:
    return: json response
    """
    data = {"status": "OK"}

    respns = jsonify(data)
    respns.status_code = 200

    return respns


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """
    stats of all objs route
    :return: json of all objs
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    respns = jsonify(data)
    respns.status_code = 200

    return respns
