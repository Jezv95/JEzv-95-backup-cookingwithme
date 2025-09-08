"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User,Chef,Utensil,Ingredient,Admin_user
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/chefs', methods=['GET'])
def get_all_chef():
    all_chefs = Chef.query.all()
    results = list(map( lambda chef: chef.serialize(), all_chefs))
    return jsonify(results), 200

@api.route('/chefs/<int:chef_id>', methods=['GET'])
def get_chef(chef_id):
    chef = Chef.query.filter_by(id=chef_id).first()
    if chef is None:
        return {"error-msg":"enter a valid chef"},400
    return jsonify(chef.serialize()), 200

@api.route('/chefs/<int:chef_id>', methods=['DELETE'])
def delete_chef(chef_id):
    chef = Chef.query.filter_by(id=chef_id).first()
    if chef is None:
        return {"error-msg":"enter a valid chef"},400
    db.session.delete(chef)
    db.session.commit()
    response_body = {
        "message": "se elimino el chef " + chef.name
    }

    return jsonify(response_body), 200

@api.route('/chefs', methods=['POST'])
def add_chef():
    body = request.get_json()
    chef = Chef(name=body["name"],email=body["email"],rating=body["rating"], password=body["password"])
    db.session.add(chef)
    db.session.commit()
    response_body = {
        "se creo el chef ": chef.serialize()
    }

    return jsonify(response_body), 200

@api.route('/chefs/<int:chef_id>', methods=['PUT'])
def update_chef(chef_id):
    chef = Chef.query.filter_by(id=chef_id).first()
    if chef is None:
        return {"error-msg":"chef does not exist"},400
    
    body = request.get_json()
    chef.name = body["name"]
    db.session.commit()
    response_body = {
        "message": "chef " + chef.name + " successfully update"
    }

    return jsonify(response_body), 200

@api.route('/recipes', methods=['GET'])
def get_all_recipes():

    response_body = {
            "Recipe": "Neque porro quisquam est qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit..."
        }

    return jsonify(response_body), 200    

@api.route('/utensils', methods=['GET'])
def get_all_utensil():
    all_utensils = Utensil.query.all()
    results = list(map( lambda utensil: utensil.serialize(), all_utensils))
    return jsonify(results), 200

@api.route('/utensils/<int:utensil_id>', methods=['GET'])
def get_utensil(utensil_id):
    utensil = Utensil.query.filter_by(id=utensil_id).first()
    if utensil is None:
        return {"error-msg":"enter a valid utensil"},400
    return jsonify(utensil.serialize()), 200

@api.route('/utensils/<int:utensil_id>', methods=['DELETE'])
def delete_utensil(utensil_id):
    utensil = Utensil.query.filter_by(id=utensil_id).first()
    if utensil is None:
        return {"error-msg":"enter a valid utensil"},400
    db.session.delete(utensil)
    db.session.commit()
    response_body = {
        "message": "se elimino el chef " + utensil.name
    }

    return jsonify(response_body), 200

@api.route('/utensils', methods=['POST'])
def add_utensil():
    body = request.get_json()
    utensil = Utensil(name=body["name"],description=body["description"],url_img=body["url_img"])
    db.session.add(utensil)
    db.session.commit()
    response_body = {
        "se creo el utensilio ": utensil.serialize()
    }

    return jsonify(response_body), 200



@api.route('/utensils/<int:utensil_id>', methods=['PUT'])
def update_utensil(utensil_id):
    utensil = utensil.query.filter_by(id=utensil_id).first()
    if utensil is None:
        return jsonify({"error-msg": "utensil does not exist"}), 404
    
    body = request.get_json()
    utensil.name = body.get("name", utensil.name)
    utensil.description = body.get("description", utensil.description)
    utensil.url_img = body.get("image", utensil.url_img)
    db.session.commit()
    response_body = {
        "message": f"utensil {utensil.id} updated successfully",
        "utensil": utensil.serialize()
    }
    return jsonify(response_body), 200

@api.route('/ingredients', methods=['GET'])
def get_all_ingredients():
    all_ingredients = Ingredient.query.all()
    results = list(map( lambda ingredient: ingredient.serialize(), all_ingredients))
    return jsonify(results), 200

@api.route('/ingredients/<int:ingredient_id>', methods=['GET'])
def get_ingredient(ingredient_id):
    ingredient = Ingredient.query.filter_by(id=ingredient_id).first()
    if ingredient is None:
        return {"error-msg":"enter a valid ingredient"},400
    return jsonify(ingredient.serialize()), 200

@api.route('/ingredients/<int:ingredient_id>', methods=['DELETE'])
def delete_ingredient(ingredient_id):
    ingredient = Ingredient.query.filter_by(id=ingredient_id).first()
    if ingredient is None:
        return {"error-msg":"enter a valid ingredient"},400
    db.session.delete(ingredient)
    db.session.commit()
    response_body = {
        "message": "se elimino el ingredient " + ingredient.name
    }

    return jsonify(response_body), 200

@api.route('/ingredients', methods=['POST'])
def add_ingredient():
    body = request.get_json()
    ingredient = Ingredient(name=body["name"],description=body["description"],image=body["image"])
    db.session.add(ingredient)
    db.session.commit()
    response_body = {
        "se creo el ingredient ": ingredient.serialize()
    }

    return jsonify(response_body), 200


@api.route('/ingredients/<int:ingredient_id>', methods=['PUT'])
def update_ingredient(ingredient_id):
    ingredient = Ingredient.query.filter_by(id=ingredient_id).first()
    if ingredient is None:
        return jsonify({"error-msg": "ingredient does not exist"}), 404
    
    body = request.get_json()
    ingredient.name = body.get("name", ingredient.name)
    ingredient.description = body.get("description", ingredient.description)
    ingredient.image = body.get("image", ingredient.image)
    db.session.commit()
    response_body = {
        "message": f"Ingredient {ingredient.id} updated successfully",
        "ingredient": ingredient.serialize()
    }


    return jsonify(response_body), 200

# #--------Administrador-----------------------

@api.route('/adminuser', methods=['GET'])
def get_all_adminusers():
    all_admins = Admin_user.query.all()
    results = list(map( lambda adminuser: adminuser.serialize(), all_admins))
    return jsonify(results), 200


@api.route('/adminuser/<int:adminuser_id>', methods=['GET'])
def get_admin(adminuser_id):
    admin = Admin_user.query.filter_by(id=adminuser_id).first()
    if admin is None:
        return {"error-msg":"enter a valid admin"},400
    return jsonify(admin.serialize()), 200

@api.route('/adminuser/<int:adminuser_id>', methods=['DELETE'])
def delete_admin(adminuser_id):
    adminuser = Admin_user.query.filter_by(id=adminuser_id).first()
    if adminuser is None:
        return {"error-msg":"enter a valid Admin User"},400
    db.session.delete(adminuser)
    db.session.commit()
    admin_response_body = {
        "message": "se elimino el Admin " + adminuser.email}
    return jsonify(admin_response_body), 200

@api.route('/adminuser', methods=['POST'])
def add_admin():
    admin_body = request.get_json()
    admin = Admin_user(email=admin_body["email"],password=admin_body["password"])
    db.session.add(admin)
    db.session.commit()
    admin_response_body = {
        "Se registro un nuevo administrador": admin.serialize()
    }

    return jsonify(admin_response_body), 200

@api.route('/adminuser/<int:adminuser_id>', methods=['PUT'])
def update_admin(adminuser_id):
    admin = Admin_user.query.filter_by(id=adminuser_id).first()
    if admin is None:
        return jsonify({"error-msg": "admin does not exist"}), 404
    
    admin_body = request.get_json()
    admin.email = admin_body.get("email", admin.email)
    admin.password = admin_body.get("password", admin.password)
    db.session.commit()
    admin_response_body = {
        "message": f"Admin {admin.id} updated successfully",
        "utensil": admin.serialize()
    }

    return jsonify(admin_response_body), 200