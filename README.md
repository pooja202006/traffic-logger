# 🚦 Smart Traffic Violation Logger

A **complete, production-style** Flask web application for traffic police officers to digitally record, manage, search, and generate challans for traffic violations — with QR code integration and public payment status pages.

---

## 🌟 Features

- ✅ **Secure Officer Authentication** (login, register, logout via Flask-Login)
- ✅ **Dashboard** with live statistics (total/paid/unpaid violations, fine amounts)
- ✅ **Add Violation** with auto-generated unique challan number (`CHL-2026-00001`)
- ✅ **Violation History** with server-side search & multi-filter
- ✅ **Vehicle Search** — look up all violations by vehicle number
- ✅ **QR Code Generation** — unique QR per challan
- ✅ **Public Status Page** — scan QR to see violation status (no login needed)
- ✅ **Digital Challan** with print support (CSS print media)
- ✅ **Mark as Paid** — one-click status update
- ✅ **Edit & Delete** violations
- ✅ **Fully Responsive** Bootstrap 5 UI with dark police/government theme
- ✅ **Sample Data** pre-loaded for testing

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3, Flask 3.0 |
| Database | SQLite + SQLAlchemy |
| Auth | Flask-Login + Werkzeug hashing |
| QR Codes | qrcode + Pillow |
| Frontend | Bootstrap 5 + Vanilla CSS + JavaScript |
| Templates | Jinja2 |

---

## 📁 Project Structure

```
flask mini1/
├── app.py                   # App factory + seeding
├── config.py                # Configuration classes
├── extensions.py            # db, login_manager
├── requirements.txt
├── .env.example
├── .gitignore
│
├── models/
│   ├── user.py              # User model
│   └── violation.py         # Violation model
│
├── routes/
│   ├── auth.py              # /login, /register, /logout
│   ├── dashboard.py         # /dashboard
│   └── violations.py        # All violation routes + /public/status
│
├── utils/
│   └── qr_generator.py      # QR code generation utility
│
├── templates/
│   ├── base.html            # Base layout with navbar
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── add_violation.html
│   ├── edit_violation.html
│   ├── violations.html      # List with filters
│   ├── violation_details.html
│   ├── vehicle_search.html
│   ├── challan.html         # Printable challan
│   ├── public_status.html   # QR scan public page
│   ├── 404.html
│   └── 500.html
│
├── static/
│   ├── css/style.css
│   ├── js/script.js
│   └── qrcodes/             # QR PNG files
│
└── instance/
    └── traffic.db           # SQLite database (auto-created)
```

---

## 🚀 Installation & Setup

### 1. Clone / Navigate to Project

```bash
cd "flask mini1"
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables (Optional)

```bash
copy .env.example .env
# Edit .env and set your SECRET_KEY
```

### 5. Run the Application

```bash
python app.py
```

The app will automatically:
- Create the SQLite database (`instance/traffic.db`)
- Create tables
- Create a default officer account
- Load 5 sample violations

---

## 🌐 Application URL

```
http://127.0.0.1:5000
```

---

## 🔐 Default Login Credentials

| Field | Value |
|-------|-------|
| Username | `officer` |
| Password | `officer123` |

> ⚠️ **Change this before any real deployment!**

---

## 🗺️ Main Routes

| URL | Description | Auth Required |
|-----|-------------|:---:|
| `/` | Redirect to dashboard | ✅ |
| `/login` | Officer login | ❌ |
| `/register` | Register new officer | ❌ |
| `/logout` | Logout | ✅ |
| `/dashboard` | Statistics + recent violations | ✅ |
| `/violations/` | All violations + search/filter | ✅ |
| `/violations/add` | Add new violation | ✅ |
| `/violations/<id>` | Violation details | ✅ |
| `/violations/<id>/edit` | Edit violation | ✅ |
| `/violations/<id>/delete` | Delete violation (POST) | ✅ |
| `/violations/<id>/mark_paid` | Mark as paid (POST) | ✅ |
| `/violations/challan/<id>` | Printable challan | ✅ |
| `/violations/vehicle-search` | Search by vehicle number | ✅ |
| `/public/status/<id>` | **Public QR scan page** | ❌ |

---

## 📱 QR Code Feature

Every violation automatically generates a QR code stored in `static/qrcodes/`.

The QR contains the URL:
```
http://127.0.0.1:5000/public/status/<violation_id>
```

Anyone scanning the QR sees the **Public Status Page** showing:
- Challan number
- Vehicle number
- Violation type & location
- Fine amount
- **PAID** / **UNPAID** status

No login required for the public page.

---

## 🧪 Sample Data

5 violations are pre-loaded:

| Vehicle | Violation | Status |
|---------|-----------|--------|
| TN01AB1234 | No Helmet | Unpaid |
| TN01AB1234 | Signal Jump | Paid |
| KA05CD5678 | Overspeeding | Unpaid |
| MH12EF9012 | Drunk Driving | Unpaid |
| DL01GH3456 | Mobile Phone While Driving | Paid |

---

## 🔍 Search & Filter

On the Violation History page (`/violations/`), you can filter by:
- Vehicle Number (partial match)
- Violation Type
- Payment Status (Paid / Unpaid)
- Date From
- Date To

All filters are applied via **SQLAlchemy database queries**, not frontend JS.

---

## 🖨️ Printing Challans

Navigate to `/violations/challan/<id>` and click **Print Challan**.  
The browser's print dialog opens. Only the challan is printed (other UI is hidden via CSS).

---

## 🔒 Security

- Passwords hashed with **Werkzeug PBKDF2-SHA256**
- All officer routes protected with `@login_required`
- CSRF protection via Flask-WTF
- No raw SQL — SQLAlchemy ORM only
- No sensitive data exposed on the public status page

---

## 📸 Screenshots Section

_Add screenshots of:_
- Dashboard
- Add Violation form
- Violation History with filters
- Challan page
- Public QR Status page

---

## 🔮 Future Enhancements

- PDF export of challans
- Online payment gateway integration
- SMS notifications for violators
- Multi-officer department management
- Analytics charts (violation trends)
- Mobile app with camera QR scanner

---

## 📄 License

For educational/college project use. MIT License.
