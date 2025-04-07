import os

folders = [
    "app/routes",
    "app/utils",
    "static/qr",
    "templates",
]

files = {
    "app/__init__.py": "",
    "app/models.py": "",
    "app/routes/__init__.py": "",
    "app/routes/admin.py": "",
    "app/routes/attendance.py": "",
    "app/utils/__init__.py": "",
    "app/utils/qr_generator.py": "",
    "app/utils/auth.py": "",
    "app/utils/gps_check.py": "",
    "app/utils/device_check.py": "",
    "templates/admin_dashboard.html": "<!-- Admin Dashboard HTML -->",
    "config.py": "",
    "run.py": "",
    "requirements.txt": "",
    "schema.sql": "-- MySQL schema here",
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for filepath, content in files.items():
    with open(filepath, "w") as f:
        f.write(content)

print("✅ Folder and file structure created!")
