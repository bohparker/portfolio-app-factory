from wtforms.fields import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        [InputRequired()]
    )
    password = PasswordField(
        'Password',
        [InputRequired()]
    )
    submit = SubmitField(
        'Submit',
        [InputRequired()]
    )

class PortfolioForm(FlaskForm):
    name = StringField(
        'Name',
        [InputRequired()]
    )
    link = StringField(
        'Link',
        [InputRequired()]
    )
    description = TextAreaField(
        'Description',
        [InputRequired()]
    )
    submit = SubmitField(
        'Submit',
        [InputRequired()]
    )