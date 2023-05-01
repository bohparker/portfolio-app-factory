import os
from dotenv import load_dotenv

from flask import render_template, request, flash, redirect, url_for, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename

from app import login_manager
from ..db.queries import validate_user, get_user_object, create_project, save_img
from . import admin_blueprint as blp
from .forms import LoginForm, PortfolioForm, BadgeForm


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
    form2 = BadgeForm()
    if request.method == 'POST' and form1.validate_on_submit():
        name = form1.name.data
        link = form1.link.data
        description = form1.description.data

        create_project(name,link,description)
        flash('Project added.', 'success')

        return redirect(url_for('.admin_page'))
    
    elif request.method == 'POST' and form2.validate_on_submit():
        img = form2.image.data
        name = form2.name.data
        link = form2.link.data
        filename = secure_filename(img.filename)

        save_img(name,link,filename)

        img.save(os.path.join(current_app.config['BADGES_FOLDER'], filename))

        return redirect(url_for('.admin_page'))
    
    return render_template('admin-page.html', form1=form1, form2=form2)
