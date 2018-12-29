### Overview
Access your RingCentral account's call log database using the call-log API.

### RingCentral Connect Platform
RingCentral Connect Platform is a rich RESTful API platform with more than 70 APIs for business communication includes advanced voice calls, chat messaging, SMS/MMS and Fax.

### RingCentral Developer Portal
To setup a free developer account, click [https://developer/ringcentral.com](here)

### Clone - Setup - Run the project
```
git clone https://github.com/ringcentral-tutorials/calllog-visualization-python-demo

cd calllog-visualization-python-demo

pip install ringcentral

pip install python-dotenv

pip install Flask==1.0.2

cp dotenv .env

FLASK_APP=index.py flask run
```
Remember to add your app client id and client secret as well as account login credentials to the .env file.

Open your Web browser and enter localhost:5000

## RingCentral Python SDK
The SDK is available at https://github.com/ringcentral/ringcentral-python
