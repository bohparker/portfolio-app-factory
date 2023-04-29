import os
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_login import LoginManager


csrf = CSRFProtect()
mail = Mail()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    load_dotenv()

    app.config['DEBUG'] = True

    app.config['SECRET_KEY'] = os.environ['SECRET_KEY'] or 'none'
    app.config['WTF_CSRF_SECRET_KEY'] = os.environ['WTF_CSRF_SECRET_KEY'] or 'none'


    csrf.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin_blueprint.login'
    login_manager.login_message_category = 'info'

    from app.frontend import frontend_blueprint
    app.register_blueprint(frontend_blueprint)

    from app.admin import admin_blueprint
    app.register_blueprint(admin_blueprint)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app