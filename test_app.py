import unittest
from app import app  # Importa la app Flask principal desde el archivo 'app'
from utils.db import db  # Importa el objeto 'db' que maneja la base de datos
from models.contact import Contact  # Importa el modelo 'Contact' de la base de datos

from config import DATABASE_CONNECTION_URI

class FlaskTestCase(unittest.TestCase):  # Define una clase que hereda de 'unittest.TestCase', para realizar pruebas unitarias

    def setUp(self):
        """
        Este método se ejecuta antes de cada prueba.
        Se configura la app para el entorno de pruebas y la base de datos en memoria.
        """
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
        self.client = app.test_client()  # Crea un cliente de prueba para realizar solicitudes HTTP
        
        # Empujar el contexto de la aplicación antes de interactuar con la base de datos
        with app.app_context():
            db.create_all()  # Crea todas las tablas de la base de datos (en memoria)

    def tearDown(self):
        """
        Este método se ejecuta después de cada prueba.
        Se encarga de limpiar la sesión y eliminar las tablas de la base de datos.
        """
        with app.app_context():
            db.session.remove()  # Elimina la sesión de la base de datos
            db.drop_all()  # Elimina todas las tablas de la base de datos

    # TESTING   Ejecutar prueba con: python -m unittest test_app.py

    # Prueba de la ruta principal
    def test_index(self):
        """
        Prueba que la ruta principal ('/') responda correctamente.
        Se espera que el texto "Lista de Contactos" esté presente en la página.
        """
        response = self.client.get('/')  # Realiza una solicitud GET a la ruta '/'
        
        self.assertEqual(response.status_code, 200)  # Verifica que el código de estado de la respuesta sea 200 (OK)
        
        # Verifica que algún fragmento del HTML esté presente, por ejemplo, una clase o un contenedor
        self.assertIn(b'Agregar Nuevo Contacto', response.data)

    # Prueba para agregar un nuevo contacto
    def test_add_contact(self):
        """
        Prueba que la funcionalidad para agregar un nuevo contacto funcione correctamente.
        Se realiza un POST con datos de un contacto y se espera un mensaje de éxito.
        """
        response = self.client.post('/new', data={  # Realiza un POST a la ruta '/new'
            'fullname': 'Yeison Example',  # Nombre completo del contacto
            'email': 'yeison@example.com',  # Email del contacto
            'phone': '1234567890'  # Teléfono del contacto
        }, follow_redirects=True)  # Sigue las redirecciones automáticas después del POST
        
        self.assertEqual(response.status_code, 200)  # Verifica que la respuesta sea 200 (OK)
        
        # Verifica que el mensaje de éxito esté en la respuesta
        self.assertIn('¡Contacto agregado exitosamente!'.encode('utf-8'), response.data)

    # Prueba para actualizar un contacto existente
    def test_update_contact(self):
        """
        Prueba que la actualización de un contacto existente funcione correctamente.
        Se crea un contacto en la base de datos, luego se actualiza a través de un POST.
        """
        # Empujar el contexto de la aplicación para interactuar con la base de datos
        with app.app_context():
            contact = Contact(fullname='Old Name',  # Crea un contacto inicial
                              email='old@example.com',
                              phone='0000000000')
            db.session.add(contact)  # Añade el contacto a la base de datos
            db.session.commit()  # Guarda los cambios en la base de datos

        # Realiza una solicitud POST para actualizar el contacto creado
        response = self.client.post(f'/update/{contact.id}', data={  # Usamos la ruta '/update/<id>'
            'fullname': 'Updated Name',  # Nombre actualizado
            'email': 'updated@example.com',  # Email actualizado
            'phone': '1111111111'  # Teléfono actualizado
        }, follow_redirects=True)  # Sigue las redirecciones después del POST
        
        self.assertEqual(response.status_code, 200)  # Verifica que la respuesta sea 200 (OK)
        
        # Verifica que el mensaje de éxito esté en la respuesta
        self.assertIn('¡Contacto actualizado exitosamente!'.encode('utf-8'), response.data)

    # Prueba para eliminar un contacto existente
    def test_delete_contact(self):
        """
        Prueba que la eliminación de un contacto funcione correctamente.
        Se crea un contacto en la base de datos y luego se elimina a través de una solicitud GET.
        """
        # Empujar el contexto de la aplicación para interactuar con la base de datos
        with app.app_context():
            contact = Contact(fullname='To Delete',  # Crea un contacto inicial
                              email='delete@example.com',
                              phone='12345')
            db.session.add(contact)  # Añade el contacto a la base de datos
            db.session.commit()  # Guarda los cambios en la base de datos

        # Realiza una solicitud GET para eliminar el contacto
        response = self.client.get(f'/delete/{contact.id}', follow_redirects=True)  # Usa la ruta '/delete/<id>'
        
        self.assertEqual(response.status_code, 200)  # Verifica que la respuesta sea 200 (OK)
        
        # Verifica que el mensaje de éxito esté en la respuesta
        self.assertIn('¡Contacto eliminado exitosamente!'.encode('utf-8'), response.data)


if __name__ == "__main__":
    unittest.main()  # Ejecuta las pruebas cuando se corre el script directamente
