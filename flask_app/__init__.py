from flask import Flask
from .auth.routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('flask_app.config.DevelopmentConfig')

    # database
    from .db import init_db
    init_db(app)

    from .auth.models import login_manager
    login_manager.init_app(app)
    login_manager.login_view = 'login'




    app.register_blueprint(auth_bp)

    return app
