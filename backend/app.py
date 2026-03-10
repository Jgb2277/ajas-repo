import os
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from models import db

socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__, static_folder='uploads/pdfs', static_url_path='/files')
    app.config['SECRET_KEY'] = 'dev-secret-key-edupath'
    
    # Ensure upload directory exists
    os.makedirs(os.path.join(app.root_path, 'uploads', 'pdfs'), exist_ok=True)
    
    # Use absolute path for db to avoid issues with working dir
    db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'edupath.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app)
    db.init_app(app)
    socketio.init_app(app)

    with app.app_context():
        # Import blueprints
        from routes.auth import auth_bp
        from routes.student import student_bp
        from routes.admin import admin_bp
        from routes.chat import init_socket_events
        
        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(student_bp, url_prefix='/api/student')
        app.register_blueprint(admin_bp, url_prefix='/api/admin')
        
        # Initialize socket events
        init_socket_events(socketio)
        
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, debug=True, port=5000, allow_unsafe_werkzeug=True)
