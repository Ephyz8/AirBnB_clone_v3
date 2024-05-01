#!usr/bin/python3
"""Creates Flask app; app_views."""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def api_status():
  """
  Returns JSON response.
  """
  resp = {'status': "OK"}
  return jsonify(resp)
