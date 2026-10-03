import os
from flask import Flask, render_template
from config import config
from extensions import db, login_manager
from models.user import User


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Ensure instance and qrcode directories exist
    os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)
    os.makedirs(app.config['QR_CODE_DIR'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.violations import violations_bp, register_public_routes

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(violations_bp)
    register_public_routes(app)

    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('500.html'), 500

    # Inject current datetime into all templates
    @app.context_processor
    def inject_now():
        from datetime import datetime
        return {'now': datetime.utcnow()}

    # Create tables and seed data
    with app.app_context():
        db.create_all()
        seed_data()

    return app


def seed_data():
    """Create default admin and sample violations if DB is empty."""
    from models.user import User
    from models.violation import Violation
    from datetime import date, datetime, timezone

    # Create default officer account if no users exist
    if not User.query.first():
        admin = User(
            username='officer',
            email='officer@traffic.gov',
        )
        admin.set_password('officer123')
        db.session.add(admin)
        db.session.commit()
        print("[OK] Default account created: username=officer, password=officer123")

    # Create sample violations if none exist
    if not Violation.query.first():
        samples = [
            {
                'vehicle_number': 'TN01AB1234',
                'violation_type': 'No Helmet',
                'location': 'Salem Main Road',
                'violation_date': date(2026, 9, 10),
                'fine_amount': 500.0,
                'payment_status': 'Unpaid',
            },
            {
                'vehicle_number': 'TN01AB1234',
                'violation_type': 'Signal Jump',
                'location': 'Salem Junction',
                'violation_date': date(2026, 9, 15),
                'fine_amount': 1000.0,
                'payment_status': 'Paid',
            },
            {
                'vehicle_number': 'KA05CD5678',
                'violation_type': 'Overspeeding',
                'location': 'Bengaluru Highway',
                'violation_date': date(2026, 9, 20),
                'fine_amount': 2000.0,
                'payment_status': 'Unpaid',
            },
            {
                'vehicle_number': 'MH12EF9012',
                'violation_type': 'Drunk Driving',
                'location': 'Pune City Center',
                'violation_date': date(2026, 9, 25),
                'fine_amount': 5000.0,
                'payment_status': 'Unpaid',
            },
            {
                'vehicle_number': 'DL01GH3456',
                'violation_type': 'Mobile Phone While Driving',
                'location': 'Connaught Place, Delhi',
                'violation_date': date(2026, 10, 1),
                'fine_amount': 1500.0,
                'payment_status': 'Paid',
            },
        ]

        for s in samples:
            challan = Violation.generate_challan_number()
            v = Violation(
                challan_number=challan,
                **s
            )
            db.session.add(v)
            db.session.flush()

            # Generate QR for each sample
            try:
                from utils.qr_generator import generate_qr_code
                from flask import current_app
                base_url = 'http://127.0.0.1:5000'
                qr_file = generate_qr_code(v.id, base_url)
                v.qr_code_filename = qr_file
            except Exception as e:
                print(f"QR generation skipped for sample: {e}")

        db.session.commit()
        print("[OK] Sample violation records created.")


if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)
