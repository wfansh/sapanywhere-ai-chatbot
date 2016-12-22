#!/usr/bin/env python

import urllib
import json
import os
import anw

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)
anw.init()



@app.route('/webhook', methods=['POST', 'GET'] )
def webhook():
    req = request.get_json(silent = True, force = True)

    print("Request:%s" %json.dumps(req, indent = 4))

    resp = makeWebhookResult(req)
    resp = json.dumps(resp, indent = 4)
    print(resp)
    
    r = make_response(resp)
    r.headers['Content-Type'] = 'application/json'
    return r


def makeWebhookResult(req):
	result = req.get('result')
	action = result.get('action')

	print 'Action : %s' %action

	if action == 'action.show.topN' :
		print 'Resolved Query : %s' %result.get('resolvedQuery')

		api = result.get('parameters').get('api')[0]
		number = result.get('parameters').get('number')[0]

		resp = anw.topN(api, number)

		print resp

		speech = 'Top ' + str(number) + ' ' + api + ' are : '

		for obj in resp :
			if api == 'Customers' :
				speech += obj.get('displayName')
			elif api == 'SKUs' :
				speech += obj.get('name')
			elif api == 'SalesOrders' :
				speech += obj.get('docNumber')

			speech += ', '

		return {
			'speech' : speech,
			'displayText' : speech,
			# 'data' : {},
			# 'contextOut' : [],
			'source' : 'sapanywhere-ai-showcase'
		}


	else :
		return {}


if __name__ == '__main__':

    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')

