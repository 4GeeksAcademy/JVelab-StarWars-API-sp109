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
from models import db, User, Character, Planet, FavoritePlanet, FavoriteCharacter
from sqlalchemy import select

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():
    all_users = db.session.execute(select(User)).scalars().all()
    result = list(map(lambda characher: characher.serialize(), all_users))

    return result, 200

@app.route('/user/favorites', methods=['GET'])
def get_userfavorites():
    all_favorites_planets = db.session.execute(select(FavoritePlanet)).scalars().all()
    all_favorites_characters = db.session.execute(select(FavoriteCharacter)).scalars().all()

    result1 = [planet.serialize() for planet in all_favorites_planets]
    result2 = [character.serialize() for character in all_favorites_characters]


    return {
        "favorite_planets": result1,
        "favorite_characters": result2
    }, 200

@app.route('/people', methods=['GET'])
def get_characters():
    all_character = db.session.execute(select(Character)).scalars().all()
    result = list(map(lambda characher: characher.serialize(), all_character))

    return result, 200

@app.route('/people', methods=['POST'])
def add_people():
    new_people = request.get_json()

    if new_people is None:
        return 'El cuerpo debe seguir la siguiente estructura, {"name": nombre, "genre": genero, "race": raza, "skin_color": color de piel, "hair_color": color de pelo, "eye_color": color de ojos}', 400
    if 'name' not in new_people:
        return 'Debes especificar name', 400
    if 'genre' not in new_people:
        return 'Debes especificar genero', 400
    if 'race' not in new_people:
        return 'Debes especificar raza', 400
    if 'skin_color' not in new_people:
        return 'Debes especificar color de piel', 400
    if 'hair_color' not in new_people:
        return 'Debes especificar color de pelo', 400
    if 'eye_color' not in new_people:
        return 'Debes especificar color de ojos', 400

    character = Character(
        name=new_people['name'],
        genre=new_people['genre'],
        race=new_people['race'],
        skin_color=new_people['skin_color'],
        hair_color=new_people['hair_color'],
        eye_color=new_people['eye_color']
    )
    db.session.add(character)
    db.session.commit()

    return 'Agregado con exito', 200

@app.route('/planet', methods=['DELETE'])
def delete_people():
    character_for_delete = request.get_json()
    character = db.session.execute(select(Character).where(Character.id == character_for_delete['id'])).scalars().first()

    if character_for_delete is None:
        return 'Debes introducir un cuerpo con la siguiente estructura: {"id": id del personaje a eliminar}', 400
    if character is None:
        return 'No se encuentra el planeta con la id ' + character_for_delete['id'], 400

    db.session.delete(character)
    db.session.commit()

    return 'Personaje eliminado con exito', 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    character = db.session.execute(select(Character).where(Character.id == people_id)).scalars().first()
    
    if character is None:
        return 'No se encuentra el personaje', 400

    return character.serialize(), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_character(people_id):
    user = db.session.execute(select(User)).scalars().first()
    character = db.session.execute(select(Character).where(Character.id == people_id)).scalars().first()

    if character is None:
        return 'No se encuentra el personaje', 400
    
    favorite_character = FavoriteCharacter(user_id=user.id, character_id=character.id)
    db.session.add(favorite_character)
    db.session.commit()

    return 'Agregado con exito', 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_character(people_id):
    favorite_character = db.session.execute(select(FavoriteCharacter).where(FavoriteCharacter.character_id == people_id)).scalars().first()

    if favorite_character is None:
        return 'No se encuentra el personaje', 400
    
    db.session.delete(favorite_character)
    db.session.commit()

    return 'Eliminado con exito', 200

@app.route('/planet', methods=['GET'])
def get_planets():
    all_planet = db.session.execute(select(Planet)).scalars().all()
    result = list(map(lambda characher: characher.serialize(), all_planet))

    return result, 200

@app.route('/planet', methods=['POST'])
def add_planets():
    new_planet = request.get_json()

    if new_planet is None:
        return 'El cuerpo debe seguir la siguiente estructura, {"name": nombre, "climate": clima, "terrain": terreno, "population": poblacion, "mass": gravedad}', 400
    if 'name' not in new_planet:
        return 'Debes especificar name', 400
    if 'climate' not in new_planet:
        return 'Debes especificar clima', 400
    if 'terrain' not in new_planet:
        return 'Debes especificar terreno', 400
    if 'population' not in new_planet:
        return 'Debes especificar poblacion', 400
    if 'mass' not in new_planet:
        return 'Debes especificar gravedad', 400

    planet = Planet(
        name=new_planet['name'],
        climate=new_planet['climate'],
        terrain=new_planet['terrain'],
        population=new_planet['population'],
        mass=new_planet['mass']
    )
    db.session.add(planet)
    db.session.commit()

    return 'Agregado con exito', 200

@app.route('/planet', methods=['DELETE'])
def delete_planet():
    planet_for_delete = request.get_json()
    planet = db.session.execute(select(Planet).where(Planet.id == planet_for_delete['id'])).scalars().first()

    if planet_for_delete is None:
        return 'Debes introducir un cuerpo con la siguiente estructura: {"id": id del planeta a eliminar}', 400
    if planet is None:
        return 'No se encuentra el planeta con la id ' + planet_for_delete['id'], 400

    db.session.delete(planet)
    db.session.commit()

    return 'Planeta eliminado con exito', 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = db.session.execute(select(Planet).where(Planet.id == planet_id)).scalars().first()
    
    if planet is None:
        return 'No se encuentra el planeta', 400

    return planet.serialize(), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user = db.session.execute(select(User)).scalars().first()
    planet = db.session.execute(select(Planet).where(Planet.id == planet_id)).scalars().first()

    if planet is None:
        return 'No se encuentra el planeta', 400

    favorite_planet = FavoritePlanet(user_id=user.id, planet_id=planet.id)
    db.session.add(favorite_planet)
    db.session.commit()

    return 'Agregado con exito', 200

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite_planet= db.session.execute(select(FavoritePlanet).where(FavoritePlanet.planet_id == planet_id)).scalars().first()

    if favorite_planet is None:
        return 'No se encuentra el planeta', 400

    db.session.delete(favorite_planet)
    db.session.commit()

    return 'Eliminado con exito', 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
