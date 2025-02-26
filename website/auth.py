from flask import Blueprint, render_template, flash, redirect
from .forms import LoginForm, SignUpForm
from .models import Customer
from . import  db
from flask_login import login_user, login_required, logout_user

auth=Blueprint('auth', __name__)

#route for login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data

        #check if this particular customer exists in db
        customer=Customer.query.fiter_by(email=email).first()  #unique email are there

        if customer:
            if customer.verify_password(password=password):
                login_user(customer)
                return redirect('/')
            else:
                flash('Incorrect Email or Password')    
        else:
            flash('Account does not exist please Sign Up')    
    return render_template('login.html', form=form)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form=SignUpForm()
    
    #collecting data from user
    if form.validate_on_submit():
        email=form.email.data
        username=form.username.data
        password1=form.password1.data
        password2=form.password2.data

        if password1== password2:
            #if equal then create new customer
            new_customer=Customer()
            new_customer.email=email
            new_customer.username=username
            #when call  this pass->password setter with hasned form
            new_customer.password=password2

            #add this customer to db
            try:
                db.session.add(new_customer)
                db.session.commit()
                flash('Account Created Successfully, You can now Login')
                return redirect('/login')
            except Exception as e:
                print(e)
                flash('Account Not Created!!, Email already exists')

            form.email.data=''    
            form.username.data=''
            form.password1.data=''
            form.password2.data=''

    #whenever we return render_template signup.html, the val of form will passed from backend to the frontend here
    return render_template('signup.html', form=form)

@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def log_out():
    logout_user()
    return redirect('/')