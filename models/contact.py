from utils.db import db

# Define the Contact model
class Contact(db.Model):
    # Define the fields (columns) of the Contact table
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the Contact table
    fullname = db.Column(db.String(100))          # Column for storing the full name (up to 100 characters)
    email = db.Column(db.String(100))            # Column for storing the email address (up to 100 characters)
    phone = db.Column(db.String(100))            # Column for storing the phone number (up to 100 characters)

    # Constructor for initializing a Contact instance
    def __init__(self, fullname, email, phone):
        self.fullname = fullname  # Assign the provided full name
        self.email = email        # Assign the provided email
        self.phone = phone        # Assign the provided phone number
