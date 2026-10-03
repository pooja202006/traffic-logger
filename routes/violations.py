from datetime import datetime, date
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from extensions import db
from models.violation import Violation, VIOLATION_TYPES
from utils.qr_generator import generate_qr_code, delete_qr_code

violations_bp = Blueprint('violations', __name__, url_prefix='/violations')


@violations_bp.route('/')
@login_required
def list_violations():
    query = Violation.query

    # Search by vehicle number
    vehicle_search = request.args.get('vehicle', '').strip().upper()
    violation_type = request.args.get('violation_type', '').strip()
    payment_status = request.args.get('payment_status', '').strip()
    date_from = request.args.get('date_from', '').strip()
    date_to = request.args.get('date_to', '').strip()

    if vehicle_search:
        query = query.filter(Violation.vehicle_number.ilike(f'%{vehicle_search}%'))
    if violation_type:
        query = query.filter(Violation.violation_type == violation_type)
    if payment_status:
        query = query.filter(Violation.payment_status == payment_status)
    if date_from:
        try:
            df = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(Violation.violation_date >= df)
        except ValueError:
            flash('Invalid "Date From" format.', 'warning')
    if date_to:
        try:
            dt = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(Violation.violation_date <= dt)
        except ValueError:
            flash('Invalid "Date To" format.', 'warning')

    violations = query.order_by(Violation.created_at.desc()).all()

    filters = {
        'vehicle': vehicle_search,
        'violation_type': violation_type,
        'payment_status': payment_status,
        'date_from': date_from,
        'date_to': date_to,
    }

    return render_template('violations.html',
                           violations=violations,
                           violation_types=VIOLATION_TYPES,
                           filters=filters)


@violations_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_violation():
    today = date.today().strftime('%Y-%m-%d')

    if request.method == 'POST':
        vehicle_number = request.form.get('vehicle_number', '').strip().upper()
        violation_type = request.form.get('violation_type', '').strip()
        location = request.form.get('location', '').strip()
        violation_date_str = request.form.get('violation_date', '').strip()
        fine_amount_str = request.form.get('fine_amount', '').strip()

        errors = []

        if not vehicle_number:
            errors.append('Vehicle number is required.')
        if not violation_type or violation_type not in VIOLATION_TYPES:
            errors.append('Please select a valid violation type.')
        if not location:
            errors.append('Location is required.')
        if not violation_date_str:
            errors.append('Violation date is required.')
        else:
            try:
                violation_date = datetime.strptime(violation_date_str, '%Y-%m-%d').date()
            except ValueError:
                errors.append('Invalid date format.')
                violation_date = None

        if not fine_amount_str:
            errors.append('Fine amount is required.')
        else:
            try:
                fine_amount = float(fine_amount_str)
                if fine_amount <= 0:
                    errors.append('Fine amount must be greater than 0.')
            except ValueError:
                errors.append('Fine amount must be a valid number.')
                fine_amount = None

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('add_violation.html',
                                   violation_types=VIOLATION_TYPES,
                                   today=today,
                                   form_data=request.form)

        # Generate unique challan number
        challan_number = Violation.generate_challan_number()

        violation = Violation(
            challan_number=challan_number,
            vehicle_number=vehicle_number,
            violation_type=violation_type,
            location=location,
            violation_date=violation_date,
            fine_amount=fine_amount,
            payment_status='Unpaid'
        )
        db.session.add(violation)
        db.session.flush()  # Get the ID before committing

        # Generate QR code
        try:
            base_url = request.host_url.rstrip('/')
            qr_filename = generate_qr_code(violation.id, base_url)
            violation.qr_code_filename = qr_filename
        except Exception as e:
            current_app.logger.error(f"QR generation error: {e}")

        db.session.commit()

        flash(f'Violation recorded! Challan Number: {challan_number}', 'success')
        return redirect(url_for('violations.view_violation', violation_id=violation.id))

    return render_template('add_violation.html',
                           violation_types=VIOLATION_TYPES,
                           today=today,
                           form_data={})


@violations_bp.route('/<int:violation_id>')
@login_required
def view_violation(violation_id):
    violation = Violation.query.get_or_404(violation_id)
    return render_template('violation_details.html', violation=violation)


@violations_bp.route('/<int:violation_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_violation(violation_id):
    violation = Violation.query.get_or_404(violation_id)

    if request.method == 'POST':
        vehicle_number = request.form.get('vehicle_number', '').strip().upper()
        violation_type = request.form.get('violation_type', '').strip()
        location = request.form.get('location', '').strip()
        violation_date_str = request.form.get('violation_date', '').strip()
        fine_amount_str = request.form.get('fine_amount', '').strip()

        errors = []

        if not vehicle_number:
            errors.append('Vehicle number is required.')
        if not violation_type or violation_type not in VIOLATION_TYPES:
            errors.append('Please select a valid violation type.')
        if not location:
            errors.append('Location is required.')
        if not violation_date_str:
            errors.append('Violation date is required.')
        else:
            try:
                violation_date = datetime.strptime(violation_date_str, '%Y-%m-%d').date()
            except ValueError:
                errors.append('Invalid date format.')
                violation_date = None

        if not fine_amount_str:
            errors.append('Fine amount is required.')
        else:
            try:
                fine_amount = float(fine_amount_str)
                if fine_amount <= 0:
                    errors.append('Fine amount must be greater than 0.')
            except ValueError:
                errors.append('Fine amount must be a valid number.')
                fine_amount = None

        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('edit_violation.html',
                                   violation=violation,
                                   violation_types=VIOLATION_TYPES)

        violation.vehicle_number = vehicle_number
        violation.violation_type = violation_type
        violation.location = location
        violation.violation_date = violation_date
        violation.fine_amount = fine_amount
        violation.updated_at = datetime.utcnow()

        db.session.commit()
        flash('Violation updated successfully!', 'success')
        return redirect(url_for('violations.view_violation', violation_id=violation.id))

    return render_template('edit_violation.html',
                           violation=violation,
                           violation_types=VIOLATION_TYPES)


@violations_bp.route('/<int:violation_id>/delete', methods=['POST'])
@login_required
def delete_violation(violation_id):
    violation = Violation.query.get_or_404(violation_id)
    qr_file = violation.qr_code_filename

    db.session.delete(violation)
    db.session.commit()

    # Delete QR code file
    if qr_file:
        delete_qr_code(qr_file)

    flash('Violation deleted successfully.', 'success')
    return redirect(url_for('violations.list_violations'))


@violations_bp.route('/<int:violation_id>/mark_paid', methods=['POST'])
@login_required
def mark_paid(violation_id):
    violation = Violation.query.get_or_404(violation_id)

    if violation.payment_status == 'Paid':
        flash('This violation is already marked as Paid.', 'info')
    else:
        violation.payment_status = 'Paid'
        violation.updated_at = datetime.utcnow()
        db.session.commit()
        flash(f'Challan {violation.challan_number} marked as Paid!', 'success')

    return redirect(url_for('violations.view_violation', violation_id=violation.id))


@violations_bp.route('/challan/<int:violation_id>')
@login_required
def challan(violation_id):
    violation = Violation.query.get_or_404(violation_id)
    return render_template('challan.html', violation=violation)


@violations_bp.route('/vehicle-search')
@login_required
def vehicle_search():
    vehicle_number = request.args.get('vehicle', '').strip().upper()
    violations = []
    stats = None

    if vehicle_number:
        violations = Violation.query.filter(
            Violation.vehicle_number == vehicle_number
        ).order_by(Violation.violation_date.desc()).all()

        total_fine = sum(v.fine_amount for v in violations)
        paid_fine = sum(v.fine_amount for v in violations if v.payment_status == 'Paid')
        pending_fine = sum(v.fine_amount for v in violations if v.payment_status == 'Unpaid')

        stats = {
            'total_violations': len(violations),
            'total_fine': total_fine,
            'paid_fine': paid_fine,
            'pending_fine': pending_fine,
        }

    return render_template('vehicle_search.html',
                           vehicle_number=vehicle_number,
                           violations=violations,
                           stats=stats)


# Public route - no login required
def register_public_routes(app):
    @app.route('/public/status/<int:violation_id>')
    def public_status(violation_id):
        violation = Violation.query.get_or_404(violation_id)
        return render_template('public_status.html', violation=violation)
