import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecretkey')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:password@localhost/qr_attendance')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    QR_EXPIRY_SECONDS = 15
    LOCATION_RADIUS_METERS = 50
