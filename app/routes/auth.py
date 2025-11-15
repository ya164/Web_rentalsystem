from flask import Blueprint, request, jsonify
from app.models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import logging

auth_bp = Blueprint('auth', __name__)

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data:
        logger.warning("No input data provided")
        return jsonify({"msg": "No input data provided"}), 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        logger.warning("Missing required fields")
        return jsonify({"msg": "Username, email, and password are required."}), 400

    # Перевірка, чи вже існує користувач з таким username або email
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        if existing_user.username == username:
            logger.warning(f"Registration attempt with existing username: {username}")
            return jsonify({"msg": "Username already exists."}), 409
        else:
            logger.warning(f"Registration attempt with existing email: {email}")
            return jsonify({"msg": "Email already exists."}), 409

    # Створення нового користувача
    new_user = User(
        username=username,
        email=email,
        is_admin=False
    )
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
        logger.info(f"User registered successfully: {username}")

        # Створення токена доступу
        access_token = create_access_token(identity=str(new_user.id), expires_delta=timedelta(hours=1))

        return jsonify({
            "msg": "User registered successfully.",
            "access_token": access_token
        }), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error during registration: {str(e)}")
        return jsonify({"msg": "Internal server error."}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        logger.info(f"Received login data: {data}")

        if not data:
            logger.warning("No input data provided for login")
            return jsonify({"msg": "No input data provided"}), 400

        username = data.get('username')
        password = data.get('password')

        logger.info(f"Attempting login for user: {username}")

        if not username or not password:
            logger.warning("Missing username or password")
            return jsonify({"msg": "Username and password are required."}), 400

        user = User.query.filter_by(username=username).first()

        if not user:
            logger.warning(f"User not found: {username}")
            return jsonify({"msg": "Invalid credentials."}), 401

        if not user.check_password(password):
            logger.warning(f"Password mismatch for user: {username}")
            return jsonify({"msg": "Invalid credentials."}), 401

        # Створення токена доступу з рядком user_id
        access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
        logger.info(f"Login successful for user: {username}")
        return jsonify({"access_token": access_token}), 200

    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        return jsonify({"msg": "Internal server error."}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    try:
        user_id = get_jwt_identity()
        logger.info(f"Fetching user profile for user ID: {user_id}")

        try:
            user_id = int(user_id)
        except ValueError:
            logger.error(f"Invalid user ID type: {user_id}")
            return jsonify({"msg": "Invalid token."}), 422

        user = User.query.get(user_id)
        if not user:
            logger.warning(f"User not found with ID: {user_id}")
            return jsonify({"msg": "User not found."}), 404

        user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin  # Додано поле is_admin
        }
        logger.info(f"User profile retrieved: {user_data}")
        return jsonify(user_data), 200

    except Exception as e:
        logger.error(f"Error fetching user profile: {str(e)}")
        return jsonify({"msg": "Internal server error."}), 500
