import qrcode
import secrets
import datetime
from app import db
from app.models import QRToken
import os

def generate_qr_token(session_id):
    token = secrets.token_urlsafe(16)
    now = datetime.datetime.utcnow()

    # Store in DB
    qr = QRToken(session_id=session_id, token=token, generated_at=now)
    db.session.add(qr)
    db.session.commit()

    # Generate QR image
    img = qrcode.make(token)
    path = f'static/qr/session_{session_id}.png'
    img.save(path)

    return token, path
