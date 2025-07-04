from flask import Flask
from pymongo import MongoClient

# Replace with your actual MongoDB Atlas connection string
client = MongoClient("mongodb+srv://kowshik:kowshik2002@cluster0.b1qnmhs.mongodb.net/webhookdb?retryWrites=true&w=majority&appName=Cluster0")
db = client['webhookdb']  # Database name

def create_app():
    app = Flask(__name__)

    from .routes import main  # Import routes (Blueprint)
    app.register_blueprint(main)  # Register Blueprint

    return app
