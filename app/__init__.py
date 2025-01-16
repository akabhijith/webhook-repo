from flask import Flask
from app.routes import webhook
from app.extensions import mongo
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    mongo.init_app(app)
    app.register_blueprint(webhook)
    return app