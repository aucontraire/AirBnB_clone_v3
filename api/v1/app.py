#!/usr/bin/python3
"""Register blueprint"""
from os import getenv
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views


app = Flask(__name__)


app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_down(error):
    """remove the current SQLAlchemy Session"""
    storage.close()


if __name__ == '__main__':
    app.run(
        host=getenv['HBNB_API_HOST'],
        port=getenv['HBNB_API_PORT'],
        threaded=True
    )
