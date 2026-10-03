from flask import Blueprint, render_template
from flask_login import login_required
from extensions import db
from models.violation import Violation

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    # Statistics
    total_violations = Violation.query.count()
    paid_violations = Violation.query.filter_by(payment_status='Paid').count()
    unpaid_violations = Violation.query.filter_by(payment_status='Unpaid').count()

    total_fine = db.session.query(
        db.func.sum(Violation.fine_amount)
    ).scalar() or 0.0

    collected_fine = db.session.query(
        db.func.sum(Violation.fine_amount)
    ).filter_by(payment_status='Paid').scalar() or 0.0

    pending_fine = db.session.query(
        db.func.sum(Violation.fine_amount)
    ).filter_by(payment_status='Unpaid').scalar() or 0.0

    # Recent violations (last 10)
    recent_violations = Violation.query.order_by(
        Violation.created_at.desc()
    ).limit(10).all()

    stats = {
        'total_violations': total_violations,
        'paid_violations': paid_violations,
        'unpaid_violations': unpaid_violations,
        'total_fine': total_fine,
        'collected_fine': collected_fine,
        'pending_fine': pending_fine,
    }

    return render_template('dashboard.html',
                           stats=stats,
                           recent_violations=recent_violations)
