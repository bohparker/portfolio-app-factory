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
    
    app.config['DATABASE_URI'] = os.environ['DATABASE_URI']
    
    app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER']
    app.config['MAIL_PORT'] = os.environ['MAIL_PORT']
    app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
    app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
    app.config['DEFAULT_MAIL_SENDER'] = os.environ['DEFAULT_MAIL_SENDER']
    app.config['MAIL_SUBJECT_PREFIX'] = os.environ['MAIL_SUBJECT_PREFIX']
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    basedir = os.path.abspath(os.path.dirname(__file__))
    badges_folder = os.path.join(basedir, 'static/images/badges')
    app.config['BADGES_FOLDER'] = badges_folder

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