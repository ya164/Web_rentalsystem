from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Asset, User
from app.utils.decorators import admin_required
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

objects_bp = Blueprint('objects', __name__)

@objects_bp.route('/', methods=['POST'])
@admin_required
def add_asset():
    logger.info("Received request to add a new asset")
    data = request.get_json()
    name = data.get('name')
    type = data.get('type')
    description = data.get('description', '')
    price_per_day = data.get('price_per_day')

    if not name or not type or price_per_day is None:
        logger.warning("Missing required fields in the request")
        return jsonify({"msg": "Name, type, and price_per_day are required"}), 400

    try:
        price_per_day = float(price_per_day)
    except ValueError:
        logger.warning("Invalid price_per_day format")
        return jsonify({"msg": "Invalid price_per_day format"}), 400

    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except ValueError:
        logger.error("Invalid token")
        return jsonify({"msg": "Invalid token"}), 422

    user = User.query.get(user_id)
    if not user or not user.is_admin:
        logger.warning("Unauthorized user attempted to add an asset")
        return jsonify({"msg": "Admins only!"}), 403

    new_asset = Asset(
        name=name,
        type=type,
        description=description,
        status='Доступно',
        price_per_day=price_per_day,
        user_id=user_id
    )
    try:
        db.session.add(new_asset)
        db.session.commit()
        logger.info(f"Asset '{name}' added successfully with ID {new_asset.id}")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding asset: {e}")
        return jsonify({"msg": "Internal server error"}), 500

    return jsonify({"msg": "Asset added successfully", "id": new_asset.id}), 201

@objects_bp.route('/', methods=['GET'])
@jwt_required()
def get_assets():
    logger.info("Received request to get assets")
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except ValueError:
        logger.error("Invalid token")
        return jsonify({"msg": "Invalid token"}), 422

    user = User.query.get(user_id)
    if not user:
        logger.warning(f"User with ID {user_id} not found")
        return jsonify({"msg": "User not found"}), 404

    if user.is_admin:
        assets = Asset.query.all()
    else:
        assets = Asset.query.filter_by(status='Доступно').all()

    assets_data = [{
        "id": asset.id,
        "name": asset.name,
        "type": asset.type,
        "description": asset.description,
        "status": asset.status,
        "price_per_day": float(asset.price_per_day),
        "created_at": asset.created_at.isoformat(),
        "updated_at": asset.updated_at.isoformat()
    } for asset in assets]

    logger.info(f"Returning {len(assets_data)} assets")
    return jsonify(assets_data), 200

@objects_bp.route('/<int:asset_id>', methods=['GET'])
@jwt_required()
def get_asset(asset_id):
    logger.info(f"Received GET request for asset ID {asset_id}")
    asset = Asset.query.get(asset_id)
    if not asset:
        logger.warning(f"Asset with ID {asset_id} not found")
        return jsonify({"msg": "Asset not found"}), 404

    asset_data = {
        "id": asset.id,
        "name": asset.name,
        "type": asset.type,
        "description": asset.description,
        "status": asset.status,
        "price_per_day": float(asset.price_per_day),
        "created_at": asset.created_at.isoformat(),
        "updated_at": asset.updated_at.isoformat()
    }

    logger.info(f"Returning data for asset ID {asset_id}")
    return jsonify(asset_data), 200

@objects_bp.route('/<int:asset_id>', methods=['PUT'])
@admin_required
def update_asset(asset_id):
    logger.info(f"Received request to update asset with ID {asset_id}")
    asset = Asset.query.get(asset_id)
    if not asset:
        logger.warning(f"Asset with ID {asset_id} not found")
        return jsonify({"msg": "Asset not found"}), 404

    data = request.get_json()
    asset.name = data.get('name', asset.name)
    asset.type = data.get('type', asset.type)
    asset.description = data.get('description', asset.description)
    price_per_day = data.get('price_per_day', asset.price_per_day)
    try:
        asset.price_per_day = float(price_per_day)
    except ValueError:
        logger.warning("Invalid price_per_day format")
        return jsonify({"msg": "Invalid price_per_day format"}), 400

    try:
        db.session.commit()
        logger.info(f"Asset with ID {asset_id} updated successfully")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating asset: {e}")
        return jsonify({"msg": "Internal server error"}), 500

    return jsonify({"msg": "Asset updated successfully"}), 200

@objects_bp.route('/<int:asset_id>', methods=['DELETE'])
@admin_required
def delete_asset(asset_id):
    logger.info(f"Received request to delete asset with ID {asset_id}")
    asset = Asset.query.get(asset_id)
    if not asset:
        logger.warning(f"Asset with ID {asset_id} not found")
        return jsonify({"msg": "Asset not found"}), 404

    try:
        db.session.delete(asset)
        db.session.commit()
        logger.info(f"Asset with ID {asset_id} deleted successfully")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting asset: {e}")
        return jsonify({"msg": "Internal server error"}), 500

    return jsonify({"msg": "Asset deleted successfully"}), 200

@objects_bp.route('/<int:asset_id>/maintenance', methods=['POST'])
@admin_required
def set_maintenance(asset_id):
    logger.info(f"Received request to set maintenance for asset ID {asset_id}")
    asset = Asset.query.get(asset_id)
    if not asset:
        logger.warning(f"Asset with ID {asset_id} not found")
        return jsonify({"msg": "Asset not found"}), 404

    if asset.status != 'Доступно':
        logger.warning(f"Cannot set maintenance for asset with status '{asset.status}'")
        return jsonify({"msg": f"Cannot set maintenance for asset with status '{asset.status}'"}), 400

    asset.status = 'На обслуговуванні'
    try:
        db.session.commit()
        logger.info(f"Asset ID {asset_id} status set to 'На обслуговуванні'")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error setting maintenance status: {e}")
        return jsonify({"msg": "Internal server error"}), 500

    return jsonify({"msg": "Asset status set to 'На обслуговуванні'"}), 200

@objects_bp.route('/<int:asset_id>/available', methods=['POST'])
@admin_required
def set_available(asset_id):
    logger.info(f"Received request to set available for asset ID {asset_id}")
    asset = Asset.query.get(asset_id)
    if not asset:
        logger.warning(f"Asset with ID {asset_id} not found")
        return jsonify({"msg": "Asset not found"}), 404

    if asset.status != 'На обслуговуванні':
        logger.warning(f"Cannot set available for asset with status '{asset.status}'")
        return jsonify({"msg": f"Cannot set available for asset with status '{asset.status}'"}), 400

    asset.status = 'Доступно'
    try:
        db.session.commit()
        logger.info(f"Asset ID {asset_id} status set to 'Доступно'")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error setting available status: {e}")
        return jsonify({"msg": "Internal server error"}), 500

    return jsonify({"msg": "Asset status set to 'Доступно'"}), 200
