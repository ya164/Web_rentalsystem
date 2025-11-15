from .auth import auth_bp
print("Imported auth_bp")

from .dashboard import dashboard_bp
print("Imported dashboard_bp")

from .financial_summary import financial_summary_bp
print("Imported financial_summary_bp")

from .objects import objects_bp
print("Imported objects_bp")

from .rentals import rentals_bp
print("Imported rentals_bp")

from .status_history import status_history_bp
print("Imported status_history_bp")

from .users import users_bp
print("Imported users_bp")


def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(financial_summary_bp, url_prefix='/financial_summary')
    app.register_blueprint(objects_bp, url_prefix='/objects')
    app.register_blueprint(rentals_bp, url_prefix='/rentals')
    app.register_blueprint(status_history_bp, url_prefix='/status_history')
    app.register_blueprint(users_bp, url_prefix='/users')
