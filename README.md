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

O utilizando `pytest`:

```bash
pytest
```

