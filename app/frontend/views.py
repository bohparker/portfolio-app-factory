import os
from flask import render_template, request, redirect, flash

from . import frontend_blueprint as blp

from .forms import ContactForm
from app import mail

@blp.route('/')
def index():
    return render_template('index.html')

@blp.route('/education')
def education():
    return render_template('education.html')

@blp.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@blp.route('/contact', methods=('GET','POST'))
def contact():
    form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        contact = form.contact.data
        subject = form.subject.data
        message = form.message.data

        mail.send_email(os.environ['DEFAULT_MAIL_SENDER'], subject, 'email/contact', contact=contact, message=message)
        flash('Message has been sent!', 'success')
        return redirect('contact')
    
    if form.errors:
        for error, message in form.errors.items():
            flash(message[0], 'warning')
            return render_template('contact.html', form=form)

    return render_template('contact.html', form=form)