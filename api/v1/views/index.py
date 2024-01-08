#!/usr/bin/python3
"""
This module contains endpoint(route) status
"""

from models import storage
from flask import Flask
from api.v1.views import app_view
from flask import jsonify
from flask_cors import cross_origin


@app_view.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Returns a JSON status
    """
    return jsonify({"status": "OK"})