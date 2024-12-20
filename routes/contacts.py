from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.contact import Contact
from utils.db import db

# Creación del Blueprint para manejar las rutas relacionadas con contactos
contacts = Blueprint("contacts", __name__)

# Ruta principal que muestra todos los contactos


@contacts.route('/')
def index():
    contacts = Contact.query.all()  # Consulta todos los contactos en la base de datos
    # Renderiza la plantilla 'index.html' con los contactos
    return render_template('index.html', contacts=contacts)

# Ruta para agregar un nuevo contacto


@contacts.route('/new', methods=['POST'])
def add_contact():
    if request.method == 'POST':

        # Recibir datos del formulario
        fullname = request.form['fullname']
        email = request.form['email']
        phone = request.form['phone']

        # Crear un nuevo objeto Contact
        new_contact = Contact(fullname, email, phone)

        # Guardar el objeto en la base de datos
        db.session.add(new_contact)
        db.session.commit()

        flash('¡Contacto agregado exitosamente!')  # Mensaje de éxito

        # Redirigir a la página principal
        return redirect(url_for('contacts.index'))

# Ruta para actualizar un contacto existente


@contacts.route("/update/<string:id>", methods=["GET", "POST"])
def update(id):
    # Obtener el contacto por ID
    contact = Contact.query.get(id)

    if request.method == "POST":
        # Actualizar los datos del contacto con los datos recibidos del formulario
        contact.fullname = request.form['fullname']
        contact.email = request.form['email']
        contact.phone = request.form['phone']

        db.session.commit()  # Guardar los cambios en la base de datos

        flash('¡Contacto actualizado exitosamente!')  # Mensaje de éxito

        # Redirigir a la página principal
        return redirect(url_for('contacts.index'))

    # Renderizar el formulario de actualización
    return render_template("update.html", contact=contact)

# Ruta para eliminar un contacto existente


@contacts.route("/delete/<id>", methods=["GET"])
def delete(id):
    contact = Contact.query.get(id)  # Obtener el contacto por ID
    db.session.delete(contact)  # Eliminar el contacto de la base de datos
    db.session.commit()  # Guardar los cambios

    flash('¡Contacto eliminado exitosamente!')  # Mensaje de éxito

    # Redirigir a la página principal
    return redirect(url_for('contacts.index'))

# Ruta para la página "Acerca de"


@contacts.route("/about")
def about():
    # Renderizar la plantilla "about.html"
    return render_template("about.html")

