#from flask import Blueprint, request, jsonify
from flask import Blueprint, render_template, request, flash, jsonify, session, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
from . import auth

import json
import requests
import pandas as pd 
from . import sqldata as sq
from . import api_general as ap
from . import auth as au
from . import import_data as ida

api_wholesaledeal = Blueprint('api_wholesaledeal', __name__)
    
@api_wholesaledeal.route("/general/<list_type>", methods=['GET', 'POST'])
def ret_sel_list(list_type):
    try:    
        if au.login_check() == False:
            return ap.generic_json_error()
        else:        
            sql = '[WebSite].[WholesaleDealGetInfo]'
            if (list_type=='deallist'):
                sql = '[WebSite].[WholesaleDealGetInfo]'
            elif (list_type=='counterparty'):
                sql = '[WebSite].[CounterPartyGetInfo]'
            elif (list_type=='counterparty'):
                sql = '[WebSite].[CounterPartyGetInfo]'
            elif (list_type=='wholesaleblock'):
                sql = '[WebSite].[WholeSaleBlocksGetInfo]'
            elif (list_type=='settlementpoint'):
                sql = '[WebSite].[SettlementPointsGetInfo]'
            elif (list_type=='settlementlocation'):
                sql = '[WebSite].[SettlementLocationGetInfo]'
            else:
                sql = '[WebSite].[WholesaleDealGetInfo]'
            sql = 'EXEC ' + sql
            js, sts = sq.ret_json(sql)
            if (sts != "SUCCESS"):
                return "FAILURE-1" + sts 
            else:
                return js    
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return sts    
    

@api_wholesaledeal.route("/dealselection/<wholesaledealid>", methods=['GET', 'POST'])
#@login_required
def ret_sel_dealinfo(wholesaledealid):
    try:
        if au.login_check() == False:
            return ap.generic_json_error()
        else:     
            if (wholesaledealid==None):
                wholesaledealid=0        
            sql = '[WebSite].[WholesaleDealGetInfo] ' + str(wholesaledealid)
            sql = 'EXEC ' + sql
            df, sts = sq.ret_pandas(sql)
            if (len(df)>0):
                df['CloseDate'] = pd.to_datetime(df['CloseDate'])                
                df['CloseDateString'] = df['CloseDate'].dt.strftime('%Y-%m-%d')                   
            else:
                df['CloseDateString'] = ''                
            js = df.to_json(orient='index')            
            if (sts=="SUCCESS"):
                return js
            else:
                return sts        
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return sts    
    
@api_wholesaledeal.route('/updatedeal', methods=['GET', 'POST'])
#@login_required
def create_cm():
    try:
        if au.login_check() == False:
            return ap.generic_json_error()
        else:     
            WholeSaleDealID = request.args.get('WholeSaleDealID', 0) # use default value repalce 'None'        
            WholesaleDealName = request.args.get('WholesaleDealName', None)
            CounterPartyID = request.args.get('CounterPartyID', None)
            SecondCounterPartyID = request.args.get('SecondCounterPartyID', None)
            SettlementPointID = request.args.get('SettlementPointID', None)
            SettlementLocationID = request.args.get('SetLocationID', None)
            WholeSaleBlockID = request.args.get('WholeSaleBlockID', None)
            StartDate = request.args.get('StartDate', None)
            EndDate = request.args.get('EndDate', None)
            VolumeMW = request.args.get('VolumeMW', None)
            Price = request.args.get('Price', None)
            Active = request.args.get('Active', None)
            BuySell = request.args.get('BuySell', None)
            Fee = request.args.get('Fee', None)  
            PhysicalFinancial = request.args.get('PhysicalFinancial', None)  
            UserName = session['username']
            sql = """\
            DECLARE @RC int;
            EXEC @RC = [WebSite].[WholesaleDealUpsert] ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?;
            SELECT @RC AS rc;
            """
            values = (WholeSaleDealID,WholesaleDealName,CounterPartyID, SecondCounterPartyID, SettlementPointID , SettlementLocationID, WholeSaleBlockID, StartDate, EndDate, VolumeMW, Price, Active, Fee, BuySell, PhysicalFinancial, UserName)    
            # Reset it to base
            sts = "FAILURE"
            WholeSaleDealID = 0
            data, sts = sq.ret_pandas(sql, values) 
            #print(sts)
            if (sts!="SUCCESS"):
                json = jsonify({'Status': "FAILURE", "Identifier": WholeSaleDealID})
            else:
                for ind in data.index: 
                    sts = data['Status'][ind]
                    Identifier = data['IdentifierID'][ind]
                json = jsonify({'Status': sts, "Identifier": str(Identifier)})
            return json
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return jsonify({'Status': sts, "Identifier": 0})      
    
@api_wholesaledeal.route("/confirm_deal/", methods=['GET', 'POST'])
def ret_confirm_deal():
    try:
        wholesale_deal_id = request.args.get('wholesale_deal_id', 0) # use default value repalce 'None'        
        confirm_status = request.args.get('confirm_status', 1) # use default value repalce 'None'        
        if au.login_check() == False:            
            return ap.generic_json_error()
        else:
            username = session["username"]
            # Check if user has rights
            sql = f"EXEC [WebSite].[UserAccountsGetInfo] '{username}'" 
            df, sts = sq.ret_pandas(sql)        
            ln = len(df)            
            js = jsonify({'Status': "FAILURE", "confirm_deal": 'SYSTEMFAILURE'}) 
            if (ln == 0): 
                sts = "FAILURE-NORIGHTS"
                js = jsonify({'Status': sts, "confirm_deal": 'NO RIGHTS'}) 
            else:
                user_level = df.iloc[0]['UserAccountSYSNAME']
                super_user = df.iloc[0]['SuperUser']
                if (user_level=="MGR") or (user_level == "RISKCONT") or (super_user==1):                                        
                    sql = f"EXEC [WebSite].[WholeSaleDealConfirmUpsert] @WholeSaleDealID = {wholesale_deal_id}, @ConfirmBit={confirm_status}, @Username='{username}'"                    
                    data, sts = sq.ret_pandas(sql)
                    sts = data.iloc[0]['Status']                    
                    js = jsonify({'Status': sts, "confirm_deal": 'SUCCESS'})          
                else:
                    sts = "FAILURE"                    
                    js = jsonify({'Status': sts, "confirm_deal": 'NO RIGHTS'})      
            return js
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return jsonify({'Status': sts, "confirm_deal": 'FAILURE'})          
        

@api_wholesaledeal.route("/import_custom_data/", methods=['GET', 'POST'])
def ret_import_custom_data():
    try:
        if au.login_check() == False:            
            return ap.generic_json_error()
        else:
            # Pull Parameters
            file_name = request.args.get('file_name', None) # use default value repalce 'None'        
            wholesale_deal_id = request.args.get('wholesale_deal_id', None)            
            sheet_name = request.args.get('sheet_name', 'CSV')                    
            block_type = request.args.get('block_type', None)  
            file_type = request.args.get('file_type', None)                         
            sts, run_response = ida.call_data_factory_wholesaleblock(file_name, file_type, block_type, sheet_name, wholesale_deal_id)
            return_json = jsonify({'Status': sts, "run_response": str(run_response.run_id)})      
            return return_json
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return jsonify({'Status': sts, "URL": "N/A"})     
     
@api_wholesaledeal.route("/wholesaledealclose/", methods=['GET', 'POST'])
def ret_wholesaledealclose():
    try:
        wholesale_deal_id = request.args.get('wholesale_deal_id', None)   
        UserName = session['username']
        Closed = request.args.get('Closed', None)   
        BookPrice = request.args.get('BookPrice', None)      
        ClosePrice = request.args.get('ClosePrice', None)   
        CloseDate = request.args.get('CloseDate', None)   
        sql = f"EXEC [WebSite].[WholeSaleDealCloseUpsert] @WholeSaleDealID = {wholesale_deal_id}, @Username  = '{UserName}', @Closed = {Closed}, @BookPrice = {BookPrice}, @ClosePrice = {ClosePrice}, @CloseDate = '{CloseDate}'"
        data, sts = sq.ret_pandas(sql) 
        if (sts!="SUCCESS"):
            json = jsonify({'Status': "FAILURE", "Identifier": wholesale_deal_id})
        else:
            sts = "FAILURE"
            for ind in data.index: 
                sts = data['Status'][ind]
                Identifier = wholesale_deal_id #data['IdentifierID'][ind]
            json = jsonify({'Status': sts, "Identifier": Identifier})            
        return json
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return jsonify({'Status': sts, "URL": "N/A"})              