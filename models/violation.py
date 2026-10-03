from datetime import datetime, timezone
from extensions import db


VIOLATION_TYPES = [
    'No Helmet',
    'Overspeeding',
    'Signal Jump',
    'Drunk Driving',
    'No Seat Belt',
    'Illegal Parking',
    'Driving Without License',
    'Wrong Side Driving',
    'Mobile Phone While Driving',
    'Other'
]

PAYMENT_STATUS = ['Unpaid', 'Paid']


class Violation(db.Model):
    __tablename__ = 'violations'

    id = db.Column(db.Integer, primary_key=True)
    challan_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    vehicle_number = db.Column(db.String(20), nullable=False, index=True)
    violation_type = db.Column(db.String(60), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    violation_date = db.Column(db.Date, nullable=False)
    fine_amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(10), nullable=False, default='Unpaid')
    qr_code_filename = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    @staticmethod
    def generate_challan_number():
        """Generate a unique challan number like CHL-2026-00001"""
        year = datetime.now().year
        # Find the last challan for this year
        last = Violation.query.filter(
            Violation.challan_number.like(f'CHL-{year}-%')
        ).order_by(Violation.challan_number.desc()).first()

        if last:
            try:
                seq = int(last.challan_number.split('-')[-1]) + 1
            except (ValueError, IndexError):
                seq = 1
        else:
            seq = 1
        return f'CHL-{year}-{seq:05d}'

    def __repr__(self):
        return f'<Violation {self.challan_number}>'
