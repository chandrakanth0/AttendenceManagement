from app import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(255))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    student_id = db.Column(db.String(20), unique=True)
    device_id = db.Column(db.String(255))

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    location_lat = db.Column(db.Float)
    location_lng = db.Column(db.Float)

class QRToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    token = db.Column(db.String(255))
    generated_at = db.Column(db.DateTime)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    marked_at = db.Column(db.DateTime, default=db.func.now())
    __table_args__ = (db.UniqueConstraint('student_id', 'session_id', name='unique_attendance'),)
