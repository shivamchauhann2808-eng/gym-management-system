# Iron Metrics - Gym Management System

A production-style, modular, and scalable **Gym Management System** built with **Flask**, **HTML5**, **Bootstrap 5**, **JavaScript**, and **SQLAlchemy**. 

This system leverages **Flask Blueprints** for organized routing, dynamic database interactions, comprehensive role-based access security, and an athletic dark glassmorphic user interface.

---

## ⚡ Tech Stack

- **Backend Framework**: Flask 3.0.3
- **ORM / Database**: SQLAlchemy (Flask-SQLAlchemy) using SQLite out of the box (with full PostgreSQL support via env switches)
- **Database Migrations**: Flask-Migrate (Alembic)
- **Forms & Validation**: Flask-WTF / WTForms (with CSRF, Length, and Email filters)
- **Session Authentication**: Flask-Login (secure password hashing using Werkzeug `scrypt`)
- **Frontend Styling**: HTML5, Vanilla CSS3 (Custom Dark Athletic theme + Glassmorphism rules), Bootstrap 5, and Bootstrap Icons
- **Visual Trends**: Chart.js via CDN for metric charting
- **Image Processing**: Pillow (for resizing/handling profile photo file uploads)

---

## 📂 Project Structure

```
/e:/GYM MANAGEMENT SYSTEM/
├── .env                  # Secure application configuration values
├── .env.example          # Template environment setup
├── requirements.txt      # Python library dependencies list
├── run.py                # Main system server entrypoint
├── seed.py               # Database recreation & mock stats populator
├── README.md             # Setup guide and operations manual
└── app/
    ├── __init__.py       # Application factory pattern & logging configuration
    ├── config.py         # Configuration loader & system path resolver
    ├── auth/             # Authentication blueprint package
    │   ├── forms.py      # Login WTF forms validation rules
    │   └── routes.py     # Login, Logout and Session controls
    ├── dashboard/        # Admin analytics panel blueprint
    │   └── routes.py     # Metrics math & ChartJS json aggregators
    ├── members/          # Member CRUD actions blueprint
    │   ├── forms.py      # Registration & Modify WTF forms validation
    │   └── routes.py     # Search, Paginated directory & Cascade deletions
    ├── plans/            # Subscription plans CRUD blueprint
    │   ├── forms.py      # Plan creating WTF forms rules
    │   └── routes.py     # Plan management & deletion integrity checks
    ├── member_panel/     # Read-only Gym Member profile dashboard blueprint
    │   └── routes.py     # Profile card loader & expiration check
    ├── models/           # Database Schema package
    │   ├── __init__.py   # Models exporter
    │   ├── user.py       # Authentication credentials table
    │   ├── member.py     # Personal details & dynamic expiration status properties
    │   └── plan.py       # Gym subscription packages (Monthly, Quarterly, Yearly)
    ├── static/           # Static asset assets
    │   ├── css/
    │   │   └── style.css # Neon athletic accents, custom scrollbars, animations
    │   ├── js/
    │   │   └── main.js   # Live image previews, flash fades, and confirm modals
    │   └── uploads/      # Sanitized member profile pictures directory
    ├── templates/        # Jinja2 HTML core files
    │   ├── base.html     # Sidebar/Navbar skeleton & reusable Delete Modal
    │   ├── auth/
    │   │   └── login.html # High-end centered dark glassmorphic login card
    │   ├── dashboard/
    │   │   └── index.html # Cards, Chart.js targets, Recent Registrations table
    │   ├── members/
    │   │   ├── create.html # Drag-drop styled uploader & calendar pickers
    │   │   ├── edit.html
    │   │   ├── list.html   # Search input, paginated grid, delete triggers
    │   │   └── view.html   # Details grid & membership percentage progress bar
    │   ├── plans/
    │   │   ├── form.html   # Plan add/modify controls
    │   │   └── list.html   # Current plans table and subscriber counters
    │   ├── member_panel/
    │   │   └── profile.html # Read-only personal statistics portal for members
    │   └── errors/
    │       ├── 403.html    # Clear permissions barrier error screens
    │       ├── 404.html    # Page not found error screens
    │       └── 500.html    # Internal Server crash error screens
    └── utils/
        ├── __init__.py
        └── decorators.py  # Role guard checks (@admin_required, @member_required)
```

---

## 🔐 Credentials & Roles

Iron Metrics enforces strict **Role-Based Access Control (RBAC)**:

### 1. Super Admin Portal
Accesses metrics dashboard, manages active plans, adds/edits/deletes gym members, and views full analytics profiles.
- **Login Email**: `admin@gym.com`
- **Login Password**: `admin123`

### 2. Gym Member Panel
Enjoys a clean read-only membership summary displaying enrolled subscription durations, active price scales, start/expiry dates, and a dynamic progress bar showcasing days remaining in their current subscription. **Members are blocked from executing data modifications or accessing admin directories.**
- **Seeded Mock Profiles** (10 separate members populated by default):
  - Email: `marcus@gym.com`, `serena@gym.com`, `arnold@gym.com`, `rocky@gym.com`, `usain@gym.com` (etc.)
  - **Login Password** (for all seeded members): `member123`

---

## 🚀 Quick Start Guide

Execute the following commands in order to set up, seed, and run your application:

### Step 1: Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Seed and Initialize Database
Run the helper CLI script to drop existing tables (if any), create fresh SQLite database schemas, set up plans, create the default Super Admin, and populate 10 mock members with diverse subscription states:
```powershell
python seed.py
```

### Step 3: Start the Flask Development Server
Launch the system locally:
```powershell
python run.py
```
Open your browser and navigate to **`http://127.0.0.1:5000/`**. 

---

## 🛡️ Production & Security Safeguards

- **Input Filtering**: Integrated WTF validation guards. Form limits prevent buffer overflows, while Regexp filters sanitize telephone structures.
- **SQLi Defense**: Bound query parameters processed by SQLAlchemy ORM abstract raw statement calls, blocking injection vectors.
- **Password Safety**: Session validations are backed by secure `scrypt` password hashing via Werkzeug, meaning plain password strings are never stored.
- **CSRF Safeguards**: Built-in CSRF token protection is enabled application-wide using `CSRFProtect(app)` and injected into forms and delete modal templates.
- **Asset Integrity**: Old profile photo files are deleted from the server disk storage when a member is deleted or their profile image updated, preventing storage bloat.
