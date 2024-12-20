## Proyecto de práctica con Fazt Web de youtube
```
git clone https://github.com/FaztWeb/flask-sqlalchemy-crud
cd flask-sqlalchemy-crud
docker-compose up
```
# CRUD de Contactos con Flask
Este proyecto implementa una aplicación web para gestionar contactos utilizando Flask. Incluye funcionalidades CRUD (Crear, Leer, Actualizar, Eliminar) y está estructurado para facilitar la extensión y el mantenimiento del código.

## Características Principales

- **Rutas CRUD**: Gestiona contactos almacenados en una base de datos.
- **Organización con Blueprint**: Las rutas relacionadas con contactos están agrupadas.
- **Mensajes Flash**: Proporciona retroalimentación al usuario.
- **Plantillas HTML**: Renderiza vístas personalizadas.



## Rutas y Funcionalidades

### 1. Ruta Principal (`/`)
Muestra una lista de todos los contactos almacenados en la base de datos.

```python
@contacts.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)
```

---

### 2. Agregar Contacto (`/new`)
Recibe datos de un formulario, crea un nuevo contacto y lo guarda en la base de datos.

```python
@contacts.route('/new', methods=['POST'])
def add_contact():
    fullname = request.form['fullname']
    email = request.form['email']
    phone = request.form['phone']
    new_contact = Contact(fullname, email, phone)
    db.session.add(new_contact)
    db.session.commit()
    flash('¡Contacto agregado exitosamente!')
    return redirect(url_for('contacts.index'))
```

---

### 3. Actualizar Contacto (`/update/<id>`)
Permite modificar los datos de un contacto existente. Si se accede por `POST`, actualiza los datos; si se accede por `GET`, renderiza el formulario.

```python
@contacts.route("/update/<string:id>", methods=["GET", "POST"])
def update(id):
    contact = Contact.query.get(id)
    if request.method == "POST":
        contact.fullname = request.form['fullname']
        contact.email = request.form['email']
        contact.phone = request.form['phone']
        db.session.commit()
        flash('¡Contacto actualizado exitosamente!')
        return redirect(url_for('contacts.index'))
    return render_template("update.html", contact=contact)
```

---

### 4. Eliminar Contacto (`/delete/<id>`)
Elimina un contacto por su ID.

```python
@contacts.route("/delete/<id>", methods=["GET"])
def delete(id):
    contact = Contact.query.get(id)
    db.session.delete(contact)
    db.session.commit()
    flash('¡Contacto eliminado exitosamente!')
    return redirect(url_for('contacts.index'))
```

---

### 5. Página Informativa (`/about`)
Muestra información sobre el proyecto.

```python
@contacts.route("/about")
def about():
    return render_template("about.html")
```

---

## Testing de la Aplicación

El testing asegura que todas las funcionalidades trabajen correctamente. Se utiliza `unittest` para realizar pruebas unitarias.

### Configuración Inicial

Crea un archivo `test_app.py` con la siguiente estructura:

```python
import unittest
from app import app
from utils.db import db

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
```

### Pruebas Unitarias

#### 1. Ruta Principal

```python
def test_index(self):
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Lista de Contactos', response.data)
```

#### 2. Agregar Contacto

```python
def test_add_contact(self):
    response = self.client.post('/new', data={
        'fullname': 'Yeison Example',
        'email': 'yeison@example.com',
        'phone': '1234567890'
    }, follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'¡Contacto agregado exitosamente!', response.data)
```

#### 3. Actualizar Contacto

```python
def test_update_contact(self):
    contact = Contact(fullname='Old Name', email='old@example.com', phone='0000000000')
    db.session.add(contact)
    db.session.commit()

    response = self.client.post(f'/update/{contact.id}', data={
        'fullname': 'Updated Name',
        'email': 'updated@example.com',
        'phone': '1111111111'
    }, follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'¡Contacto actualizado exitosamente!', response.data)
```

#### 4. Eliminar Contacto

```python
def test_delete_contact(self):
    contact = Contact(fullname='To Delete', email='delete@example.com', phone='12345')
    db.session.add(contact)
    db.session.commit()

    response = self.client.get(f'/delete/{contact.id}', follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'¡Contacto eliminado exitosamente!', response.data)
```

### Ejecutar las Pruebas

Ejecuta las pruebas con:

```bash
python -m unittest test_app.py
```

unittest es el módulo estándar de Python para realizar pruebas automatizadas. Permite escribir y ejecutar casos de prueba para garantizar que el código funcione como se espera. Al ejecutarlo con python -m unittest, Python busca y ejecuta todas las pruebas definidas en tu código.

O utilizando `pytest`:

```bash
pytest
```

# Despliegue de Aplicación Flask con PostgreSQL en Render

Este repositorio contiene una aplicación web construida con **Flask** y conectada a una base de datos **PostgreSQL**. Los pasos a continuación explican cómo desplegar la aplicación en **Render.com**.

## 1. Crear la Base de Datos PostgreSQL en Render

1. Inicia sesión en [Render](https://render.com) y accede a tu cuenta.
2. Crea una base de datos PostgreSQL:
   - Haz clic en **"New"** > **"Database"**.
   - Selecciona **PostgreSQL**.
   - Configura los parámetros:
     - **Nombre de la base de datos**: Por ejemplo, `flaskdb`.
     - **Región**: Elige la más cercana.
   - Haz clic en **Create Database**.
3. Copia la URI de conexión que aparece en el panel de configuración de la base de datos:
   - **Internal Database URL**: Se usa si la base de datos y la app están dentro de Render.
   - **External Database URL**: Se usa para conectarse desde fuera de Render.

## 2. Configurar la Aplicación Flask

### Instalar Dependencias

En tu entorno de desarrollo local, instala las dependencias necesarias:

```bash
pip install psycopg2-binary flask-sqlalchemy gunicorn


Configurar SQLAlchemy y la Conexión a la Base de Datos
En tu archivo principal (app.py), configura la conexión a PostgreSQL usando la URI de conexión:

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# URI de conexión a la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/db_name')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definir un modelo de ejemplo
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'

# Ruta de prueba
@app.route('/')
def index():
    return '¡Conexión con PostgreSQL exitosa!'

if __name__ == '__main__':
    app.run(debug=True)


## Explicación

### SQLALCHEMY_DATABASE_URI
Configura la URI para conectar Flask con PostgreSQL. Esto se hace leyendo una variable de entorno llamada `DATABASE_URL`.

SQLALCHEMY_DATABASE_URI: Configura la URI para conectar Flask con PostgreSQL. Esto se hace leyendo una variable de entorno llamada DATABASE_URL.


### Modelo de ejemplo
El modelo `User` es solo un ejemplo para ilustrar cómo puedes interactuar con la base de datos.

Modelo de ejemplo: El modelo User es solo un ejemplo para ilustrar cómo puedes interactuar con la base de datos.
---

## 3. Preparar para Despliegue en Render

### Crear un archivo `requirements.txt`
Este archivo es necesario para que Render sepa qué dependencias instalar:



### Crear el archivo `start` para Render
Este archivo es necesario para indicarle a Render cómo ejecutar tu aplicación:

```bash
gunicorn app:app




## 4. Subir el Proyecto a GitHub

git init
git add .
git commit -m "Primer commit"
git remote add origin https://github.com/tu_usuario/tu_proyecto.git
git push -u origin main


##5. Desplegar en Render

###Crear un Web Service en Render

Ve al panel de control de Render.

Haz clic en "New" > "Web Service".

Selecciona el repositorio de tu proyecto de GitHub.

Configurar el servicio:

Environment: Elige Python.

Build Command: pip install -r requirements.txt.

Start Command: ./start.

Agregar la variable de entorno DATABASE_URL:

Nombre: DATABASE_URL.

Valor: Copia la External Database URL de PostgreSQL en Render (debería verse como postgres://user:password@host.render.com:5432/database_name).

Haz clic en "Create Web Service".

##6. Migrar la Base de Datos
###Una vez que tu aplicación esté desplegada, abre el Web Shell en Render:

Ve al panel de control de tu aplicación.

Haz clic en "Shell".

Ejecuta los comandos de migración en Python.