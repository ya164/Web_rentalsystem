from flask import Flask
from flask_cors import CORS
import logging

from app.extensions import db, migrate, jwt
from app.routes import register_routes

def create_app():
    app = Flask(__name__)

    app.config.from_object('config.Config')

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info("Starting Flask application")

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    with app.app_context():
        from app import models

    # Реєстрація маршрутів
    register_routes(app)

    # Маршрут для головної сторінки
    @app.route('/', methods=['GET'])
    def home():
        return {"message": "Welcome to RentalSystem API"}, 200

    return app
