from flask import Flask
from flask_migrate import Migrate
from .models import db

migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'checkers game'

    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    
    from .routes.test_route import main
    app.register_blueprint(main)

    from .routes.auth_route import auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from.routes.game_routes import game_blueprint
    app.register_blueprint(game_blueprint)

    return app