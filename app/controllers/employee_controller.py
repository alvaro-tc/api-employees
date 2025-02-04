from flask import Blueprint, jsonify, request

from models.employee_model import Employee
from models.department_model import Department
from utils.decorators import jwt_required

employee_bp = Blueprint("employee", __name__)


@employee_bp.route("/employees", methods=["GET"])
@jwt_required
def get_employees():
    department_id = request.args.get("department")
    if department_id:
        department = Department.get_by_id(department_id)
        if not department:
            return jsonify({"error": "Departamento no encontrado"}), 404
        employees = Employee.query.filter_by(department_id=department_id).all()
    else:
        employees = Employee.get_all()
    return jsonify([employee.to_dict() for employee in employees]), 200


@employee_bp.route("/employees/<int:id>", methods=["GET"])
@jwt_required
def get_employee(id):
    employee = Employee.get_by_id(id)
    if employee:
        return jsonify(employee.to_dict()), 200
    return jsonify({"error": "Empleado no encontrado"}), 404


@employee_bp.route("/employees", methods=["POST"])
@jwt_required
def create_employee():
    data = request.json
    name = data.get("name")
    lastname = data.get("lastname")
    ci = data.get("ci")
    department_id = data.get("department_id")

    if not name or not lastname or not ci or not department_id:
        return jsonify({"error": "Faltan datos requeridos"}), 400

    department = Department.get_by_id(department_id)
    if not department:
        return jsonify({"error": "Departamento no encontrado"}), 404

    new_employee = Employee(name=name, lastname=lastname, ci=ci, department_id=department_id)
    new_employee.save()

    return jsonify({"message": "Empleado creado exitosamente"}), 201


@employee_bp.route("/employees/<int:id>", methods=["PUT"])
@jwt_required
def update_employee(id):
    data = request.json
    employee = Employee.get_by_id(id)
    if not employee:
        return jsonify({"error": "Empleado no encontrado"}), 404

    name = data.get("name")
    lastname = data.get("lastname")
    ci = data.get("ci")
    department_id = data.get("department_id")

    if department_id:
        department = Department.get_by_id(department_id)
        if not department:
            return jsonify({"error": "Departamento no encontrado"}), 404

    employee.update(name=name, lastname=lastname, ci=ci, department_id=department_id)

    return jsonify({"message": "Empleado actualizado exitosamente"}), 200


@employee_bp.route("/employees/<int:id>", methods=["DELETE"])
@jwt_required
def delete_employee(id):
    employee = Employee.get_by_id(id)
    if not employee:
        return jsonify({"error": "Empleado no encontrado"}), 404

    employee.delete()

    return jsonify({"message": "Empleado eliminado exitosamente"}), 200