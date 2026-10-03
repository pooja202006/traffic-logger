import os
import qrcode
from qrcode.image.pure import PyPNGImage
from flask import current_app


def generate_qr_code(violation_id, base_url):
    """
    Generate a QR code for a violation's public status URL.
    Returns the filename of the saved QR code.
    """
    public_url = f"{base_url}/public/status/{violation_id}"
    filename = f"qr_{violation_id}.png"

    qr_dir = current_app.config.get('QR_CODE_DIR',
                                     os.path.join(current_app.root_path, 'static', 'qrcodes'))
    os.makedirs(qr_dir, exist_ok=True)

    filepath = os.path.join(qr_dir, filename)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(public_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filepath)

    return filename


def delete_qr_code(filename):
    """Delete a QR code file if it exists."""
    if not filename:
        return
    try:
        qr_dir = current_app.config.get('QR_CODE_DIR',
                                         os.path.join(current_app.root_path, 'static', 'qrcodes'))
        filepath = os.path.join(qr_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception as e:
        current_app.logger.error(f"Error deleting QR code {filename}: {e}")
