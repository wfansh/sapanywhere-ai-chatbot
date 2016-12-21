#!/usr/bin/env python

import urllib
import json
import os

import httplib
from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)



api_key = 'DukY4kB5FjKn4DMMbqpXiei37yo21Gnz'
api_secret = 'PIi7Wab2wtLAEKXjDoD9W2LKzuyWwH85'
refresh_token = '9ffbe34-b169-49e4-8b47-5cf31d7805e9'
api_endpoint = 'https://api.sapanywhere.com/v1/'
auth_endpoint = 'https://go.sapanywhere.com/oauth2/token'


@app.route('/webhook', methods=['POST', 'GET'] )
def webhook():
    req = request.get_json(silent = True, force = True)

    print("Request:")
    print(json.dumps(req, indent = 4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent = 4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "lead.create":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    customer = parameters.get("customer")


    speech = "Create sales lead for customer " + customer

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


def httpTest():
	http_client = httplib.HTTPConnection('127.0.0.1', 8080, timeout = 30)
	http_client.request('GET', '/contextio-showcase')

	response = http_client.getresponse()
	print response.read()



if __name__ == '__main__':

    port = int(os.getenv('PORT', 5000))

    httpTest()


    print "Starting app on port %d" % port

    app.run(debug = True, port = port, host = '127.0.0.1')
