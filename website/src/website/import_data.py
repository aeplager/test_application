import pandas as pd 
import json
import io
import openpyxl
from io import StringIO
import os
import xlrd
import pendulum
# Azure Installations
# from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
# from azure.common.credentials import ServicePrincipalCredentials
# from azure.mgmt.resource import ResourceManagementClient
# from azure.mgmt.datafactory import DataFactoryManagementClient
# from azure.mgmt.datafactory.models import *

def ret_base_pandas_dataframe():
    try:        
        data = {'FileName':  ['FileName'],
            'ValidateID': ['1'],
            'Field1': ['Field1'],         
            'Field2': ['Field2'],
            'Field3': ['Field3'],
            'Field4': ['Field4'],
            'Field5': ['Field5'],
            'Field6': ['Field6'],
            'Field7': ['Field7'],
            'Field8': ['Field8'],
            'Field9': ['Field9'],
            'Field10': ['Field10'],
            'Field11': ['Field11'],
            'Field12': ['Field12'],
            }
        dataBlank = {'FileName':  ['N/A'],
            'ValidateID': ['0'],
            'Field1': [''],         
            'Field2': [''],
            'Field3': [''],
            'Field4': [''],
            'Field5': [''],
            'Field6': [''],
            'Field7': [''],
            'Field8': [''],
            'Field9': [''],
            'Field10': [''],
            'Field11': [''],
            'Field12': [''],
            }
        fields = []
        fields.append('FileName')      
        fields.append('ValidateID')
        for i in range(1,13,1):
            fld = 'Field' + str(i)
            fields.append(fld)
            fld = [fld,'N/A']
        df = pd.DataFrame (data, columns = fields)
        dfAppend = pd.DataFrame(dataBlank, columns = fields)
        # for i in range (0,10,1):
        #     df = df.append(dfAppend)
        sts = "SUCCESS"
        return sts, df
    except Exception as ex:               
        sts = "FAILURE:  "  + str(ex)
        df = None
        return sts, df
# def pipeline_run_id_status(run_id):
#     try:
#         # Obtain credential information        
#         client_id = retEnvironmentVBL("client_id")
#         client_secret = retEnvironmentVBL("client_secret")                
#         tenant_id = retEnvironmentVBL("tenant_id")
#         resource_group = retEnvironmentVBL("resource_group")
#         data_factory_name = retEnvironmentVBL("data_factory_name")
#         container_name = retEnvironmentVBL("container_name")
#         subscription_id = retEnvironmentVBL("subscription_id")
#         # Establish Credential Control
#         dt_current = pendulum.now()
#         credentials = ServicePrincipalCredentials(client_id=client_id, secret=client_secret, tenant=tenant_id)        
#         resource_client = ResourceManagementClient(credentials, subscription_id)
#         adf_client = DataFactoryManagementClient(credentials, subscription_id)            
#         dt_diff_connection = dt_current.diff(pendulum.now()).in_seconds()
#         dt_current = pendulum.now()
#         pipeline_run = adf_client.pipeline_runs.get(resource_group, data_factory_name, run_id)
#         run_status = pipeline_run.status        
#         dt_diff_obtain = dt_current.diff(pendulum.now()).in_seconds()            
#         return "SUCCESS", run_id, run_status, str(dt_diff_connection), str(dt_diff_obtain)
#     except Exception as ex:               
#         return "FAILURE:  " + str(ex), run_id, run_status, None, None
    
def retEnvironmentVBL(EnvironVBLName):    
    retVBL = os.environ[EnvironVBLName]
    if retVBL[:2] == '= ':    
        retVBL = retVBL[2:] 
    retVBL = retVBL.strip()    
    return retVBL 

# def load_data_temptable(file_name, sheet_name = None, record_limit=None):
    try: 
        #cnxn, sts = ConnecttoDB()        
        #newString = '{"01": {"note": "This new stuff is very simple because were demonstrating only the mechanism."}}  '         
        # Odbc Container Stuff        
        begintime = pendulum.now()        
        container_name = retEnvironmentVBL('container_name')
        azure_conn_string = retEnvironmentVBL('azure_conn_string')
        blob_service_client = BlobServiceClient.from_connection_string(azure_conn_string)                
        container_client = blob_service_client.get_container_client(container_name)
        file_name = file_name.strip()
        file_extension = file_name[-4:].lower()
        file_extension_4 = file_name[-5:].lower()
        file_type = 'xls'
        num_cols = 0
        if (file_extension=='.csv'):
            # CSV
            file_type = 'CSV'
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
            blob = blob_client.download_blob().content_as_text()
            df = pd.read_csv(StringIO(blob))            
            sts = "SUCCESS"
        elif (file_extension=='.xls') or (file_extension_4==".xlsx"):
            file_type = 'Excel'
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
            blob = blob_client.download_blob().content_as_bytes()
            begintime = pendulum.now()   
            cols =[0,1,2,3,4,5,6,7,8,9,10,11,12]            
            df = pd.read_excel(blob, sheet_name=sheet_name, usecols=cols, nrows=2000)
            endtime = pendulum.now()           
            delta = begintime - endtime
            deltaseconds = delta.seconds                
            sts = "SUCCESS"
        else:
            sts = "File Format Is Not Correct"
        if (sts == "SUCCESS"):
            # blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
            # blob = blob_client.download_blob().content_as_bytes()
            # df = pd.read_excel(blob)        
            # Limit the import to 10,000 records for             #
            if (record_limit==None):
                record_limit = int(retEnvironmentVBL('record_limit'))            
            else:
                record_limit = int(record_limit)
            if (record_limit != 0):                
                df = df.head(record_limit)
            ln = len(df.columns)
            num_cols = ln
            for iCol in range(0,ln,1):        
                colName = df.columns[iCol]                        
                #print(colName)  
                df[colName] = df[colName].astype('str') 
                newColName = "Field" + str(iCol+1)
                df.rename(columns = {colName:newColName}, inplace = True) 
                iColStart = iCol+1         
            df["ValidateID"] = 1                  
            df["FileName"] = file_name       
            name_order=[]                    
            name_order.append("FileName")
            name_order.append("ValidateID")
            for iCol in range(0,ln,1):
                colName = "Field" + str(iCol+1)
                name_order.append(colName)     
            df = pd.DataFrame(df,columns=name_order)   
        dataBlank = {'FileName':  ['N/A'],
            'ValidateID': ['0'],
            'Field1': [''],         
            'Field2': [''],
            'Field3': [''],
            'Field4': [''],
            'Field5': [''],
            'Field6': [''],
            'Field7': [''],
            'Field8': [''],
            'Field9': [''],
            'Field10': [''],
            'Field11': [''],
            'Field12': [''],
            }
        dfAppend = pd.DataFrame(dataBlank, columns = name_order)
        # for i in range (0,10,1):
        #     df = df.append(dfAppend)                     
        for iCol in range(ln,12,1):
            colName = "Field" + str(iCol+1)
            df[colName] = None
        #sts = LoadDataTableAnyTable(df)
        endtime = pendulum.now()
        delta = begintime - endtime
        deltaseconds = delta.seconds
        sts = "Uploaded " + sts + " for file " + file_name + " processed in " + str(deltaseconds)
        rsts, run_response = call_data_factory_general(file_name, file_type, sheet_name, num_cols)
        df["run_id"] = run_response.run_id
        sts = "SUCCESS"# + str(rsts)            
        return sts, df
    except Exception as ex:               
        sts = "FAILURE:  "  + str(ex)
        return 
# def obtain_sheets_excel(file_name):
    try:        
        """
            Based on Excel file, this returns 
            a JSON of the SHEETS from the Excel
        """
        begintime = pendulum.now()        
        container_name = retEnvironmentVBL('container_name')
        azure_conn_string = retEnvironmentVBL('azure_conn_string')
        blob_service_client = BlobServiceClient.from_connection_string(azure_conn_string)                
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
        blob = blob_client.download_blob().content_as_bytes()
        wb = openpyxl.load_workbook(filename = io.BytesIO(blob), read_only=True, keep_links=False)
        sheets = wb.sheetnames
        for i in range(0,len(sheets),1):
            dataBlank = {'SheetName':  [sheets[i]]}
            if (i==0):                
                dfBase = pd.DataFrame(dataBlank)
            else:
                dfAppend = pd.DataFrame(dataBlank)
                dfBase = dfBase.append(dfAppend)
        sts="SUCCESS", dfBase
        return sts
    except Exception as ex:               
        sts = "FAILURE:  "  + str(ex), None
        return 

# def call_data_factory_general(file_name, file_type, sheet_name, num_cols):
    try:
        # Establish Variables
        client_id = retEnvironmentVBL("client_id")
        client_secret = retEnvironmentVBL("client_secret")                
        tenant_id = retEnvironmentVBL("tenant_id")
        resource_group = retEnvironmentVBL("resource_group")
        data_factory_name = retEnvironmentVBL("data_factory_name")
        container_name = retEnvironmentVBL("container_name")
        subscription_id = retEnvironmentVBL("subscription_id")
        # Establish Control
        dt_current= pendulum.now()
        credentials = ServicePrincipalCredentials(client_id=client_id, secret=client_secret, tenant=tenant_id)
        p_name = ""
        if (num_cols<10):
            p_name = "pip_" + file_type + "_Table_0" + str(num_cols)
        else:
            p_name = "pip_" + file_type + "_Table_" + str(num_cols)
        resource_client = ResourceManagementClient(credentials, subscription_id)
        adf_client = DataFactoryManagementClient(credentials, subscription_id)            
        run_response = adf_client.pipelines.create_run(resource_group, data_factory_name, p_name, parameters={"FileName": file_name, "SheetName": sheet_name, "Container": container_name})
        ln = dt_current.diff(pendulum.now()).in_seconds()        
        sts = "SUCCESS"
        return sts, run_response
    except Exception as ex:    
        return 'FAILURE', None 
   
# def call_data_factory_wholesaleblock(file_name, file_type, block_type, sheet_name, wholesaledeal_id):
#     try:
#         # Establish Variables
#         client_id = retEnvironmentVBL("client_id")
#         client_secret = retEnvironmentVBL("client_secret")                
#         tenant_id = retEnvironmentVBL("tenant_id")
#         resource_group = retEnvironmentVBL("resource_group")
#         data_factory_name = retEnvironmentVBL("data_factory_name")
#         container_name = retEnvironmentVBL("container_name")
#         subscription_id = retEnvironmentVBL("subscription_id")
#         # Establish Control
#         dt_current= pendulum.now()
#         credentials = ServicePrincipalCredentials(client_id=client_id, secret=client_secret, tenant=tenant_id)        
#         p_name = "pip_" + file_type + "_Table_" + block_type        
#         resource_client = ResourceManagementClient(credentials, subscription_id)
#         adf_client = DataFactoryManagementClient(credentials, subscription_id)            
#         run_response = adf_client.pipelines.create_run(resource_group, data_factory_name, p_name, parameters={"FileName": file_name, "SheetName": sheet_name, "Container": container_name, "WholeSaleDealID":  str(wholesaledeal_id)})
#         ln = dt_current.diff(pendulum.now()).in_seconds()        
#         sts = "SUCCESS"
#         return sts, run_response
#     except Exception as ex:    
#         return 'FAILURE:  ' + str(ex), None 
   

     
# def wholesaleblock_import(file_name, sheet_name, wholesale_id, hourly_block="hourly"):
#     try:
#         begintime = pendulum.now() 
#         if (sheet_name == None):
#             sheet_name = 'CSV'
#         container_name = retEnvironmentVBL('container_name')
#         azure_conn_string = retEnvironmentVBL('azure_conn_string')
#         blob_service_client = BlobServiceClient.from_connection_string(azure_conn_string)                
#         container_client = blob_service_client.get_container_client(container_name)
#         client_id = retEnvironmentVBL("client_id")
#         client_secret = retEnvironmentVBL("client_secret")                
#         tenant_id = retEnvironmentVBL("tenant_id")
#         resource_group = retEnvironmentVBL("resource_group")
#         data_factory_name = retEnvironmentVBL("data_factory_name")
#         container_name = retEnvironmentVBL("container_name")
#         subscription_id = retEnvironmentVBL("subscription_id")
#         sts = "SUCCESS"
#         run_response = 'N/A'
#         file_name = file_name.strip()
#         file_extension = file_name[-4:].lower()
#         file_extension_4 = file_name[-5:].lower()
#         file_type = 'xls'
#         num_cols = 0
        
#         if (file_extension=='.csv'):
#             # CSV
#             file_type = 'CSV'
#             sheet_name = file_type
#             blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
#             blob = blob_client.download_blob().content_as_text()
#             df = pd.read_csv(StringIO(blob))            
#             sts = "SUCCESS"
#         elif (file_extension=='.xls') or (file_extension_4==".xlsx"):
#             file_type = 'Excel'
#             blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
#             blob = blob_client.download_blob().content_as_bytes()
#             begintime = pendulum.now()   
#             cols =[0,1,2,3,4,5,6,7,8,9,10,11,12]            
#             df = pd.read_excel(blob, sheet_name=sheet_name, usecols=cols, nrows=2000)
#             endtime = pendulum.now()           
#             delta = begintime - endtime
#             deltaseconds = delta.seconds                
#             sts = "SUCCESS"
#         else:
#             sts = "FAILURE"            
#         if (sts != "FAILURE"):
#          ## Imported into Pandas Data Frame         
#             # Establish Control
#             dt_current= pendulum.now()
#             credentials = ServicePrincipalCredentials(client_id=client_id, secret=client_secret, tenant=tenant_id)
#             p_name = ""                        
#             if (sheet_name == 'CSV'):
#                 p_name = "pip_CSV_Table_WholeSaleBlockCustom"
#             else:
#                 p_name = "pip_Excel_Table_WholeSaleBlockCustom"
#             if (hourly_block=="block"):
#                 if (sheet_name == 'CSV'):
#                     p_name = "pip_CSV_Table_WholeSaleBlockCustomBlock"
#                 else:
#                     p_name = "pip_Excel_Table_WholeSaleBlockCustomBlock"                
#             elif (hourly_block == "block_wide"):
#                 if (sheet_name == 'CSV'):
#                         p_name = "pip_CSV_Table_WholeSaleBlockCustomBlockWide"
#                 else:
#                     p_name = "pip_Excel_Table_WholeSaleBlockCustomBlockWide"                
#             resource_client = ResourceManagementClient(credentials, subscription_id)
#             adf_client = DataFactoryManagementClient(credentials, subscription_id)            
#             run_response = adf_client.pipelines.create_run(resource_group, data_factory_name, p_name, parameters={"FileName": file_name, "SheetName": sheet_name, "Container": container_name, "WholeSaleDealID":  wholesale_id})
#             ln = dt_current.diff(pendulum.now()).in_seconds()        
#             sts = "SUCCESS"
#         else:
#             sts = "FAILURE"                            
#         return sts, run_response
#     except Exception as ex:    
#         sts = "FAILURE:  " + str(ex)
#         run_response = None
#         #json_response = {"Status": sts}    
#         #y = json.dumps(json_response)
#         return sts, run_response

            
### DELETE DOWN HERE###############
def ReturnValues():
    return 'Test Values'