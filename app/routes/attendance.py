from flask import Blueprint, request
from datetime import datetime, timedelta
from app import db
from app.models import QRToken, Session, Student, Attendance
from app.utils.gps_check import is_within_radius
from app.utils.device_check import is_device_valid

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/submit', methods=['POST'])
def submit_attendance():
    data = request.json
    token = data['token']
    student_id = data['student_id']
    device_id = data['device_id']
    lat = data['latitude']
    lng = data['longitude']

    qr_token = QRToken.query.filter_by(token=token).first()
    if not qr_token:
        return {'error': 'Invalid token'}, 400

    # Check token validity
    expiry_time = qr_token.generated_at + timedelta(seconds=15)
    if datetime.utcnow() > expiry_time:
        return {'error': 'QR code expired'}, 400

    session = Session.query.get(qr_token.session_id)
    student = Student.query.filter_by(student_id=student_id).first()

    if not is_device_valid(student, device_id):
        return {'error': 'Invalid device'}, 403

    if not is_within_radius((lat, lng), (session.location_lat, session.location_lng)):
        return {'error': 'You are not in the classroom'}, 403

    # Prevent duplicate
    if Attendance.query.filter_by(student_id=student.id, session_id=session.id).first():
        return {'error': 'Already marked'}, 409

    att = Attendance(student_id=student.id, session_id=session.id)
    db.session.add(att)
    db.session.commit()

    return {'message': 'Attendance marked'}
