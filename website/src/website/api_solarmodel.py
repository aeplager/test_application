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


api_solarmodel = Blueprint('api_solarmodel', __name__)

@api_solarmodel.route("/return_all", methods=['GET', 'POST'])
def ret_solarmodel_all():
    try:    
        if au.login_check() == False:
            return ap.generic_json_error()
        else:      
            stored_procedure = request.args.get('stored_procedure', 0) 
            sql = "EXEC " + stored_procedure
            js, sts = sq.ret_json(sql)        
            if (sts!="SUCCESS"):
                js = jsonify({'Status': "FAILURE", "StoredProcedure": stored_procedure})
            return js
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return jsonify({'Status': sts, "Identifier": 0})               
    
@api_solarmodel.route("/return_USAF", methods=['GET', 'POST'])    
def ret_solarmodel_USAF():
    try:
        if au.login_check() == False:
            return ap.generic_json_error()
        else:              
            USAF_StationID = request.args.get('USAF_StationID',None)
            state = request.args.get('state', None) 
            sql = 'EXEC [WebSite].[USAFGetInfo] '
            if (USAF_StationID!=None):
                sql = sql + '@USAF_StationID = ' + USAF_StationID
                if (state!=None):
                    sql = sql + ","
            if (state!=None):
                sql = sql + "@State = '" + state + "'"            
            js, sts = sq.ret_json(sql)  
            if (sts!="SUCCESS"):
                return jsonify({'Status': sts, "Procedure": "return_USAF"})                       
            else:
                return js
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return jsonify({'Status': sts, "Identifier": 0})   
    
@api_solarmodel.route("/change_deal", methods=['GET', 'POST'])    
def ret_change_deal():
    try:
        if au.login_check() == False:
            return ap.generic_json_error()
        else:    
            deal_id = request.args.get('deal_id',0)
            if (deal_id==None):
                deal_id = 0
            sql =  'EXEC [Solar].[ClearGraphInfo] @DealID=' + deal_id
            sts="SUCCESS"
            sts = sq.run_sql(sql)
            return jsonify({'Status': sts, "TypeOfRecord": "ChangeDeal"})  
        return sts
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return jsonify({'Status': sts, "Identifier": 0})       
        
@api_solarmodel.route("/obtaintable", methods=['GET', 'POST'])     
def ret_solar_table():
    try:
        if au.login_check() == False:
            return ap.generic_json_error()
        else:  
            js = jsonify({'Status': "FAILURE", "Identifier": 0})   
            deal_id = request.args.get('deal_id',0)
            if (deal_id==None):
                deal_id = 0                
            sql =  'EXEC [Solar].[TablesGetInfo_Test] @DealID=' + deal_id
            js_ret, sts = sq.ret_json(sql)                          
            if (sts=="SUCCESS"):
                js = js_ret
            return js            
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return jsonify({'Status': sts, "Identifier": 0}) 

@api_solarmodel.route("/obtaingraph", methods=['GET', 'POST'])     
def ret_solar_graph():
    try:
        if au.login_check() == False:
            return ap.generic_json_error()
        else:  
            js = jsonify({'Status': "FAILURE", "Identifier": 0})   
            deal_id = request.args.get('deal_id',0)
            if (deal_id==None):
                deal_id = 0
            sql =  'EXEC [Solar].[GraphsGetInfo_NEW] @DealID=' + deal_id
            js_ret, sts = sq.ret_json(sql)                          
            if (sts=="SUCCESS"):
                js = js_ret
            return js            
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return jsonify({'Status': sts, "Identifier": 0}) 
        
@api_solarmodel.route("update_test", methods=['GET', 'POST'])    
def ret_solarmodel_test():  
    try:
        if au.login_check() == False:
            return ap.generic_json_error()
        else:    
            deal_id = request.args.get('deal_id',0)
            if (deal_id==None):
                deal_id = 0
            deal_name = request.args.get('deal_name','N/A')                        
            set_point_id = request.args.get('set_point_id',0)
            set_loc_id = request.args.get('set_loc_id',0)
            start_date = request.args.get('start_date',None)
            end_date = request.args.get('end_date',None)            
            firm_cont = request.args.get('firm_cont','firm')
            cap_factor = request.args.get('cap_factor',0)
            disc_rate = request.args.get('disc_rate',0)
            capacity = request.args.get('capacity',0)       
            sql =  'EXEC [Solar].[DealUpsert] @DealID=' + deal_id
            sql = sql + ",@DealName='" + deal_name + "'"
            sql = sql + ",@SettlementPointID=" + set_point_id
            sql = sql + ",@SettlementLocationID=" + set_loc_id
            sql = sql + ",@StartDate='" + start_date + "'"
            sql = sql + ",@EndDate='" + end_date + "'"         
            sql = sql + ",@CapacityFactor=" + cap_factor
            sql = sql + ",@FirmContingent='" + firm_cont + "'"
            sql = sql + ",@DiscountRate=" + disc_rate
            sql = sql + ",@Capacity=" + capacity
            df, sts = sq.ret_pandas(sql)
            if (sts=="SUCCESS"):
                df['Status'] = sts
                js = df.to_json(orient='index')
                return js
            else:
                return jsonify({'Status': sts, "TypeOfRecord": "UpdateDate"})        
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return jsonify({'Status': sts, "TypeOfRecord": "UpdateDate"})                    
@api_solarmodel.route("/save_USAF", methods=['GET', 'POST'])    

def ret_solarmodel_USAF_update():  
    try:
        if au.login_check() == False:
            return ap.generic_json_error()
        else:    
            deal_id = request.args.get('deal_id',0)
            if (deal_id==None):
                deal_id = 0
            deal_name = request.args.get('deal_name','N/A')
            usaf_station_name = request.args.get('usaf_station_name','N/A')
            market_id = request.args.get('market_id',1)
            set_point_id = request.args.get('set_point_id',0)
            set_loc_id = request.args.get('set_loc_id',0)
            start_date = request.args.get('start_date',None)
            end_date = request.args.get('end_date',None)            
            firm_cont = request.args.get('firm_cont','firm')
            cap_factor = request.args.get('cap_factor',0)
            disc_rate = request.args.get('disc_rate',0)
            capacity = request.args.get('capacity',0)       
            if (market_id == None):
                market_id = 1
            elif (int(market_id) <=0):
                market_id = 1
            sql =  'EXEC [Solar].[DealUpsert] @DealID=' + deal_id
            sql = sql + ",@DealName='" + deal_name + "'"
            sql = sql + ",@MarketID='" + market_id + "'"
            sql = sql + ",@USAF_StationName='" + usaf_station_name + "'"
            sql = sql + ",@SettlementPointID=" + set_point_id
            sql = sql + ",@SettlementLocationID=" + set_loc_id
            sql = sql + ",@StartDate='" + start_date + "'"
            sql = sql + ",@EndDate='" + end_date + "'"         
            sql = sql + ",@CapacityFactor=" + cap_factor
            sql = sql + ",@FirmContingent='" + firm_cont + "'"
            sql = sql + ",@DiscountRate=" + disc_rate
            sql = sql + ",@Capacity=" + capacity
            df, sts = sq.ret_pandas(sql)
            if (sts=="SUCCESS"):
                df['Status'] = sts
                js = df.to_json(orient='index')
                return js
            else:
                return jsonify({'Status': sts, "TypeOfRecord": "UpdateDate"})        
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)   
        return jsonify({'Status': sts, "TypeOfRecord": "UpdateDate"})            