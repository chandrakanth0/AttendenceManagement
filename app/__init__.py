from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    from .routes.admin import admin_bp
    from .routes.attendance import attendance_bp

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')

    return app
