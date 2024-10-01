# app.py
from flask import Flask
from extensions import db, migrate  # Asegúrate de que esta línea es correcta y que no haya errores tipográficos
from routes.repairs_routes import repairs_bp
from config import Config

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar blueprints (rutas)
    app.register_blueprint(repairs_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
