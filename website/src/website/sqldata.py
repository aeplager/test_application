import pyodbc
import pandas as pd 
import json
import os
from . import api_general as ap

def connect_db():
    try:        
        #Driver = ap.ret_envvbl("Driver") #os.environ["Driver"]
        #Server = ap.ret_envvbl("SQLServer") #os.environ["SQLServer"]
        #Database = ap.ret_envvbl("Database") #os.environ["Database"]
        #Pwd = ap.ret_envvbl("PASSWRD") #os.environ["PWD"]
        #Uid =ap.ret_envvbl("UID") #os.environ["UID"]
        #PYODBC_Connection = 'DRIVER=' + Driver + ';SERVER=' + Server +  ';DATABASE=' + Database + ';UID=' + Uid + ';PWD=' + Pwd            
        PYODBC_Connection = ap.ret_envvbl("DBSVRConnectionString") #'DRIVER=' + Driver + ';SERVER=' + Server +  ';DATABASE=' + Database + ';UID=' + Uid + ';PWD=' + Pwd                    
        PYODBC_Connection = PYODBC_Connection.replace("dollardollar", "$")
        #PYODBC_Connection = os.environ["DBSVRConnectionString"]        
        #PYODBC_Connection2 = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=Bde-db-prod-03.cmv1nl5nsudc.us-east-1.rds.amazonaws.com;DATABASE=27434-DB;UID=Bridgelink-db;PWD=74zkRP7MUJQ!$h*W"
        #PYODBC_Connection = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=Dev3;UID=sa;PWD=G0gators;Connection Timeout=45'
        cnxn = pyodbc.connect(PYODBC_Connection)                        
        sts = "SUCCESS"
        return cnxn, sts
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)            
        return None, sts
  
def ret_pandas(sql, values = None):
    try:
        cnxn, sts = connect_db()   
        if (sts!="SUCCESS"):
            return None, "FAILURE-CNXN" + sts            
        if (values==None):
            df = pd.read_sql(sql, cnxn)                          
            cnxn.commit()
            cnxn.close()
        else:
            df = pd.read_sql(sql, cnxn, params=values)                
            cnxn.commit()
            cnxn.close()
        return df, "SUCCESS"
    except Exception as ex:                    
        return None, "FAILURE:  " + str(ex)        
def ret_json(sql, values = None):
    try:        
        data, sts = ret_pandas(sql, values)
        if (sts == "SUCCESS"):
            jsonstring = data.to_json(orient='index')
        else:
            sts = "FAILURE"
            jsonstring = None
        return jsonstring, sts          
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)        
        return None, sts   
def run_sql(sql):
    try:
        cnxn, sts = connect_db()
        if (sts=="SUCCESS"):
            cursor = cnxn.cursor()            
            cursor.execute(sql)
            cnxn.commit()
            cnxn.close()
            sts="SUCCESS"        
        return sts 
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)        
        return sts  
     
def connect_db_dev():
    try:        
        #Driver = ap.ret_envvbl("Driver") #os.environ["Driver"]
        #Server = ap.ret_envvbl("SQLServer") #os.environ["SQLServer"]
        #Database = ap.ret_envvbl("DevDB") #os.environ["Database"]
        #Pwd = ap.ret_envvbl("PASSWRD") #os.environ["PWD"]
        #Uid =ap.ret_envvbl("UID") #os.environ["UID"]        
        PYODBC_Connection = ap.ret_envvbl("DBSVRConnectionString") #'DRIVER=' + Driver + ';SERVER=' + Server +  ';DATABASE=' + Database + ';UID=' + Uid + ';PWD=' + Pwd                    
        cnxn = pyodbc.connect(PYODBC_Connection)
        sts = "SUCCESS"
        return cnxn, sts
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)            
        return None, sts       
    
def ret_pandas_dev(sql, values = None):
    try:
        cnxn, sts = connect_db_dev()   
        if (sts!="SUCCESS"):
            return None, "FAILURE-CNXN" + sts            
        if (values==None):
            df = pd.read_sql(sql, cnxn)                          
            cnxn.commit()
            cnxn.close()
        else:
            df = pd.read_sql(sql, cnxn, params=values)                
            cnxn.commit()
            cnxn.close()
        return df, "SUCCESS"
    except Exception as ex:                    
        return None, "FAILURE:  " + str(ex)  
     
def ret_json_dev(sql, values = None):
    try:        
        data, sts = ret_pandas_dev(sql, values)
        if (sts == "SUCCESS"):
            jsonstring = data.to_json(orient='index')
        else:
            sts = "FAILURE"
            jsonstring = None
        return jsonstring, sts          
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)        
        return None, sts  
         
def run_sql_dev(sql):
    try:
        cnxn, sts = connect_db_dev()
        if (sts=="SUCCESS"):
            cursor = cnxn.cursor()            
            cursor.execute(sql)
            cnxn.commit()
            cnxn.close()
            sts="SUCCESS"        
        return sts 
    except Exception as ex:            
        sts = "FAILURE:  " + str(ex)        
        return sts      