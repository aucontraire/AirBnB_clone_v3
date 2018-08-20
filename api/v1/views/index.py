#!/usr/bin/python3
"""Routing functions"""
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status', methods=['GET'])
def show_status():
    """Shows the status"""
    return jsonify({'status': 'OK'})
