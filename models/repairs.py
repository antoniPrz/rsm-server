# models/repairs.py
from extensions import db

class Repair(db.Model):
    __tablename__ = 'repairs'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    device_model = db.Column(db.String(100))
    serial_number = db.Column(db.String(50))
    reported_issue = db.Column(db.Text)
    status = db.Column(db.String(20), default='En progreso')
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    user_id = db.Column(db.Integer)
