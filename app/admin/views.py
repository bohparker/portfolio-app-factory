from flask import render_template, request
from flask_login import current_user, login_user, logout_user, login_required

from app import login_manager
from ..db.queries import validate_user, get_user_object
from . import admin_blueprint as blp
from .forms import LoginForm, PortfolioForm


@login_manager.user_loader
def load_user(id):
    return get_user_object(int(id))


@blp.route('/mypanel', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user_id = validate_user(username, password)
        if user_id:
            user = load_user(user_id)
            login_user(user)
            return f"logged in {user.username}, {user.id}"

    return render_template('login.html', form=form)


@blp.route('/admin-page')
@login_required
def admin_page():
    form1 = PortfolioForm()