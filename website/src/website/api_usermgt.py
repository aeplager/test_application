#from flask import Blueprint, request, jsonify
from flask import Blueprint, render_template, request, flash, jsonify, session, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
from . import auth

import json
import requests
import pandas as pd 
import numpy as np
import pendulum
from . import sqldata as sq
from . import api_general as ap
from . import auth as au


api_usermgt = Blueprint('api_usermgt', __name__)

@api_usermgt.route("/useraccounttypes", methods=['GET', 'POST'])
def ret_sel_useraccounttypes():
    try:
        if au.login_check() == False:
            return ap.generic_json_error()
        else:     
            user_account_type_id = request.args.get('user_account_type_id', None) # use default value repalce 'None'        
            if (user_account_type_id==None):
                user_account_type_id=0        
            sql = '[WebSite].[UserAccountsTypeGetInfo] ' + str(user_account_type_id)
            sql = 'EXEC ' + sql
            js, sts = sq.ret_json(sql)
            if (sts=="SUCCESS"):
                return js
            else:
                return sts        
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return sts  
@api_usermgt.route("/useraccount", methods=['GET', 'POST'])
def ret_sel_useraccount():
    try:
        if au.login_check() == False:
            return ap.generic_json_error()
        else:                 
            user_account = request.args.get('user_account', 'NOID') # use default value repalce 'None'                    
            if (user_account=='NOID'):
                sql = f"EXEC [WebSite].[UserAccountsGetInfo]"
            else:                
                sql = f"EXEC [WebSite].[UserAccountsGetInfo] '{user_account}'"            
            js, sts = sq.ret_json(sql)
            if (sts=="SUCCESS"):
                return js
            else:
                return sts        
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return sts  
@api_usermgt.route("/updateuser", methods=['GET', 'POST'])
def ret_useraccountupdate():
    try:
        sts = au.check_user_super_user() 
        if au.login_check() == False:
            return ap.generic_json_error()
        else:
            if (au.check_user_super_user()=="SUCCESS"):
                email = request.args.get('email', None)            
                user_type_id  = request.args.get('user_type_id', None)
                first_name = request.args.get('first_name', None)
                last_name = request.args.get('last_name', None)
                resetpwd = request.args.get('resetpwd', None)
                active  = request.args.get('active', None)
                super_user = request.args.get('super_user', None)     
                sql = "EXEC [WebSite].[UserAccountsTypeGetInfo] "
                df, sts = sq.ret_pandas(sql)
                df = df.query("UserAccountTypeID == " + str(user_type_id))
                if (len(df)>0):
                    user_type = df.iloc[0]['SYSNAME']   
                else:
                    user_type = "N/A"
                sql = "EXEC [WebSite].[UserAccountsTypeGetInfo] "
                df, sts = sq.ret_pandas(sql)
                df = df.query("UserAccountTypeID == " + str(user_type_id))
                if (len(df)>0):
                    user_type = df.iloc[0]['SYSNAME']   
                else:
                    user_type = "N/A"                     
                reset_code = str(np.random.randint(1000, 9999))
                sql = f"EXEC [WebSite].[UserAccountsGetInfo] '{email}'"
                df, sts = sq.ret_pandas(sql)
                ltr = chr(np.random.randint(65,90))
                ltr =  ltr + chr(np.random.randint(65,90))
                ltr =  ltr + chr(np.random.randint(65,90))    
                sts = "N/A"            
                if (len(df)==1) and (resetpwd == 0):
                    pwd = df.iloc[0]['PWD']
                    sts="SUCCESS"                    
                elif (len(df)>1):
                    sts="FAILURE"
                else:
                    sts="NEW"    
                    pwd_reset = str(reset_code) + "-" +  ltr
                    pwd = au.hash_password(pwd_reset)
                    # Email Password
                    msg = "Your new password is " + pwd_reset + " Please reset your password when you log in"
                    sts = ap.send_email(email,"VRD Important", msg)
                if (sts!="FAILURE"):
                    reset_code = str(np.random.randint(1000, 9999))                               
                dt = pendulum.now().in_tz('GMT')
                dt_string = dt.format('MM/DD/YYYY')                
                sql = f"EXEC [WebSite].[UserAccountsUpsert] @FirstName='{first_name}', @LastName='{last_name}', @Email='{email}', "
                sql = sql + f"@SuperUser = {super_user}, @UserAccountTypeSysName = '{user_type}', @ResetPassword = {resetpwd}"
                sql = sql + f", @ResetCode = {reset_code}, @ResetDate = '{dt_string}', @Active = {active}, @PWD='{pwd}'"
                df, sts = sq.ret_pandas(sql)
                if (len(df)>0):
                    sts = df.iloc[0]['Status']
                else:
                    sts = "FAILURE"
            else:
                sts = "NOT SUFFICIENT RIGHTS"
            json = jsonify({'Status': sts, "Function": "Update User Information"})
            return json            
    except Exception as ex:            
        sts = "FAILURE-SYSTEM:  " + str(ex)   
        json = jsonify({'Status': sts, "Function": "Update User Information"})
        return json              

@api_usermgt.route("/passwordresetandsendemail", methods=['GET', 'POST'])
def ret_passwordresetandsendemail():
    try:        
        sts = "FAILURE"        
        email = request.args.get('email', None)        
        reset_code = str(np.random.randint(1000, 9999))
        ltr = chr(np.random.randint(65,90))
        ltr =  ltr + chr(np.random.randint(65,90))
        ltr =  ltr + chr(np.random.randint(65,90))        
        pwd_reset = str(reset_code) + "-" +  ltr
        pwd = au.hash_password(pwd_reset)
        sql = f"EXEC [WebSite].[UserAccountsResetPasswordAndSendEmailUpsert] @Email = '{email}', @PWD = '{pwd}', @ResetCode = {reset_code}, @ResetPassword = 1 "
        df, sts = sq.ret_pandas(sql)
        if (sts=="SUCCESS") and (len(df)>0):
            msg = "Your new password is " + pwd_reset + " Please reset your password when you log in"
            sts = ap.send_email(email,"VRD Important", msg)
        else:
            sts = "FAILURE-NOUSER"
        json = jsonify({'Status': sts, "Function": "Update User Information"})
        return json            
    except Exception as ex:            
        sts = "FAILURE-SYSTEM:  " + str(ex)   
        json = jsonify({'Status': sts, "Function": "Update User Information"})         

@api_usermgt.route("/passwordreset", methods=['GET', 'POST'])
def ret_useraccountpassword():
    try:
        sts = "FAILURE"
        email = session['username']
        email=email.strip()        
        password1 = request.args.get('password1', None)    
        password2 = request.args.get('password2', None)    
        password1 = password1.strip()
        password2 = password2.strip()
        json = jsonify({'Status': sts, "Function": "Update User Information"})
        if (password1==None) or (password1==None):
             json = jsonify({'Status': "FAILURE-TWO PASSWORDS REQUIRED", "Function": "Update Password"})
        elif (len(password1)<7):
             json = jsonify({'Status': "FAILURE-PASSWORD NEEDS TO BE AT LEAST 7 CHARACTERS", "Function": "Update Password"})
        else:
            # Obtain Hash Password
            pwd = au.hash_password(password1)
            sql = f"EXEC [WebSite].[UserAccountsPasswordResetUpsert] @Email='{email}', @PWD='{pwd}'"
            df, sts = sq.ret_pandas(sql)                        
            if (sts=="SUCCESS"):
                sts = df.iloc[0]['Status']            
                if (sts=="SUCCESS"):
                    msg = "Your password for VRD has been reset to " + password1;
                    sts = ap.send_email(email,"VRD Important", msg)
            json = jsonify({'Status': sts, "Function": "Update User Information"})
        return json            
    except Exception as ex:            
        sts = "FAILURE-SYSTEM:  " + str(ex)   
        json = jsonify({'Status': sts, "Function": "Update User Information"}) 
       