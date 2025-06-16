"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for   # La función url_for se usa para generar URLs dinámicamente a partir del nombre de una función de vista (la función que maneja una ruta).
from flask_cors import CORS               
# La extensión flask_cors modifica las respuestas HTTP para incluir los encabezados CORS necesarios.
# Esto permite que tu API Flask pueda ser consumida desde una aplicación frontend que está en otro origen 
# (por ejemplo, un cliente en React que corre en http://localhost:3000 mientras tu backend está en http://localhost:5000). 
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)                               # Habilita CORS para todas las rutas

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def call_all_members():
    # This is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200


@app.route('/members/<int:id>', methods=['GET'])
def obtain_member(id):
    member = jackson_family.get_member(id)
    if member:
        return jsonify(member), 200
    else:
        return jsonify({"error": f"The member is not here! Try again!"}), 404
    

@app.route('/members', methods=['POST'])
def new_member():
    body = request.get_json()
    new_member = jackson_family.add_member(body)
    return jsonify(new_member), 200


@app.route('/members/<int:id>', methods=['DELETE'])
def delete_one_member(id):
    result = jackson_family.delete_member(id)
    if result["done"]:
        return jsonify(result), 200
    else:
        return jsonify({"error": "No se pudo eliminar"}), 404









# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
