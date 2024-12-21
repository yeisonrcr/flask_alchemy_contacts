from flask import Flask
from routes.contacts import contacts  # Importación del blueprint para las rutas de contactos
from utils.db import db  # Objeto SQLAlchemy inicializado
import os  # Para manejar variables de entorno
from config import DevelopmentConfig, TestingConfig, ProductionConfig  # Configuraciones según el entorno

# Inicializar la aplicación Flask
app = Flask(__name__)

# Determina la configuración basada en el entorno
ENV = os.getenv("FLASK_ENV", "development")  # Por defecto, se asume desarrollo
if ENV == "development":
    app.config.from_object(DevelopmentConfig)
elif ENV == "production":
    app.config.from_object(ProductionConfig)
elif ENV == "testing":
    app.config.from_object(TestingConfig)
else:
    raise ValueError(f"Entorno desconocido: {ENV}")

# Configuración adicional de la aplicación
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Desactiva el sistema de eventos de SQLAlchemy para ahorrar recursos
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Desactiva el caché de archivos estáticos durante el desarrollo

# Inicializar SQLAlchemy con la aplicación Flask
db.init_app(app)

# Registrar el blueprint 'contacts' para modularizar las rutas
app.register_blueprint(contacts)

# Crear las tablas de la base de datos si no existen
# Esto asegura que la estructura esté lista antes de ejecutar la aplicación
with app.app_context():
    db.create_all()

# Punto de entrada para ejecutar la aplicación Flask
if __name__ == '__main__':
    # Determina el modo debug basado en el entorno
    debug_mode = ENV == "development"  # Debug solo en entorno de desarrollo

    # Ejecuta la aplicación
    app.run(debug=debug_mode, host="0.0.0.0")
