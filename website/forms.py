from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange

class SignUpForm(FlaskForm):
    email=EmailField('Email', validators=[DataRequired()])
    username=StringField('Username', validators=[DataRequired(), Length(min=2)])
    password1=PasswordField('Enter Your Password', validators=[DataRequired(),Length(min=6)])
    password2=PasswordField('Confirm Your Password', validators=[DataRequired(),Length(min=6)])
    submit=SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email=EmailField('Email', validators=[DataRequired()])
    password=PasswordField('Enter Your Password', validators=[DataRequired(),Length(min=6)]) 
    submit=SubmitField('Log in')
