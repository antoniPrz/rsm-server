# controllers/repairs_controller.py
from models.repairs import Repair
from app import db

# Obtener todas las reparaciones
def get_all_repairs():
    repairs = Repair.query.order_by(Repair.order_number.desc()).all()
    return repairs

# Obtener una reparación por ID
def get_repair_by_id(id):
    repair = Repair.query.get(id)
    return repair

# Agregar una nueva reparación
def create_repair(data):
    new_repair = Repair(
         order_number=data['order_number'],
        device_model=data['device_model'],
        serial_number=data['serial_number'],
        reported_issue=data['reported_issue'],
        status=data['status'],
        user_id=data['user_id']
    )
    db.session.add(new_repair)
    db.session.commit()
    return new_repair

# Actualizar una reparación
def update_repair(id, data):
    repair = Repair.query.get(id)
    if repair:
        repair.status = data.get('status', repair.status)
        db.session.commit()
    return repair

# Eliminar una reparación
def delete_repair(id):
    repair = Repair.query.get(id)
    if repair:
        db.session.delete(repair)
        db.session.commit()
    return repair
