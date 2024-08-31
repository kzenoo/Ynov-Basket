from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from YNOV_BASKET.models import User
from YNOV_BASKET.routes import bp as routes_bp

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'routes.login'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    login_manager.init_app(app)
    
    app.register_blueprint(routes_bp)

    with app.app_context():
        db.create_all()  # Crée les tables ici si elles n'existent pas

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
