from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from app import login_manager
from ..db.queries import validate_user, get_user_object, create_project
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
            return redirect(url_for('.admin_page'))

    return render_template('login.html', form=form)


@blp.route('/admin-page', methods=('GET', 'POST'))
@login_required
def admin_page():
    form1 = PortfolioForm()
    if request.method == 'POST' and form1.validate_on_submit():
        name = form1.name.data
        link = form1.link.data
        description = form1.description.data

        create_project(name,link,description)
        flash('Project added.', 'success')

        return redirect(url_for('.admin_page'))
    
    return render_template('admin-page.html', form1=form1)
