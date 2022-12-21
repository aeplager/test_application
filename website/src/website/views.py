from flask import Blueprint, render_template, request, flash, jsonify, session ,url_for, redirect
from flask_login import login_required, current_user
from .models import Note
from . import auth as au
from . import db
import json
from . import sqldata as sq
from . import api_general as ap
import requests 
import pyodbc
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('auth.login'))   

@views.route('/graphing_page', methods=['GET', 'POST'])
def testing_stuff():
    return render_template("graphing_page.html", user=current_user)    

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    if au.login_check() == False:
        return redirect(url_for('auth.login'))
    else:              
        note = json.loads(request.data)
    return jsonify({})

@views.route('/test_connection', methods=['GET', 'POST'])  
def vw_ret_test_connection():
    try:
        fctn = "test_connect V5"        
        PYODBC_Connection = ap.ret_envvbl("DBSVRConnectionString") #'DRIVER=' + Driver + ';SERVER=' + Server +  ';DATABASE=' + Database + ';UID=' + Uid + ';PWD=' + Pwd                    
        print(PYODBC_Connection)        
        PYODBC_Connection = PYODBC_Connection.replace("dollardollar", "$")                
        myip = requests.get('https://www.wikipedia.org').headers['X-Client-IP']
        Driver = "ODBC Driver 17 for SQL Server"
        Database = "TestApplication"
        Uid="SA"
        Pwd = "G0gators#124$"
        AdditionalCommands = "Encrypt=yes;TrustServerCertificate=yes"
        Server = str(myip)
        Server = "host.docker.internal,1433"
        PYODBC_Connection = 'DRIVER=' + Driver + ';SERVER=' + Server +  ';DATABASE=' + Database + ';UID=' + Uid + ';PWD=' + Pwd + ";" #+ AdditionalCommands        
        print(PYODBC_Connection)
        sts = "SUCCESS"
        #cnxn, sts = sq.connect_db()
        cnxn = pyodbc.connect(PYODBC_Connection)  
        js = jsonify({'Status': sts, "Function": fctn, "PYODBC_Connection": PYODBC_Connection})
        return js
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        fctn = "test_connect V5"
        return jsonify({'Status': sts, "Function": fctn})    
    
@views.route('/data_entry_page', methods=['GET', 'POST'])
def wholesaledealpage():     
    if au.login_check() == False:
        return redirect(url_for('auth.login'))
    else:        
        return render_template("data_entry_page.html", user=current_user)
    

@views.route('/passwordreset', methods=['GET', 'POST'])
def ret_passwordreset():
    if au.login_check() == False:
        return redirect(url_for('auth.login'))
    else:        
        return render_template("passwordreset.html", user=current_user)
             
   
@views.route('/adminscreens', methods=['GET', 'POST'])
def ret_adminscreens():     
    if au.login_check() == False:
        return redirect(url_for('auth.login'))
    else:        
        # Test if user can view        
        username = session["username"]        
        # Check if user has rights  
        if (au.check_user_super_user()=="SUCCESS"):
            super_user= 1
        else:              
            sql = f"EXEC [WebSite].[UserAccountsGetInfo] '{username}'" 
            df, sts = sq.ret_pandas(sql)
            user_level = df.iloc[0]['UserAccountSYSNAME']
            super_user = df.iloc[0]['SuperUser']                           
        if (super_user == 1):
            return render_template("useradmin.html", user=current_user)
        else:
            return render_template("wholesaledealpage.html", user=current_user)
        


