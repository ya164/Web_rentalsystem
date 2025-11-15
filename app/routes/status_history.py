from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import StatusHistory, Asset
from datetime import datetime

status_history_bp = Blueprint('status_history', __name__)

@status_history_bp.route('/', methods=['POST'])
@jwt_required()
def create_status_history():
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"msg": "Invalid token"}), 422

    data = request.get_json()

    asset_id = data.get('asset_id')
    previous_status = data.get('previous_status')
    new_status = data.get('new_status')

    if not all([asset_id, previous_status, new_status]):
        return jsonify({"msg": "Missing required fields"}), 400

    asset = Asset.query.get(asset_id)
    if not asset:
        return jsonify({"msg": "Asset not found"}), 404

    # Перевірте, чи статус змінюється коректно
    valid_statuses = ['Доступно', 'Зайнято', 'На обслуговуванні']
    if previous_status not in valid_statuses or new_status not in valid_statuses:
        return jsonify({"msg": "Invalid status values"}), 400

    # Зміна статусу об'єкта
    asset.status = new_status

    new_history = StatusHistory(
        asset_id=asset_id,
        previous_status=previous_status,
        new_status=new_status,
        changed_at=datetime.utcnow()
    )

    db.session.add(new_history)
    db.session.commit()

    return jsonify({"msg": "Status history created successfully"}), 201

@status_history_bp.route('/<int:history_id>', methods=['GET'])
@jwt_required()
def get_status_history(history_id):
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"msg": "Invalid token"}), 422

    history = StatusHistory.query.get(history_id)

    if not history:
        return jsonify({"msg": "Status history not found"}), 404

    history_data = {
        "id": history.id,
        "asset_id": history.asset_id,
        "previous_status": history.previous_status,
        "new_status": history.new_status,
        "changed_at": history.changed_at.isoformat()
    }

    return jsonify(history_data), 200

@status_history_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_status_histories():
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"msg": "Invalid token"}), 422

    assets = Asset.query.filter_by(user_id=user_id).all()
    asset_ids = [asset.id for asset in assets]

    histories = StatusHistory.query.filter(StatusHistory.asset_id.in_(asset_ids)).all()
    histories_data = [{
        "id": history.id,
        "asset_id": history.asset_id,
        "previous_status": history.previous_status,
        "new_status": history.new_status,
        "changed_at": history.changed_at.isoformat()
    } for history in histories]

    return jsonify(histories_data), 200

@status_history_bp.route('/<int:history_id>', methods=['PUT'])
@jwt_required()
def update_status_history(history_id):
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"msg": "Invalid token"}), 422

    history = StatusHistory.query.get(history_id)

    if not history:
        return jsonify({"msg": "Status history not found"}), 404

    data = request.get_json()

    previous_status = data.get('previous_status')
    new_status = data.get('new_status')

    if previous_status:
        history.previous_status = previous_status
    if new_status:
        history.new_status = new_status
        # Оновлення статусу об'єкта
        history.asset.status = new_status

    history.changed_at = datetime.utcnow()

    db.session.commit()

    return jsonify({"msg": "Status history updated successfully"}), 200

@status_history_bp.route('/<int:history_id>', methods=['DELETE'])
@jwt_required()
def delete_status_history(history_id):
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"msg": "Invalid token"}), 422

    history = StatusHistory.query.get(history_id)

    if not history:
        return jsonify({"msg": "Status history not found"}), 404

    db.session.delete(history)
    db.session.commit()

    return jsonify({"msg": "Status history deleted successfully"}), 200
