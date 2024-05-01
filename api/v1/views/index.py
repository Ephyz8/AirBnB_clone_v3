#!usr/bin/python3
"""Creates Flask app; app_views."""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def api_status():
  """

  """
  resp = {'status': "OK"}
  return jsonify(resp)
