from flask import Blueprint, render_template, request # type: ignore #this file is Blueprint of our app
from flask import flash, redirect, url_for # type: ignore
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password') 

        user=User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in successfully', category='success')
                login_user(user, remember=True)     #store in flask session
                return redirect(url_for('views.home'))
                
            else:
                flash('incorret password, try again!', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template('login.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()       #automatically logout current user
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method=='POST':
        email=request.form.get('email')
        first_name=request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        user=User.query.filter_by(email=email).first()
        if user:
            flash('Email already Exist', category='error')
        elif len(email)<4:
            flash('Email must be greater than 3 characters', category='error') #if this is failure message then "error"
        elif len(first_name)<2:
            flash('First name must be greater than 1 characters', category='error')
        elif password1!=password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1)<7:
            flash('Password must be at least 7 characters', category='error')
        else:
            #print(email, firstName, password1, password2)
            #add user to DB
            #hashed_password = generate_password_hash(password1, method='sha256')
            new_user=User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))  #Encrypt password and store
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash('Account created!', category="success")
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)