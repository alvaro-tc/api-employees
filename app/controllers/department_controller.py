from flask import Blueprint, jsonify, request

from models.department_model import Department
from utils.decorators import jwt_required

department_bp = Blueprint("department", __name__)


@department_bp.route("/departments", methods=["GET"])
@jwt_required
def get_departments():
    departments = Department.get_all()
    return jsonify([department.to_dict() for department in departments]), 200


@department_bp.route("/departments/<int:id>", methods=["GET"])
@jwt_required
def get_department(id):
    department = Department.get_by_id(id)
    if department:
        return jsonify(department.to_dict()), 200
    return jsonify({"error": "Departamento no encontrado"}), 404


@department_bp.route("/departments", methods=["POST"])
@jwt_required
def create_department():
    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    new_department = Department(name=name)
    new_department.save()

    return jsonify({"message": "Departamento creado exitosamente"}), 201


@department_bp.route("/departments/<int:id>", methods=["PUT"])
@jwt_required
def update_department(id):
    data = request.json
    department = Department.get_by_id(id)
    if not department:
        return jsonify({"error": "Departamento no encontrado"}), 404

    name = data.get("name")

    department.update(name=name)

    return jsonify({"message": "Departamento actualizado exitosamente"}), 200


@department_bp.route("/departments/<int:id>", methods=["DELETE"])
@jwt_required
def delete_department(id):
    department = Department.get_by_id(id)
    if not department:
        return jsonify({"error": "Departamento no encontrado"}), 404

    department.delete()

    return jsonify({"message": "Departamento eliminado exitosamente"}), 200