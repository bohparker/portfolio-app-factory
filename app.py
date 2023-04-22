import os
from threading import Thread
from dotenv import load_dotenv
from flask import Flask, render_template, \
    flash, url_for, request, current_app, redirect
from flask_wtf import CSRFProtect
from flask_mail import Mail, Message

from forms import ContactForm

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['WTF_CSRF_SECRET_KEY'] = os.environ['WTF_CSRF_SECRET_KEY']
app.config['MAIL_SERVER'] = os.environ['MAIL_SERVER']
app.config['MAIL_PORT'] = os.environ['MAIL_PORT']
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['DEFAULT_MAIL_SENDER'] = os.environ['DEFAULT_MAIL_SENDER']
app.config['MAIL_SUBJECT_PREFIX'] = os.environ['MAIL_SUBJECT_PREFIX']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

csrf = CSRFProtect(app)
mail = Mail(app)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['DEFAULT_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact', methods=('GET','POST'))
def contact():
    form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        contact = form.contact.data
        subject = form.subject.data
        message = form.message.data

        send_email(os.environ['DEFAULT_MAIL_SENDER'], subject, 'email/contact', contact=contact, message=message)
        return redirect('contact')
    

    return render_template('contact.html', form=form)

@app.route('/education')
def education():
    return render_template('education.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404





if __name__ == '__main__':
    app.run()