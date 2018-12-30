from ringcentral import SDK
import os
import json
from dotenv import load_dotenv
dotenv_path = '.env'
load_dotenv(dotenv_path)
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
platform = None

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/readlog', methods=['GET'])
def login():
    global platform
    if os.environ.get("ENVIRONMENT_MODE") == "sandbox":
        rcsdk = SDK(os.environ.get("CLIENT_ID_SB"), os.environ.get("CLIENT_SECRET_SB"), 'https://platform.devtest.ringcentral.com')
        username = os.environ.get("USERNAME_SB")
        pwd = os.environ.get("PASSWORD_SB")
    else:
        rcsdk = SDK(os.environ.get("CLIENT_ID_PROD"), os.environ.get("CLIENT_SECRET_PROD"), 'https://platform.ringcentral.com')
        username = os.environ.get("USERNAME_PROD")
        pwd = os.environ.get("PASSWORD_PROD")
    platform = rcsdk.platform()
    
    try:
        platform.login(username, '', pwd)
        res = readCallLogs()
        return json.dumps(res)
    except Exception as e:
        errorRes = {"calllog_error":"Cannot login."}
        return errorRes

def readCallLogs() :
    global platform
    access = request.args.get('access', "account")
    endpoint = "/account/~/extension/~/call-log";
    if access == "account":
        endpoint = "/account/~/call-log";

    try:
        params = request.args.get('params', None)
        if params != None:
            configs = json.loads(params)
            response = platform.get(endpoint, configs)
            jsonObj = json.loads(response.response()._content)
            return jsonObj['records']
        else:
            errorRes = {"calllog_error":"Mising query parameters"}
            return errorRes
    except Exception as e:
        error = str(e)
        if error.find("ReadCompanyCallLog") != -1:
            errorRes = {"calllog_error":"You do not have admin role to access account level. You can choose the extension access level."}
            return errorRes
        else:
            errorRes = {"calllog_error":"Cannot access call log."}
            return errorRes
