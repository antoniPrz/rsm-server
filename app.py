# app.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_migrate import Migrate 
from datetime import datetime

from config import Config

# Inicializar la app Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar la base de datos
db = SQLAlchemy(app)
migrate = Migrate(app, db) 

# Definir el modelo de la tabla repairs
# class Repair(db.Model):
    # __tablename__ = 'repairs'
    
    # id = db.Column(db.Integer, primary_key=True)
    # device_model = db.Column(db.String(100), nullable=False)
    # serial_number = db.Column(db.String(50), nullable=False)
    # reported_issue = db.Column(db.Text, nullable=False)
    # status = db.Column(db.String(20), nullable=False)
    # created_at = db.Column(db.DateTime, nullable=False)
    # updated_at = db.Column(db.DateTime, nullable=False)
    # user_id = db.Column(db.Integer, nullable=True)  # Si usas foreign key, se debería ajustar

class Repair(db.Model):
    __tablename__ = 'repairs'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)  # Nuevo campo
    device_model = db.Column(db.String(100))
    serial_number = db.Column(db.String(50))
    reported_issue = db.Column(db.Text)
    status = db.Column(db.String(20), default='En progreso')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer)



# Ruta para obtener todas las reparaciones
@app.route('/repairs', methods=['GET'])
def get_repairs():
    # repairs = Repair.query.all()
     # Ordenar las reparaciones por created_at en orden ascendente
    # repairs = Repair.query.order_by(Repair.created_at.asc()).all()
    repairs = Repair.query.order_by(Repair.order_number.desc()).all()
    # Convertir los resultados a formato JSON
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


@app.route('/repairs/<int:id>', methods=['GET'])
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



# ADD NEW repair 

@app.route('/repairs', methods=['POST'])
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


# UPDATE repair 

@app.route('/repairs/<int:id>', methods=['PUT'])
def update_repair(id):
    repair = Repair.query.get(id)
    if repair:
        data = request.get_json()
        repair.status = data.get('status', repair.status)
        repair.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": "Repair updated successfully!"})
    return jsonify({"error": "Repair not found"}), 404


# DELETE repair 

@app.route('/repairs/<int:id>', methods=['DELETE'])
def delete_repair(id):
    repair = Repair.query.get(id)
    if repair:
        db.session.delete(repair)
        db.session.commit()
        return jsonify({"message": "Repair deleted successfully!"})
    return jsonify({"error": "Repair not found"}), 404


# Iniciar la app en modo desarrollo
if __name__ == '__main__':
    app.run(debug=True)
