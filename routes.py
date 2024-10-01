# routes.py
from flask import Blueprint, jsonify, request
from models import Repair
from app import db
from datetime import datetime

# Crear un Blueprint para las rutas de reparaciones
repair_routes = Blueprint('repair_routes', __name__)

# Ruta para obtener todas las reparaciones
@repair_routes.route('/repairs', methods=['GET'])
def get_repairs():
    repairs = Repair.query.order_by(Repair.order_number.desc()).all()
    results = [
        {
            "id": repair.id,
            "order_number": repair.order_number,
            "device_model": repair.device_model,
            "serial_number": repair.serial_number,
            "reported_issue": repair.reported_issue,
            "status": repair.status,
            "created_at": repair.created_at,
            "updated_at": repair.updated_at,
            "user_id": repair.user_id
        } for repair in repairs
    ]
    return jsonify(results)

# Ruta para obtener una reparación por ID
@repair_routes.route('/repairs/<int:id>', methods=['GET'])
def get_repair(id):
    repair = Repair.query.get(id)
    if repair:
        result = {
            "id": repair.id,
            "device_model": repair.device_model,
            "serial_number": repair.serial_number,
            "reported_issue": repair.reported_issue,
            "status": repair.status,
            "created_at": repair.created_at,
            "updated_at": repair.updated_at,
            "user_id": repair.user_id
        }
        return jsonify(result)
    return jsonify({"error": "Repair not found"}), 404

# Ruta para agregar una nueva reparación
@repair_routes.route('/repairs', methods=['POST'])
def add_repair():
    data = request.get_json()
    new_repair = Repair(
        device_model=data['device_model'],
        serial_number=data['serial_number'],
        reported_issue=data['reported_issue'],
        status=data['status'],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        user_id=data['user_id']
    )
    db.session.add(new_repair)
    db.session.commit()
    return jsonify({"message": "Repair added successfully!"}), 201

# Ruta para actualizar una reparación
@repair_routes.route('/repairs/<int:id>', methods=['PUT'])
def update_repair(id):
    repair = Repair.query.get(id)
    if repair:
        data = request.get_json()
        repair.status = data.get('status', repair.status)
        repair.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "Repair updated successfully!"})
    return jsonify({"error": "Repair not found"}), 404

# Ruta para eliminar una reparación
@repair_routes.route('/repairs/<int:id>', methods=['DELETE'])
def delete_repair(id):
    repair = Repair.query.get(id)
    if repair:
        db.session.delete(repair)
        db.session.commit()
        return jsonify({"message": "Repair deleted successfully!"})
    return jsonify({"error": "Repair not found"}), 404
