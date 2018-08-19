#!/usr/bin/python3
"""Register blueprint"""
from os import getenv
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views


app = Flask(__name__)


app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(error):
    """remove the current SQLAlchemy Session"""
    storage.close()


@app.errorhandler(404)
def not_found(message):
    """handles the 404 status code"""
    response = jsonify({'error': 'Not found'})
    response.status_code = 404
    return response


if __name__ == '__main__':
    app.run(
        host=getenv('HBNB_API_HOST', default='0.0.0.0'),
        port=getenv('HBNB_API_PORT', default=5000),
        threaded=True
    )
