from app import db
from datetime import datetime

# Enumeración para los estados de reparación (opcional, puedes usar solo strings si prefieres)
class EstadoReparacion(db.Enum):
    RECEPCION = "Recepción"
    REVISION = "Revisión"
    DIAGNOSTICO = "Diagnóstico"
    REPARACION = "Reparación"
    EN_PRUEBA = "En Prueba"
    CONTROL_CALIDAD = "Control de Calidad"
    EN_BODEGA = "En Bodega"
    EN_ESPERA = "En Espera"
    POR_RETIRAR = "Por Retirar"

# Modelo Reparaciones (Repair)
class Repair(db.Model):
    __tablename__ = 'repairs'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    device_model = db.Column(db.String(100))
    serial_number = db.Column(db.String(50))
    reported_issue = db.Column(db.Text)
    status = db.Column(db.String(20), default='En progreso')  # Puedes usar 'db.Enum(EstadoReparacion)' si lo defines arriba
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Relación con la tabla 'users'

    # Relación con logs de reparación
    logs = db.relationship('RepairLog', backref='repair', lazy=True)

# Modelo Usuarios (User)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # Puede ser 'admin', 'tecnico', etc.
    created_at = db.Column(db.DateTime, default=db.func.now())

    # Relación con reparaciones
    repairs = db.relationship('Repair', backref='user', lazy=True)

# Modelo Logs de Reparación (RepairLog)
class RepairLog(db.Model):
    __tablename__ = 'repair_logs'
    id = db.Column(db.Integer, primary_key=True)
    repair_id = db.Column(db.Integer, db.ForeignKey('repairs.id'), nullable=False)
    log_entry = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # Opcionalmente podrías tener más detalles aquí, como el técnico que hizo el log
# from app import db
# from datetime import datetime

# # Enumeración para los estados de reparación (opcional, puedes usar solo strings si prefieres)
# class EstadoReparacion(db.Enum):
#     RECEPCION = "Recepción"
#     REVISION = "Revisión"
#     DIAGNOSTICO = "Diagnóstico"
#     REPARACION = "Reparación"
#     EN_PRUEBA = "En Prueba"
#     CONTROL_CALIDAD = "Control de Calidad"
#     EN_BODEGA = "En Bodega"
#     EN_ESPERA = "En Espera"
#     POR_RETIRAR = "Por Retirar"

# # Modelo Reparaciones (Repair)
# class Repair(db.Model):
#     __tablename__ = 'repairs'
#     id = db.Column(db.Integer, primary_key=True)
#     order_number = db.Column(db.String(20), unique=True, nullable=False)
#     device_model = db.Column(db.String(100))
#     serial_number = db.Column(db.String(50))
#     reported_issue = db.Column(db.Text)
#     status = db.Column(db.String(20), default='En progreso')  # Puedes usar 'db.Enum(EstadoReparacion)' si lo defines arriba
#     created_at = db.Column(db.DateTime, default=db.func.now())
#     updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Relación con la tabla 'users'

#     # Relación con logs de reparación
#     logs = db.relationship('RepairLog', backref='repair', lazy=True)

# # Modelo Usuarios (User)
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password_hash = db.Column(db.String(255), nullable=False)
#     role = db.Column(db.String(20), nullable=False)  # Puede ser 'admin', 'tecnico', etc.
#     created_at = db.Column(db.DateTime, default=db.func.now())

#     # Relación con reparaciones
#     repairs = db.relationship('Repair', backref='user', lazy=True)

# # Modelo Logs de Reparación (RepairLog)
# class RepairLog(db.Model):
#     __tablename__ = 'repair_logs'
#     id = db.Column(db.Integer, primary_key=True)
#     repair_id = db.Column(db.Integer, db.ForeignKey('repairs.id'), nullable=False)
#     log_entry = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, default=db.func.now())

#     # Opcionalmente podrías tener más detalles aquí, como el técnico que hizo el log
