from flask import Flask
from routes.contacts import contacts
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_CONNECTION_URI

# Initialize the Flask application
app = Flask(__name__)

# Application settings
# Secret key for session management and other Flask functionalities
app.secret_key = 'mysesdaasdasf34234eqafasfasfasfcret'

# Database configuration
# DATABASE_CONNECTION_URI is imported from the config module
print(DATABASE_CONNECTION_URI)  # Debugging: Prints the database connection URI


app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Disables SQLAlchemy event system to save resources


# Disable caching for static files (useful during development)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Initialize the SQLAlchemy object with the Flask app
SQLAlchemy(app)

# Register the 'contacts' blueprint for modular route management
app.register_blueprint(contacts)
