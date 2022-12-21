from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash # Possibly Remove
from . import db
from flask_login import login_user, login_required, logout_user, current_user # Possibly Remove
# Password Stuff
import hashlib, binascii, os

from . import sqldata as sq
from . import api_general as ap

import pyodbc
import pandas 

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():    
    try:
        login_status=False
        if request.method == 'POST':        
            email = request.form.get('email')
            password = request.form.get('password')                
            pwd = 'N/A'
            sts, userstatus, pwd = check_user(email)                        
            msg = "Error"       
            super_user_user_name = ap.ret_envvbl("super_user_user_name")
            super_user_pwd = ap.ret_envvbl("super_user_pwd")   
            if (userstatus == 'EXISTS'):                        
                if (verify_password(pwd, password)==True):                                   
                    msg="Login Successful"
                    session['loggedin'] = True
                    session['id'] = 1
                    session['username'] = email
                    session['pwd'] = password
                    flash('Logged in successfully!' + msg, category='success')                    
                    login_status = True
                else:
                    msg = "Login Failure"
                    flash(msg, category='error')                    
                    login_status = False 
            elif (email==super_user_user_name) and (super_user_pwd==super_user_pwd):
                msg="Login Successful"                    
                session['loggedin'] = True
                session['id'] = 1              
                session['username'] = super_user_user_name
                session['pwd'] = super_user_pwd      
                login_status = True          
        if login_status==True:
            #return redirect(url_for('views.wholesaledealpage'))
            return redirect(url_for('views.testing_stuff'))
        else:
            return render_template("login.html", user=current_user)
    except:
        
        return render_template("login.html", user=current_user)                
    
@auth.route('/logout')
#@login_required
def logout():
    if login_check() == False:
        return redirect(url_for('auth.login'))
    else:
        #logout_user()
        session.pop('loggedin')
        session.pop('id')
        session.pop('username')
        session.pop('pwd')
        return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')        
        sts, userstatus, pwd2 = check_user(email)                    
        #user = User.query.filter_by(email=email).first()
        pwd = hash_password(password1)        
        sts, userstatus, pwd_check = check_user(email)            
        if (sts == "EXISTS"):
            flash('Email already exists.' + sts,  category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.' + sts, category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.' + sts, category='error')
        elif (password1 != password2):
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')   
        else:                       
            sts = update_user(first_name, first_name, email, pwd)
            new_user = User(email=email, first_name=first_name, password=pwd)    
            session['pwd'] = pwd
            #db.session.add(new_user)
            #db.session.commit()
            #login_user(new_user, remember=True)
            flash('Account created!' + sts, category='success')
            return redirect(url_for('views.wholesaledealpage'))
    return render_template("sign_up.html", user=current_user)

def check_user(email):
    try:
        sql = f"EXEC [WebSite].[UserAccountsGetInfo] '{email}'"        
        df, sts = sq.ret_pandas(sql)        
        ln = len(df)
        pwd = 'N/A'
        SYSNAME = 'N/A'
        UserAccountType = 'N/A'
        UserAccountTypeID = 0               
        if (ln == 0):                             
            userstatus="DNE"            
        if (ln>0):
            userstatus="EXISTS"                        
            pwd = df.iloc[0]['PWD']                        
            SYSNAME = df.iloc[0]['UserAccountSYSNAME']     
            UserAccountType = df.iloc[0]['UserAccountType']     
            UserAccountTypeID = df.iloc[0]['UserAccountTypeID']  
        if (check_user_super_user() == "SUCCESS"):
            ln = 1            
            pwd = ap.ret_envvbl("super_user_pwd")
            userstatus="EXISTS"            
        sts="SUCCESS"            
        return sts, userstatus, pwd
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)        
        return sts, sts, "N/A"
def update_user(firstname, lastname, email, pwd):
    # Update the user information including password
    try:
        sts = "FAILURE"
        sql = f"EXEC [WebSite].[UserAccountsUpsert] '{firstname}','{lastname}','{email}','{pwd}'"        
        df, sts = sq.ret_pandas(sql)        
        return sts 
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)        
        return sts
def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password    

def login_check():            
    # Check if Logged In
    try:
        if not ("username" in session):        
            return False
        else:
            return True        
    except:
        return False
def obtain_user():  
    # Return User Name
    try:
        if not ("username" in session):        
            user = session["username"]
            return user
        else:
            return None
    except:
        return None      
def check_user_super_user():
    try:
        super_user_user_name = ap.ret_envvbl("super_user_user_name")
        super_user_pwd = ap.ret_envvbl("super_user_pwd")
        user_email = session["username"]
        pwd  = session['pwd']
        super_user = 0
        if (user_email==super_user_user_name) and (super_user_pwd==pwd):
            super_user = 1
        else:
            sql = f"EXEC [WebSite].[UserAccountsGetInfo] '{user_email}'" 
            df, sts = sq.ret_pandas(sql)  
            user_level = df.iloc[0]['UserAccountSYSNAME']
            super_user = df.iloc[0]['SuperUser']             
        if super_user==True:
            sts = "SUCCESS"
        else:
            sts = "FAILURE"
        return sts
    except:
        return "SYSTEM-FAILURE"         
