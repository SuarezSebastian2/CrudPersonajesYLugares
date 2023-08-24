from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import asc

app = Flask(__name__)
CORS(app, origins=['http://127.0.0.1:5500']) # Esto es para que reciba peticiones desde el frontend

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost/PruebaABC'
db = SQLAlchemy(app)

class Location(db.Model):
    __tablename__ = 'lugares'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.Text)
    characters = db.relationship('Character', backref='origin')

class Character(db.Model):
    __tablename__ = 'personajes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    nombre = db.Column(db.String(255))
    edad = db.Column(db.Integer)
    origen_id = db.Column(db.Integer, db.ForeignKey('lugares.id'))

#funcion para encontrar id disponible
def encontrar_id_disponible(model):
    ids_existentes = [record[0] for record in db.session.query(model.id).order_by(asc(model.id)).all()]
    id_disponible = 1
    for id_existente in ids_existentes:
        if id_existente != id_disponible:
            break
        id_disponible += 1
    return id_disponible

@app.route('/character', methods=['POST'])
def add_character():
    data = request.json
    id_disponible = encontrar_id_disponible(Character)
    new_character = Character(id=id_disponible, nombre=data['nombre'], edad=data['edad'], origen_id=data['origen_id'])
    db.session.add(new_character)
    db.session.commit()
    return jsonify({'message': 'Character added'}), 201

@app.route('/characters', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    return jsonify([{'id': character.id, 'nombre': character.nombre, 'edad': character.edad, 'origen_id': character.origen_id} for character in characters])

@app.route('/character/<int:id>', methods=['PUT'])
def update_character(id):
    character = Character.query.get(id)
    data = request.json
    character.nombre = data['nombre']
    character.edad = data['edad']
    character.origen_id = data['origen_id']
    db.session.commit()
    return jsonify({'message': 'Character updated'}), 200

@app.route('/character/<int:id>', methods=['DELETE'])
def delete_character(id):
    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()
    return jsonify({'message': 'Character deleted'}), 200

@app.route('/location', methods=['POST'])
def add_location():
    data = request.json
    id_disponible = encontrar_id_disponible(Location)
    new_location = Location(id=id_disponible, nombre=data['nombre'], descripcion=data['descripcion'])
    db.session.add(new_location)
    db.session.commit()
    return jsonify({'message': 'Location added'}), 201

@app.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    return jsonify([{'id': location.id, 'nombre': location.nombre, 'descripcion': location.descripcion} for location in locations])

@app.route('/location/<int:id>', methods=['PUT'])
def update_location(id):
    location = Location.query.get(id)
    data = request.json
    location.nombre = data['nombre']
    location.descripcion = data['descripcion']
    db.session.commit()
    return jsonify({'message': 'Location updated'}), 200

@app.route('/location/<int:id>', methods=['DELETE'])
def delete_location(id):
    location = Location.query.get(id)
    db.session.delete(location)
    db.session.commit()
    return jsonify({'message': 'Location deleted'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
