from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, User
from routes import main

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(main)

with app.app_context():
    db.create_all()
    # Seed admin user if not exists
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password="admin", role='Admin')
        db.session.add(admin)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)