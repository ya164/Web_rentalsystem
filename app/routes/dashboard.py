from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, Rental, FinancialSummary, Asset
from app.extensions import db
import logging

dashboard_bp = Blueprint('dashboard', __name__)

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dashboard_bp.route('/', methods=['GET'])
@jwt_required()
def dashboard():
  user_id = get_jwt_identity()
  logger.info(f"Dashboard accessed by user ID: {user_id}")

  try:
    user_id = int(user_id)
  except ValueError:
    logger.error("Invalid user ID type")
    return jsonify({"msg": "Invalid token"}), 422

  user = User.query.get(user_id)
  if not user:
    logger.warning(f"User not found with ID: {user_id}")
    return jsonify({"msg": "User not found"}), 404

  # Активні оренди
  active_rentals = Rental.query.filter_by(user_id=user_id, status='Активний').all()
  active_rentals_count = len(active_rentals)
  active_rentals_data = [{
    "id": rental.id,
    "asset_id": rental.asset_id,
    "asset_name": rental.asset.name,
    "user_id": rental.user_id,
    "username": rental.user.username,
    "start_date": rental.rental_date.isoformat(),
    "end_date": rental.end_date.isoformat() if rental.end_date else None,
    "total_cost": float(rental.total_cost) if rental.total_cost else None,
    "status": rental.status
  } for rental in active_rentals]

  # Завершені оренди
  completed_rentals_count = Rental.query.filter_by(user_id=user_id, status='Завершена').count()

  from datetime import datetime, timedelta
  one_month_ago = datetime.utcnow() - timedelta(days=30)
  financial_summary = FinancialSummary.query.filter(
    FinancialSummary.user_id == user_id,
    FinancialSummary.created_at >= one_month_ago
  ).order_by(FinancialSummary.created_at.desc()).first()
  monthly_expenses = float(financial_summary.total_cost) if financial_summary else 0.0

  # Доступні об'єкти оренди
  available_assets = Asset.query.filter_by(status='Доступно').all()
  available_assets_data = [{
    "id": asset.id,
    "name": asset.name,
    "type": asset.type,
    "description": asset.description,
    "status": asset.status,
    "price_per_day": float(asset.price_per_day),
    "created_at": asset.created_at.isoformat(),
    "updated_at": asset.updated_at.isoformat()
  } for asset in available_assets]

  dashboard_data = {
    "user": {
      "username": user.username,
      "email": user.email,
      "is_admin": user.is_admin
    },
    "active_rentals_count": active_rentals_count,
    "monthly_expenses": monthly_expenses,
    "completed_rentals_count": completed_rentals_count,
    "active_rentals": active_rentals_data,
    "available_assets": available_assets_data
  }

  logger.info(f"Dashboard data for user ID {user_id}: {dashboard_data}")
  return jsonify(dashboard_data), 200
