from flask import Blueprint


frontend_blueprint = Blueprint('frontend_blueprint', __name__)

from . import views