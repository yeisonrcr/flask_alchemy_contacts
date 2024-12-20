from app import app
from utils.db import db

# Crear las tablas de la base de datos si no existen
# Esto asegura que la estructura de la base de datos esté lista antes de ejecutar la aplicación
with app.app_context(): #fuera el if name main
    db.create_all()

# Punto de entrada para ejecutar la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")  # Ejecuta la aplicación en modo debug, accesible desde cualquier IP
