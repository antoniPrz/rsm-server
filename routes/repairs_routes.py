# routes/repairs_routes.py
from flask import Blueprint, jsonify, request
from controllers.repairs_controller import get_all_repairs, get_repair_by_id, create_repair, update_repair, delete_repair

repairs_bp = Blueprint('repairs', __name__)

# Obtener todas las reparaciones
@repairs_bp.route('/repairs', methods=['GET'])
def get_repairs():
    repairs = get_all_repairs()
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




# Obtener una reparación por ID
@repairs_bp.route('/repairs/<int:id>', methods=['GET'])
def get_repair(id):
    repair = get_repair_by_id(id)
    if repair:
        result = {
            "id": repair.id,
            "order_number": repair.order_number,
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

# Agregar una nueva reparación
@repairs_bp.route('/repairs', methods=['POST'])
def add_repair():
    data = request.get_json()
    new_repair = create_repair(data)
    return jsonify({
        "message": "Repair added successfully!",
        "id": new_repair.id
    }), 201

# Actualizar una reparación
@repairs_bp.route('/repairs/<int:id>', methods=['PUT'])
def update_repair_route(id):
    data = request.get_json()
    repair = update_repair(id, data)
    if repair:
        return jsonify({"message": "Repair updated successfully!"})
    return jsonify({"error": "Repair not found"}), 404

# Eliminar una reparación
@repairs_bp.route('/repairs/<int:id>', methods=['DELETE'])
def delete_repair_route(id):
    repair = delete_repair(id)
    if repair:
        return jsonify({"message": "Repair deleted successfully!"})
    return jsonify({"error": "Repair not found"}), 404
