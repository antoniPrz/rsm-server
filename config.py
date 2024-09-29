# config.py
import os

class Config:
    # Configuración de la conexión con PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:cilantro@localhost/rsm'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
