## 📘 QR Code Based Student Attendance System

A **production-ready, secure, and scalable** student attendance system using dynamic QR codes, GPS validation, and device binding. Built with **Flask (Python)** and **MySQL** for backend, this system allows an **Admin** to generate time-sensitive QR codes which students can scan (via a mobile app or web interface) to mark their attendance.

---

## 🚀 Features

- ✅ **Dynamic QR Code Generation** every 15 seconds (time-limited tokens)
- 📍 **GPS Validation** to ensure students are within the classroom
- 📱 **Device Binding** to prevent proxy attendance (only registered devices can mark)
- 👤 **Admin Dashboard** to start sessions and monitor QR generation
- 🔒 Secure APIs using token-based verification
- 📊 Attendance recorded in MySQL database with session history

---

## 🗃️ Folder Structure

```
qr_attendance_system/
├── app/
│   ├── __init__.py               # Flask app factory and DB setup
│   ├── models.py                 # SQLAlchemy ORM models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin.py              # Admin endpoints: session start, QR management
│   │   ├── attendance.py         # Student attendance submission endpoint
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── qr_generator.py       # Dynamic QR generation logic
│   │   ├── auth.py               # Password hashing utility (future use)
│   │   ├── gps_check.py          # GPS radius validation
│   │   └── device_check.py       # Device binding check
├── static/
│   └── qr/                       # QR images stored here
├── templates/
│   └── admin_dashboard.html      # Admin UI for live QR
├── config.py                     # App configuration (DB, keys, etc.)
├── run.py                        # Entry point for Flask app
├── requirements.txt              # Python dependencies
└── schema.sql                    # MySQL DB schema
```

---

## 🧠 How It Works

1. **Admin logs in** to the dashboard (login support optional).
2. Admin **starts a new session**, providing GPS coordinates of the classroom.
3. A **QR code is generated every 15 seconds** for that session.
4. The QR contains a **secure, random token** that is stored in the database with a timestamp.
5. A **student scans the QR** using an app or frontend, which sends:
   - The **token**
   - Their **GPS location**
   - Their **device ID**
   - Their **student ID**
6. The backend validates:
   - Token is not expired (within 15s)
   - GPS location is within 50 meters
   - Device matches the registered student device
   - Attendance hasn't already been marked
7. If all validations pass, **attendance is recorded**.

---

## 🛠️ How to Run Locally

### ✅ Prerequisites
- Python 3.8+
- MySQL
- Virtualenv (recommended)

---

### 📦 Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/qr-attendance-system.git
cd qr_attendance_system
```

---

### 📁 Step 2: Create Folder Structure

If structure doesn't exist, run the Python generator script:

```bash
python setup_structure.py
```

---

### 🐍 Step 3: Setup Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

pip install -r requirements.txt
```

---

### 🗃️ Step 4: Setup MySQL Database

1. Start your MySQL server.
2. Create a new database:

```sql
CREATE DATABASE qr_attendance;
```

3. Import schema:

```bash
mysql -u root -p qr_attendance < schema.sql
```

> Update username/password in `config.py` if different.

---

### 🧪 Step 5: Run Flask App

```bash
python run.py
```

Visit [http://localhost:5000](http://localhost:5000)

---

## 🧩 Module/Component Breakdown

### 📁 `app/__init__.py`
- Initializes Flask app, configures SQLAlchemy and CORS.
- Registers blueprints for admin and attendance routes.

---

### 📁 `app/models.py`
Defines all database tables:
- `Admin` – Admin users
- `Student` – Registered students + their device IDs
- `Session` – Class sessions
- `QRToken` – Tokens generated every 15 seconds
- `Attendance` – Final attendance record (unique per student per session)

---

### 📁 `app/routes/admin.py`
- Endpoint: `/admin/start_session`
- Admin starts a session with GPS location.
- Triggers dynamic QR generation (stored in `/static/qr/`).
- Returns QR path and session info.

---

### 📁 `app/routes/attendance.py`
- Endpoint: `/attendance/submit`
- Students call this API with:
  - Token from QR
  - Device ID
  - GPS Coordinates
  - Student ID
- Validates all checks and marks attendance.

---

### 📁 `app/utils/qr_generator.py`
- Uses `qrcode` to generate QR image from random token.
- Token is saved to DB with timestamp.
- Image is stored in `static/qr/session_<ID>.png`.

---

### 📁 `app/utils/gps_check.py`
- Uses `geopy` to calculate distance between student and class location.
- Rejects attendance if student is outside radius (default 50m).

---

### 📁 `app/utils/device_check.py`
- Compares incoming device ID to stored device ID for that student.

---

### 📁 `app/utils/auth.py`
- Utility for hashing and verifying passwords (can be used if login is added).

---

### 📁 `templates/admin_dashboard.html`
- Auto-refreshes every 15 seconds to show the new QR code.
- Uses Flask's `render_template` + `url_for` for dynamic image display.

---

## 🧪 Example API Requests

### 1. Start Session (Admin)
```http
POST /admin/start_session
Content-Type: application/json

{
  "latitude": 12.9716,
  "longitude": 77.5946
}
```

### 2. Submit Attendance (Student)
```http
POST /attendance/submit
Content-Type: application/json

{
  "token": "secure_token_here",
  "student_id": "S1001",
  "device_id": "12345-abcde-device",
  "latitude": 12.9716,
  "longitude": 77.5946
}
```

---

## 🧱 Future Enhancements

- Add **admin login** with token-based sessions
- Create **mobile frontend** (Flutter / Android)
- Show **session history and attendance reports**
- Add **face recognition** or **selfie validation**
- Store **QRs in Redis** instead of files (for speed)
- Auto QR regeneration using `APScheduler` or a background thread

---

## 💬 Final Notes

This project is designed to be modular, scalable, and secure. It's suitable for school/college environments that want to digitize and secure attendance without installing biometric hardware.

## 👨‍💻 Author

**Shreyas B and Chandrakanth S** 
