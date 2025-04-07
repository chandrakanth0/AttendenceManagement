from flask import Blueprint, request, render_template
from app import db
from app.models import Session
from app.utils.qr_generator import generate_qr_token

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/start_session', methods=['POST'])
def start_session():
    data = request.json
    lat = data['latitude']
    lng = data['longitude']

    session = Session(location_lat=lat, location_lng=lng)
    db.session.add(session)
    db.session.commit()

    token, path = generate_qr_token(session.id)
    return {
        'message': 'Session started',
        'qr_path': path,
        'session_id': session.id
    }
