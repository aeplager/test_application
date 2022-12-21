from flask import Blueprint, render_template, request, flash, jsonify, session, url_for
from . import auth as au
from . import sqldata as sq
import pandas as pd
import pendulum 
import json
import os
import requests

import smtplib, ssl
from . import import_data as ida
from email.mime.text import MIMEText

# Getting IP
from requests import get

api_general = Blueprint('api_general', __name__)

@api_general.route('/azureparms', methods=['GET', 'POST'])
def azureparms():    
    try:
        if au.login_check() == False:
            return generic_json_error()
        else:    
            sql = 'EXEC [WebSite].[AzureParamsGetInfo]'
            df, sts = sq.ret_pandas(sql)
            if (sts != "SUCCESS"):
                return jsonify({'Status': "FAILURE", "Type": "AzureParms"})
            else:
                # Return specific json 
                ln = len(df)
                if (ln==0):
                    return jsonify({'Status': "FAILURE", "Type": "AzureParms"})
                else:                    
                    AzureContainer = df.iloc[0]['AzureContainer']  
                    SASKey = df.iloc[0]['SASKey']  
                    blobUri = df.iloc[0]['blobUri']  
                    AzureStorageName = df.iloc[0]['AzureStorageName']  
                    return jsonify({'Status': "SUCCESS", "Type": "AzureParms","AzureContainer": AzureContainer, "SASKey": SASKey, "blobUri": blobUri, "AzureStorageName": AzureStorageName})
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return jsonify({'Status': "FAILURE", "Type": "AzureParms"})
    
@api_general.route('/return_file_docker', methods=['GET', 'POST'])    
def return_file_docker():
    try:
        if au.login_check() == False:
            return generic_json_error()
        else: 
            docker_url = ret_envvbl("File_Docker_URL")            
            return jsonify({'Status': "SUCCESS", "Docker_URL": docker_url})
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)  
        return jsonify({'Status': "FAILURE", "Type": "AzureParms"})

# Addition of Azure Functions
@api_general.route('/return_azure_function', methods=['GET', 'POST'])    
def return_azure_function():
    try:
        if au.login_check() == False:
            return generic_json_error()
        else: 
            azure_function_url = ret_envvbl("Azure_Function_URL")            
            return jsonify({'Status': "SUCCESS", "Azure_Function_URL": azure_function_url})
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)  
        return jsonify({'Status': "FAILURE", "Type": "Azure_Function_URL"})


@api_general.route('/return_unique_filename/<file_name>', methods=['GET', 'POST'])        
def return_unique_filename(file_name):
    try:
        if au.login_check()== False:
            return generic_json_error()
        else:
            ls = file_name.rfind('.')
            ln = len(file_name)-ls-1
            file_begin = file_name[:ln]
            file_end = file_name[ln:]
            print(file_end)
            dt_now = pendulum.now()
            # Create Date
            str_date = str(dt_now.year)
            str_date = str_date + '_' + str(dt_now.month).zfill(2)
            str_date = str_date + '_' + str(dt_now.day).zfill(2)
            str_date = str_date + '_' + str( dt_now.hour).zfill(2)
            str_date = str_date + '_' + str(dt_now.minute).zfill(2)
            str_date = str_date + '_' + str(dt_now.second).zfill(2)
            file_name = file_begin + '_'  + str_date + file_end
            return jsonify({'Status': "SUCCESS", "Type": "return_unique_filename", "file_name": file_name})           
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)  
        return jsonify({'Status': "FAILURE", "Type": "return_unique_filename"})       
        
def generic_json_error():
    return jsonify({'Status': "FAILURE", "Type": "Login"})
def ret_envvbl(env_vbl):
    try:
        retVBL = os.environ[env_vbl]
        if retVBL[:2] == '= ':    
            retVBL = retVBL[2:] 
        retVBL = retVBL.strip()    
        return retVBL#os.environ[env_vbl]
    except Exception as ex:            
        sts = "FAILURE TO RETURN:  " + env_vbl
        sts = sts + " with return of  " + str(ex)          
        flash('Error Message of ' + sts, category='success')                    
        return sts 
    
@api_general.route("/return_excel_sheets/<file_name>", methods=['GET', 'POST'])
def return_excel_sheets(file_name):
    try:
        if au.login_check() == False:            
            return au.generic_json_error()
        else:
            urlMain = ret_envvbl("Azure_Function_URL") + 'vrd_determine_sheets/?' + file_name
            return_json = requests.get(urlMain)
            return_json = str(return_json.text)            
            return return_json
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return jsonify({'Status': sts, "URL": "N/A"})  
    
@api_general.route("/return_datafactory_run_status", methods=['GET', 'POST'])
def return_datafactory_run_status():
    try:    
        if au.login_check() == False:
            return au.generic_json_error()
        else:        
            run_id = request.args.get('run_id', None)                          
            sts, run_id, run_status, dt_diff_connection, dt_diff_obtain = ida.pipeline_run_id_status(run_id)
            return jsonify({'Status': sts, "run_id": run_id, "run_status": run_status,"connection_time": dt_diff_connection, "obtain_time": dt_diff_obtain})          
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return jsonify({'Status': sts, "run_id": run_id, "run_status": "FAILURE", "connection_time": None, "obtain_time": None})          

def send_email(email_rec, Subject, Body):
    try:
        smtp_server = "smtp.gmail.com"
        port = 587  # For starttls
        sender_email = ret_envvbl("outgoing_email") #"aeplager@qkss.com"        
        password = ret_envvbl("outgoing_pwd") # "Simeon#124$"
        if (sender_email == "aeplager@qkss.com"):
            password = password + '$'
        # Create a secure SSL context
        context = ssl.create_default_context()
        server = smtplib.SMTP(smtp_server,port)    
        server.starttls(context=context) # Secure the connection    
        server.login(sender_email, password)
        if (Subject == None):
            Subject = "VRD Important"
        elif (len(Subject)<2):
            Subject = "VRD Important"
            
        msg = MIMEText(Body)
        msg['Subject'] = Subject
        msg['From'] = sender_email
        msg['To'] = email_rec
        
        server.sendmail(sender_email, email_rec,  msg.as_string())
        
        #server.sendmail(sender_email, email_rec,  msg.as_string())
        #server.sendmail(sender_email, email_rec, message)
        return "SUCCESS"
    except Exception as e:        
        return "FAILURE: " + str(e)
    finally:
        server.quit()    
def ret_super_user():
    try:
        super_user_user_name = ret_envvbl("super_user_user_name")
        super_user_pwd = ret_envvbl("super_user_pwd")
        check_super_user = au.check_user_super_user()
        sts = "SUCCESS"
        return sts, super_user_user_name, super_user_pwd, check_super_user
    except Exception as e:        
        return "FAILURE: " + str(e), None, None, None
        
@api_general.route("/ret_logged_in", methods=['GET', 'POST'])
def ret_logged_in():
    try:
        sts = "TRUE"
        if au.login_check() == False:
            sts = "FALSE" 
        js = jsonify({'Status': "SUCCESS", "LoginStatus": sts})
        return js
    except Exception as e:        
        js = jsonify({'Status': "FALSE", "LoginStatus": "FALSE"})
        return js

# @api_general.route("/get_svr_ip", methods=['GET', 'POST'])
# def ret_current_ip():
#     try:
#         sts = "SUCCESS"
#         ip = get('https://api.ipify.org').text
#         js = jsonify({'Status': sts, "IP": str(ip)})
#         return js
#     except Exception as e:       
#         sts = "FAILURE" 
#         ip = "0.0.0.0"
#         js = jsonify({'Status': sts, "IP": str(ip)})
#         return js
    
@api_general.route("/connection_status", methods=['GET', 'POST'])
def ret_connection_status():
    try:
        cnxn, sts = sq.connect_db()        
        js = jsonify({'Status': sts, "Type": "Connection Status"})
        return js
    except Exception as e:       
        sts = "FAILURE Website Status"   
        js = jsonify({'Status': sts, "Type": "Connection Status"})
        return js    