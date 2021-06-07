"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    
    users_alls = User.query.all()

    
    result = list(map(lambda x: x.serialize(), users_alls))

    return jsonify(result), 200

@app.route('/users/<int:id>/favorites', methods=['GET'])
def get_user_favorites(id):
    
    item = User.query.get(id)

    if item is None:
        return jsonify({
                    "Error": "Error"
                }),404

    return jsonify(item.serializeFavorites()), 200

@app.route('/people', methods=['GET'])
def get_people():
    
    people_alls = Character.query.all()
    
    result = list(map(lambda x: x.serialize(), people_alls))

    return jsonify(result), 200

@app.route('/people/<int:id>', methods=['GET'])
def get_people_detail(id):
    
    item = Character.query.get(id)

    if item is None:
        return jsonify({
                    "Error": "Error"
                }),404

    return jsonify(item.serialize()), 200

@app.route('/planets', methods=['GET'])
def get_planets():
    
    planets_alls = Planet.query.all()

    result = list(map(lambda x: x.serialize(), planets_alls))

    return jsonify(result), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet_detail(id):
    
    item = Planet.query.get(id)

    if item is None:
       return jsonify({
                    "Error": "Error"
                }),404

    return jsonify(item.serialize()), 200

@app.route('/users/<int:id>/favorites', methods=['POST'])
def add_favorites(id):
    
    item = User.query.get(id)
    body = request.get_json()

    if item is None:
       return jsonify({
                    "Error": "Error"
                }),404
    if body is None:
        return jsonify({
                    "Error": "Error"
                }),404
    if 'Type' not in body:
       return jsonify({
                    "Error": "Error"
                }),404
    if 'itemID' not in body:
       return jsonify({
                    "Error": "Error"
                }),404
    if(body['Type'] == "Planet"):
        planetid = Planet.query.get(body["itemID"])
        if planetid is None:
            raise APIException('Planet not exists', status_code=404)
        else:
            newFavPlanet = PlanetFavorite(userid = id,planetid = body["itemID"])
            db.session.add(newFavPlanet)
            db.session.commit()
    else:
        characterid = Character.query.get(body["itemID"])
        if characterid is None:
            return jsonify({
                    "Error": "Error"
                }),404
        else:
            newFavPeople = CharacterFavorite(userid = id, characterid = body["itemID"])
            db.session.add(newFavPeople)
            db.session.commit()
            
    return "OK", 200

@app.route('/favorite/<int:id>', methods=['DELETE'])
def remove_favorites(id):
    
    body = request.get_json()

    if body is None:
        return jsonify({
                    "Error": "Error"
                }),404
        
    if 'Type' not in body:
        return jsonify({
                    "Error": "Error"
                }),404

    if body['Type'] != "Planet" and body['Type'] != "Character":
       return jsonify({
                    "Error": "Error"
                }),404

    if(body['Type'] == "Planet"):
        favID = PlanetFavorite.query.get(id)
        if favID is None:
           return jsonify({
                    "Error": "Error"
                }),404
        else:
            db.session.delete(favID)
            db.session.commit()
    else:
        favID = CharacterFavorite.query.get(id)
        if favID is None:
           return jsonify({
                    "Error": "Error"
                }),404
        else:
            db.session.delete(favID)
            db.session.commit()
            
    return jsonify("Task deleted successfully."), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
