from ringcentral import SDK
import os
import json
from dotenv import load_dotenv
dotenv_path = '.env'
load_dotenv(dotenv_path)
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
platform = None
# if __name__ == "__main__":
#     app.run()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/readlog', methods=['GET'])
def login():
    print("logging in...")
    access = request.args.get('access', "account")
    params = request.args.get('params', "default")
    global platform
    if os.environ.get("ENVIRONMENT_MODE") == "sandbox":
        sdk = SDK(os.environ.get("CLIENT_ID_SB"), os.environ.get("CLIENT_SECRET_SB"), 'https://platform.devtest.ringcentral.com')
        platform = sdk.platform()
        platform.login(os.environ.get("USERNAME_SB"), '', os.environ.get("PASSWORD_SB"))
    else:
        sdk = SDK(os.environ.get("CLIENT_ID_PROD"), os.environ.get("CLIENT_SECRET_PROD"), 'https://platform.ringcentral.com')
        platform = sdk.platform()
        platform.login(os.environ.get("USERNAME_PROD"), '', os.environ.get("PASSWORD_PROD"))
    res = readCallLogs(access, params)
    return json.dumps(res)


def readCallLogs(access, params) :
    global platform
    configs = json.loads(params)
    endpoint = "";
    if access == "account":
        endpoint = '/account/~/call-log';
    else:
        endpoint = '/account/~/extension/~/call-log';

    try:
        response = platform.get(endpoint, configs)
        jsonObj = json.loads(response.response()._content)
        return jsonObj['records']
    except Exception as e:
        error = str(e)
        if error.find("ReadCompanyCallLog") != -1:
            errorRes = {"calllog_error":"You do not have admin role to access account level. You can choose the extension access level."}
            return errorRes
        else:
            errorRes = {"calllog_error":"Cannot access call log."}
            return errorRes
