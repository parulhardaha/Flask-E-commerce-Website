from flask import Blueprint, render_template
from .forms import LoginForm, SignUpForm

auth=Blueprint('auth', __name__)

#route for login
@auth.route('/login')
def login():
    form=LoginForm()
    return render_template('login.html', form=form)

@auth.route('/sign-up')
def sign_up():
    form=SignUpForm()
    #whenever we return render_template signup.html, the val of form will passed from backend to the frontend here
    return render_template('signup.html', form=form)