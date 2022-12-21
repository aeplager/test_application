FROM python:3.8.8-buster as base

# Environment Variables 
ENV container_name = "container_name"
ENV azure_conn_string = "azure_conn_string"
ENV DBSVRConnectionString = "DBSVRConnectionString"
ENV File_Docker_URL = "File_Docker_URL"
ENV Azure_Function_URL = "Azure_Function_URL"

ENV super_user_user_name = test@vrdsoft.com
ENV super_user_pwd = test
ENV outgoing_email = test@qkss.com
ENV outgoing_pwd = pwd
ENV container_name=vrd

#ENV record_limit = 2000
# Special code for PYODBC
RUN apt-get update && apt-get install -y gcc unixodbc-dev
###############################################
# Begin Special Code for ODBC Drivers
###############################################
# See about installing ODBC drivers here: https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2017
# Note that the driver version installed needs to match the version used in the code
# In this case for Ubuntu 18.04: ODBC SQL driver 17
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update -y
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev mssql-tools

###############################################
# End Special Code for ODBC Drivers
###############################################

RUN mkdir /work/
WORKDIR /work/
RUN pip install --upgrade pip
RUN pip install pyodbc
#RUN pip install openpyxl
RUN pip install Flask-Cors
RUN pip install requests

COPY ./src/requirements.txt /work/requirements.txt
RUN pip install azure-storage-blob
RUN pip install -r requirements.txt
RUN pip install openpyxl
EXPOSE 5000
#COPY ./src/ /work/
COPY ./src /work/
ENV FLASK_APP=application.py
# Soemthing else
###########START NEW IMAGE : DEBUGGER ###################
FROM base as debug
RUN pip install ptvsd


WORKDIR /work/
CMD python -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess -m flask run -h 0.0.0 -p 5000

###########START NEW IMAGE: PRODUCTION ###################
FROM base as prod
WORKDIR /work/
CMD flask run -h 0.0.0 -p 5000