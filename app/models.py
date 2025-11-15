from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)
    is_admin = db.Column(db.Boolean(), nullable=False, default=False)

    financial_summaries = db.relationship('FinancialSummary', back_populates='user', lazy='dynamic')
    rentals = db.relationship('Rental', back_populates='user', lazy='dynamic')
    assets = db.relationship('Asset', back_populates='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class FinancialSummary(db.Model):
    __tablename__ = 'financial_summaries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    period_start = db.Column(db.Date, nullable=False)
    period_end = db.Column(db.Date, nullable=False)
    total_rentals = db.Column(db.Integer, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', back_populates='financial_summaries')


class Asset(db.Model):
    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='Доступно')
    price_per_day = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = db.relationship('User', back_populates='assets')
    rentals = db.relationship('Rental', back_populates='asset', lazy='dynamic')
    status_histories = db.relationship('StatusHistory', back_populates='asset', lazy='dynamic')


class Rental(db.Model):
    __tablename__ = 'rentals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    rental_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    total_cost = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='Активний')

    user = db.relationship('User', back_populates='rentals')
    asset = db.relationship('Asset', back_populates='rentals')
    rental_histories = db.relationship('RentalHistory', back_populates='rental', lazy='dynamic')


class StatusHistory(db.Model):
    __tablename__ = 'status_histories'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    previous_status = db.Column(db.String(50), nullable=False)
    new_status = db.Column(db.String(50), nullable=False)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    asset = db.relationship('Asset', back_populates='status_histories')


class RentalHistory(db.Model):
    __tablename__ = 'rental_histories'

    id = db.Column(db.Integer, primary_key=True)
    rental_id = db.Column(db.Integer, db.ForeignKey('rentals.id'), nullable=False)
    previous_status = db.Column(db.String(50), nullable=False)
    new_status = db.Column(db.String(50), nullable=False)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    rental = db.relationship('Rental', back_populates='rental_histories')
