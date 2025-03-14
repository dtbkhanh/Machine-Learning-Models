from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


# https://flask-wtf.readthedocs.io/en/stable/
class LoginForm(FlaskForm):
    usermail = StringField('Mail', validators=[DataRequired()])
    submit = SubmitField('Login')
    remember_me = BooleanField('Remember Me')


class RegistrationForm(FlaskForm):
    username = StringField('Name', validators=[DataRequired()])
    usermail = StringField('Mail', validators=[DataRequired()])
    submit = SubmitField('Register')
