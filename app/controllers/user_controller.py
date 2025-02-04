from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from models.user_model import User

user_bp = Blueprint("user", __name__)


@user_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Se requieren nombre de usuario y contraseña"}), 400

    existing_user = User.find_by_username(username)
    if existing_user:
        return jsonify({"error": "El nombre de usuario ya está en uso"}), 400

    new_user = User(username, password)
    new_user.save()

    return jsonify({"message": "Usuario creado exitosamente"}), 201


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = User.find_by_username(username)
    if user and user.check_password(password):
        access_token = create_access_token(identity={"username": username})
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401


@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(user.to_dict()), 200


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    username = data.get("username")
    password = data.get("password")

    if username:
        user.username = username
    if password:
        user.set_password(password)
    user.save()
    return jsonify({"message": "Usuario actualizado exitosamente"}), 200


@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    user.delete()
    return jsonify({"message": "Usuario eliminado exitosamente"}), 200


@user_bp.route("/users", methods=["GET"])
def get_users():
    users = User.get_all()
    return jsonify([user.to_dict() for user in users]), 200