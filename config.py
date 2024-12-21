from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# Configuración de variables de entorno para credenciales de la base de datos
USER = os.getenv("MYSQL_USER", "ecomycr")  # Nombre de usuario por defecto
PASSWORD = os.getenv("MYSQL_PASSWORD", "zbyj8918")  # Contraseña por defecto
HOST = os.getenv("MYSQL_HOST", "localhost")  # Dirección del host por defecto
DATABASE = os.getenv("MYSQL_DATABASE", "ecomycr")  # Nombre de la base de datos por defecto

# URI de conexión a la base de datos PostgreSQL para producción (si aplica)
POSTGRES_URI = os.getenv(
    "POSTGRES_URI",
    "postgresql://ecomycr:w9M5on5qUPZebxrac9JXMbnfVhE6TCSx@dpg-ctiv2abtq21c73dv4h00-a/ecomycr_ift4"
)

class Config:
    """Configuración base común para todas las configuraciones."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  # Clave secreta con valor por defecto

class DevelopmentConfig(Config):
    """Configuración para el entorno de desarrollo."""
    ENV = 'development'
    SQLALCHEMY_DATABASE_URI = POSTGRES_URI #cambiar en render

class TestingConfig(Config):
    """Configuración para el entorno de pruebas."""
    ENV = 'testing'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Base de datos en memoria

class ProductionConfig(Config):
    """Configuración para el entorno de producción."""
    ENV = 'production'
    SQLALCHEMY_DATABASE_URI = POSTGRES_URI  # Usa PostgreSQL en producción
