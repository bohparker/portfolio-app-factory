from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired


class ContactForm(FlaskForm):
    contact = StringField(
        'Email or Phone',
        [InputRequired('Enter either an email address or a phone number.')]
    )
    subject = StringField(
        'Subject',
        [InputRequired('Enter a subject.')]
    )
    message = TextAreaField(
        'Message',
        [InputRequired('Enter a message.')]
    )
    submit = SubmitField(
        'Submit'
    )