from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde un archivo .env
load_dotenv()

# Configuración manual de credenciales (se recomienda usar variables de entorno en producción)
user = "ecomycr"  # Nombre de usuario para la base de datos (o usar os.environ["MYSQL_USER"])
password = "zbyj8918"  # Contraseña de la base de datos (o usar os.environ["MYSQL_PASSWORD"])
host = "localhost"  # Dirección del host de la base de datos (o usar os.environ["MYSQL_HOST"])
database = "ecomycr"  # Nombre de la base de datos (o usar os.environ["MYSQL_DATABASE"])

# URI de conexión a la base de datos
# Formato: mysql://usuario:contraseña@host/nombre_base_datos
DATABASE_CONNECTION_URI = f'postgresql://ecomycr:w9M5on5qUPZebxrac9JXMbnfVhE6TCSx@dpg-ctiv2abtq21c73dv4h00-a/ecomycr_ift4'



class Config:
    # Configuraciones comunes
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')  # Define una clave secreta
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desactiva el seguimiento de modificaciones de SQLAlchemy

class DevelopmentConfig(Config):
    ENV = 'development'
    DATABASE_CONNECTION_URI = f'mysql://{user}:{password}@{host}/{database}'  # Configuración MySQL para desarrollo

class TestingConfig(Config):
    ENV = 'testing'
    DATABASE_CONNECTION_URI = 'sqlite:///:memory:'  # Base de datos en memoria para pruebas

class ProductionConfig(Config):
    ENV = 'production'
    DATABASE_CONNECTION_URI = f'mysql://{user}:{password}@{host}/{database}'  # Configuración MySQL para producción
