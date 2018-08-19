#!/usr/bin/python3
"""Places API routes"""
from models import storage
from flask import jsonify, request
from api.v1.views import app_views
from api.v1.app import not_found
from models.place import Place


@app_views.route(
    '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def show_places(city_id):
    """Shows all places associated with a city
       Args:
           city_id (str): city uuid
       Returns:
           A list of JSON dictionaries of all places in a city
    """
    city = storage.get('City', city_id)
    places_list = []
    if city:
        for place in city.places:
            places_list.append(place.to_dict())
        return jsonify(places_list)
    else:
        return not_found(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def show_place(place_id):
    """Shows place
       Args:
           place_id (str): place uuid
       Returns:
           JSON dictionary of place
    """
    place = storage.get('Place', place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        return not_found(404)


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes place
       Args:
           place_id (str): place uuid
       Returns:
           Empty JSON dictionary if successful otherwise 404 error
    """
    place = storage.get('Place', place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({})
    else:
        return not_found(404)


@app_views.route(
    '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a place
       Args:
           city_id (str): city uuid
       Returns:
           JSON dictionary of place if successful
    """
    city = storage.get('City', city_id)
    error_message = ""
    if city:
        content = request.get_json(silent=True)
        if type(content) is dict:
            if "user_id" in content.keys():
                user = storage.get('User', content['user_id'])
                if user:
                    if "name" in content.keys():
                        place = Place(**content)
                        place.city_id = city_id
                        storage.new(place)
                        storage.save()
                        response = jsonify(place.to_dict())
                        response.status_code = 201
                        return response
                    else:
                        error_message = "Missing name"
                else:
                    return not_found(404)
            else:
                error_message = "Missing user_id"
        else:
            error_message = "Not a JSON"

        response = jsonify({"error": error_message})
        response.status_code = 400
        return response
    else:
        return not_found(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a place
       Args:
           place_id (str): place uuid
       Returns:
           JSON dictionary of place if successful
    """
    place = storage.get('Place', place_id)
    if place:
        content = request.get_json(silent=True)
        if type(content) is dict:
            ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
            for name, value in content.items():
                if name not in ignore:
                    setattr(place, name, value)
            storage.save()
            return jsonify(place.to_dict())

        else:
            response = jsonify({"error": "Not a JSON"})
            response.status_code = 400
            return response
    else:
        return not_found(404)
