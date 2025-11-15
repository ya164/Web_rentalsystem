from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models import FinancialSummary
from datetime import datetime

financial_summary_bp = Blueprint('financial_summary', __name__)

@financial_summary_bp.route('/', methods=['POST'])
@jwt_required()
def create_summary():
    user_id = get_jwt_identity()
    data = request.get_json()

    period_start = data.get('period_start')
    period_end = data.get('period_end')
    total_rentals = data.get('total_rentals')
    total_cost = data.get('total_cost')

    if not all([period_start, period_end, total_rentals, total_cost]):
        return jsonify({"msg": "Missing required fields"}), 400

    try:
        period_start = datetime.fromisoformat(period_start).date()
        period_end = datetime.fromisoformat(period_end).date()
    except ValueError:
        return jsonify({"msg": "Invalid date format"}), 400

    new_summary = FinancialSummary(
        user_id=user_id,
        period_start=period_start,
        period_end=period_end,
        total_rentals=total_rentals,
        total_cost=total_cost
    )

    db.session.add(new_summary)
    db.session.commit()

    return jsonify({"msg": "Financial summary created successfully"}), 201

@financial_summary_bp.route('/<int:summary_id>', methods=['GET'])
@jwt_required()
def get_summary(summary_id):
    user_id = get_jwt_identity()
    summary = FinancialSummary.query.filter_by(id=summary_id, user_id=user_id).first()

    if not summary:
        return jsonify({"msg": "Summary not found"}), 404

    summary_data = {
        "id": summary.id,
        "user_id": summary.user_id,
        "period_start": summary.period_start.isoformat(),
        "period_end": summary.period_end.isoformat(),
        "total_rentals": summary.total_rentals,
        "total_cost": float(summary.total_cost),
        "created_at": summary.created_at.isoformat()
    }

    return jsonify(summary_data), 200

@financial_summary_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_summaries():
    user_id = get_jwt_identity()
    summaries = FinancialSummary.query.filter_by(user_id=user_id).all()
    summaries_data = [{
        "id": summary.id,
        "period_start": summary.period_start.isoformat(),
        "period_end": summary.period_end.isoformat(),
        "total_rentals": summary.total_rentals,
        "total_cost": float(summary.total_cost),
        "created_at": summary.created_at.isoformat()
    } for summary in summaries]

    return jsonify(summaries_data), 200

@financial_summary_bp.route('/<int:summary_id>', methods=['PUT'])
@jwt_required()
def update_summary(summary_id):
    user_id = get_jwt_identity()
    summary = FinancialSummary.query.filter_by(id=summary_id, user_id=user_id).first()

    if not summary:
        return jsonify({"msg": "Summary not found"}), 404

    data = request.get_json()

    period_start = data.get('period_start')
    period_end = data.get('period_end')
    total_rentals = data.get('total_rentals')
    total_cost = data.get('total_cost')

    if period_start:
        try:
            summary.period_start = datetime.fromisoformat(period_start).date()
        except ValueError:
            return jsonify({"msg": "Invalid period_start format"}), 400

    if period_end:
        try:
            summary.period_end = datetime.fromisoformat(period_end).date()
        except ValueError:
            return jsonify({"msg": "Invalid period_end format"}), 400

    if total_rentals is not None:
        summary.total_rentals = total_rentals

    if total_cost is not None:
        summary.total_cost = total_cost

    db.session.commit()

    return jsonify({"msg": "Financial summary updated successfully"}), 200

@financial_summary_bp.route('/<int:summary_id>', methods=['DELETE'])
@jwt_required()
def delete_summary(summary_id):
    user_id = get_jwt_identity()
    summary = FinancialSummary.query.filter_by(id=summary_id, user_id=user_id).first()

    if not summary:
        return jsonify({"msg": "Summary not found"}), 404

    db.session.delete(summary)
    db.session.commit()

    return jsonify({"msg": "Financial summary deleted successfully"}), 200
