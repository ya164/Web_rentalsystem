from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import Rental, Asset, User, FinancialSummary, StatusHistory, RentalHistory
from datetime import datetime, date, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

rentals_bp = Blueprint('rentals', __name__)

@rentals_bp.route('/', methods=['POST'])
@jwt_required()
def create_rental():
    data = request.get_json()
    asset_id = data.get('asset_id')
    start_date_str = data.get('start_date')
    end_date_str = data.get('end_date')

    if not asset_id or not start_date_str or not end_date_str:
        logger.warning("Missing required fields for creating rental")
        return jsonify({"msg": "asset_id, start_date, and end_date are required."}), 400

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    except ValueError:
        logger.warning("Invalid date format")
        return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD."}), 400

    if end_date <= start_date:
        logger.warning("End date must be after start date")
        return jsonify({"msg": "End date must be after start date."}), 400

    asset = Asset.query.get(asset_id)
    if not asset:
        logger.warning(f"Asset with ID {asset_id} not found")
        return jsonify({"msg": "Asset not found."}), 404

    if asset.status != 'Доступно':
        logger.warning(f"Asset {asset_id} is not available for rent")
        return jsonify({"msg": "Asset is not available for rent."}), 400

    duration_days = (end_date - start_date).days
    total_cost = duration_days * asset.price_per_day

    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        logger.error(f"Invalid user_id from JWT: {user_id}")
        return jsonify({"msg": "Invalid user ID."}), 400

    user = User.query.get(user_id)

    if not user:
        logger.warning(f"User with ID {user_id} not found")
        return jsonify({"msg": "User not found."}), 404

    new_rental = Rental(
        asset_id=asset_id,
        user_id=user_id,
        rental_date=start_date,
        end_date=end_date,
        total_cost=total_cost,
        status='Активний'
    )

    try:
        previous_status = asset.status
        asset.status = 'На обслуговуванні'
        status_history = StatusHistory(
            asset_id=asset_id,
            previous_status=previous_status,
            new_status=asset.status,
            changed_at=datetime.utcnow()
        )
        db.session.add(status_history)

        db.session.add(new_rental)

        period_start = date(start_date.year, start_date.month, 1)
        if start_date.month == 12:
            next_month = date(start_date.year + 1, 1, 1)
        else:
            next_month = date(start_date.year, start_date.month + 1, 1)
        period_end = next_month - timedelta(days=1)

        financial_summary = FinancialSummary.query.filter_by(user_id=user_id, period_start=period_start).first()
        if not financial_summary:
            financial_summary = FinancialSummary(
                user_id=user_id,
                period_start=period_start,
                period_end=period_end,
                total_rentals=0,
                total_cost=0.0,
                created_at=datetime.utcnow()
            )
            db.session.add(financial_summary)

        financial_summary.total_cost += total_cost
        financial_summary.total_rentals += 1

        # Додавання запису до RentalHistory
        rental_history = RentalHistory(
            rental_id=new_rental.id,
            previous_status='',
            new_status=new_rental.status,
            changed_at=datetime.utcnow()
        )
        db.session.add(rental_history)

        db.session.commit()
        logger.info(f"Rental created successfully: {new_rental}")
        return jsonify({"msg": "Rental created successfully.", "rental_id": new_rental.id}), 201
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating rental: {e}")
        return jsonify({"msg": "Internal server error."}), 500

@rentals_bp.route('/<int:rental_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_rental(rental_id):
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)  # Конвертація до цілого числа
    except (ValueError, TypeError):
        logger.error(f"Invalid user_id from JWT: {user_id}")
        return jsonify({"msg": "Invalid user ID."}), 400

    rental = Rental.query.get(rental_id)

    if not rental:
        logger.warning(f"Rental with ID {rental_id} not found")
        return jsonify({"msg": "Rental not found."}), 404

    user = User.query.get(user_id)
    if rental.user_id != user_id and not user.is_admin:
        logger.warning(f"User {user_id} unauthorized to cancel rental {rental_id}")
        return jsonify({"msg": "Unauthorized."}), 403

    if rental.status != 'Активний':
        logger.warning(f"Rental {rental_id} is not active and cannot be canceled")
        return jsonify({"msg": "Rental is not active and cannot be canceled."}), 400

    total_cost = rental.total_cost

    try:
        # Оновлення статусу оренди
        previous_status = rental.status
        rental.status = 'Скасована'

        # Оновлення статусу транспорту та додавання запису в StatusHistory
        asset = rental.asset
        previous_asset_status = asset.status
        asset.status = 'Доступно'
        status_history = StatusHistory(
            asset_id=asset.id,
            previous_status=previous_asset_status,
            new_status=asset.status,
            changed_at=datetime.utcnow()
        )
        db.session.add(status_history)

        # Додавання запису до RentalHistory
        rental_history = RentalHistory(
            rental_id=rental.id,
            previous_status=previous_status,
            new_status=rental.status,
            changed_at=datetime.utcnow()
        )
        db.session.add(rental_history)

        # Оновлення FinancialSummary
        period_start = date(rental.rental_date.year, rental.rental_date.month, 1)
        if period_start.month == 12:
            next_month = date(period_start.year + 1, 1, 1)
        else:
            next_month = date(period_start.year, period_start.month + 1, 1)
        period_end = next_month - timedelta(days=1)

        financial_summary = FinancialSummary.query.filter_by(user_id=user_id, period_start=period_start).first()
        if financial_summary:
            financial_summary.total_cost -= total_cost
            financial_summary.total_rentals -= 1
            if financial_summary.total_cost < 0:
                financial_summary.total_cost = 0.0  # Запобігання негативним витратам
            if financial_summary.total_rentals < 0:
                financial_summary.total_rentals = 0
        else:
            logger.warning(f"No FinancialSummary found for user {user_id} and period_start {period_start}")

        db.session.commit()
        logger.info(f"Rental {rental_id} canceled successfully")
        return jsonify({"msg": "Rental canceled successfully."}), 200
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error canceling rental: {e}")
        return jsonify({"msg": "Internal server error."}), 500

@rentals_bp.route('/', methods=['GET'])
@jwt_required()
def get_rentals():
    """
    Отримати список оренд користувача.
    """
    user_id = get_jwt_identity()
    try:
        user_id = int(user_id)  # Конвертація до цілого числа
    except (ValueError, TypeError):
        logger.error(f"Invalid user_id from JWT: {user_id}")
        return jsonify({"msg": "Invalid user ID."}), 400

    user = User.query.get(user_id)

    if not user:
        logger.warning(f"User with ID {user_id} not found")
        return jsonify({"msg": "User not found."}), 404

    if user.is_admin:
        rentals = Rental.query.all()
    else:
        rentals = Rental.query.filter_by(user_id=user_id).all()

    rentals_data = [{
        "id": rental.id,
        "asset_id": rental.asset_id,
        "asset_name": rental.asset.name,
        "user_id": rental.user_id,
        "username": rental.user.username,
        "start_date": rental.rental_date.isoformat(),
        "end_date": rental.end_date.isoformat() if rental.end_date else None,
        "total_cost": float(rental.total_cost) if rental.total_cost else None,
        "status": rental.status
    } for rental in rentals]

    return jsonify(rentals_data), 200
