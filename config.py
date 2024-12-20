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
DATABASE_CONNECTION_URI = f'mysql://{user}:{password}@{host}/{database}'
