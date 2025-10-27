from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt
from .resources.auth import auth_bp
from .resources.users import users_bp
from .resources.projects import projects_bp
from .resources.tasks import tasks_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Enable CORS for frontend (React)
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(projects_bp, url_prefix='/api/projects')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')

    # Health check endpoint
    @app.route('/api/health')
    def health():
        return {'status': 'ok'}, 200

    return app
