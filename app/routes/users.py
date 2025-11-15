from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import User
from app.utils.decorators import admin_required
import logging

users_bp = Blueprint('users', __name__)

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except ValueError:
        logger.error(f"Invalid user ID type: {user_id}")
        return jsonify({"msg": "Invalid token"}), 422

    user = User.query.get(user_id)
    if not user:
        logger.warning(f"User not found with ID: {user_id}")
        return jsonify({"msg": "User not found"}), 404

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "is_admin": user.is_admin
    }
    logger.info(f"User profile retrieved: {user_data}")
    return jsonify(user_data), 200

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except ValueError:
        logger.error(f"Invalid user ID type: {user_id}")
        return jsonify({"msg": "Invalid token"}), 422

    user = User.query.get(user_id)
    if not user:
        logger.warning(f"User not found with ID: {user_id}")
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()
    if not data:
        logger.warning("No input data provided for profile update")
        return jsonify({"msg": "No input data provided"}), 400

    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    if username:
        existing_user = User.query.filter(User.username == username, User.id != user_id).first()
        if existing_user:
            logger.warning(f"Username already exists: {username}")
            return jsonify({"msg": "Username already exists"}), 409
        user.username = username

    if email:
        existing_user = User.query.filter(User.email == email, User.id != user_id).first()
        if existing_user:
            logger.warning(f"Email already exists: {email}")
            return jsonify({"msg": "Email already exists"}), 409
        user.email = email

    if phone is not None:
        user.phone = phone

    if password:
        user.set_password(password)

    try:
        db.session.commit()
        logger.info(f"User profile updated: {user.id}")
        return jsonify({"msg": "Profile updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating profile: {str(e)}")
        return jsonify({"msg": "Internal server error"}), 500

@users_bp.route('/', methods=['GET'])
@admin_required
def get_all_users():
    users = User.query.all()
    users_data = [{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "is_admin": user.is_admin
    } for user in users]
    logger.info(f"Retrieved {len(users_data)} users")
    return jsonify({"users": users_data}), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        logger.warning(f"User not found with ID: {user_id}")
        return jsonify({"msg": "User not found"}), 404

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "is_admin": user.is_admin
    }
    logger.info(f"Retrieved user: {user_data}")
    return jsonify(user_data), 200

@users_bp.route('/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        logger.warning(f"User not found with ID: {user_id}")
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()
    if not data:
        logger.warning("No input data provided for user update")
        return jsonify({"msg": "No input data provided"}), 400

    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    is_admin = data.get('is_admin')

    if username:
        existing_user = User.query.filter(User.username == username, User.id != user_id).first()
        if existing_user:
            logger.warning(f"Username already exists: {username}")
            return jsonify({"msg": "Username already exists"}), 409
        user.username = username

    if email:
        existing_user = User.query.filter(User.email == email, User.id != user_id).first()
        if existing_user:
            logger.warning(f"Email already exists: {email}")
            return jsonify({"msg": "Email already exists"}), 409
        user.email = email

    if phone is not None:
        user.phone = phone

    if password:
        user.set_password(password)

    if is_admin is not None:
        user.is_admin = bool(is_admin)

    try:
        db.session.commit()
        logger.info(f"User updated: {user.id}")
        return jsonify({"msg": "User updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating user: {str(e)}")
        return jsonify({"msg": "Internal server error"}), 500

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        logger.warning(f"User not found with ID: {user_id}")
        return jsonify({"msg": "User not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        logger.info(f"User deleted: {user.id}")
        return jsonify({"msg": "User deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting user: {e}")
        return jsonify({"msg": "Internal server error"}), 500

@users_bp.route('/<int:user_id>/make_admin', methods=['POST'])
@admin_required
def make_admin(user_id):
    user = User.query.get(user_id)
    if not user:
        logger.warning(f"User not found with ID: {user_id}")
        return jsonify({"msg": "User not found"}), 404

    if user.is_admin:
        logger.info(f"User {user.id} is already an admin")
        return jsonify({"msg": "User is already an admin"}), 400

    user.is_admin = True
    try:
        db.session.commit()
        logger.info(f"User {user.id} has been made an admin")
        return jsonify({"msg": "User has been made an admin"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error making user admin: {e}")
        return jsonify({"msg": "Internal server error"}), 500

@users_bp.route('/<int:user_id>/revoke_admin', methods=['POST'])
@admin_required
def revoke_admin(user_id):
    user = User.query.get(user_id)
    if not user:
        logger.warning(f"User not found with ID: {user_id}")
        return jsonify({"msg": "User not found"}), 404

    if not user.is_admin:
        logger.info(f"User {user.id} is not an admin")
        return jsonify({"msg": "User is not an admin"}), 400

    user.is_admin = False
    try:
        db.session.commit()
        logger.info(f"Admin rights revoked from user {user.id}")
        return jsonify({"msg": "Admin rights revoked from user"}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error revoking admin rights: {e}")
        return jsonify({"msg": "Internal server error"}), 500
