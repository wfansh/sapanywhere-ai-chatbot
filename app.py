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

	if action == 'CreateLead':
		speech = handleCreateLead(result)
		return {
			'speech' : speech,
			'displayText' : speech,
			#'resetContexts': true,
			#'data' : {},
			#'contextOut' : [],
			'source' : 'sapanywhere-ai-showcase'
		}
	
	if action == 'CreateLead_hot':
		speech = handleCreateLead_hot(result)
		return {
			'speech' : speech,
			'displayText' : speech,
			#'resetContexts': true,
			#'data' : {},
			#'contextOut' : [],
			'source' : 'sapanywhere-ai-showcase'
		}
	
	if action == 'CreateLead_warm':
		speech = handleCreateLead_warm(result)
		return {
			'speech' : speech,
			'displayText' : speech,
			#'resetContexts': true,
			#'data' : {},
			#'contextOut' : [],
			'source' : 'sapanywhere-ai-showcase'
		}

	elif action == 'Report_TopN':
		speech = handleShowTopN(result)
		return {
			'speech' : speech,
			'displayText' : speech,
			# 'data' : {},
			#'contextOut' : [],
			'source' : 'sapanywhere-ai-showcase'
		}

	else:
		return {}





def handleCreateLead(result):
	print 'Resolved Query : %s' %result.get('resolvedQuery')

	for context in result.get('contexts'):
		if context.get('name') != 'createleadforcustomer':
			continue

		customer = context.get('parameters').get('CustomerName')
		description =  context.get('parameters').get('any1')
		qualification = context.get('parameters').get('Qualification').upper()
		mobile = context.get('parameters').get('number')

		resp = anw.createLead(customer, description, qualification, mobile)
		print resp

		return  'Create lead %s for %s, qualification is %s' %(resp, customer, qualification)
			

def handleCreateLead_hot(result):
	print 'Resolved Query : %s' %result.get('resolvedQuery')

	
		

	customer = result.get('parameters').get('CustomerName')
	description =  result.get('resolvedQuery')
	qualification = 'HOT'
	
	
	resp = anw.createLead_quick(customer, description, qualification)
	print resp

	return  'Create lead %s for %s, qualification is hot' %(resp, customer)


def handleCreateLead_warm(result):
	print 'Resolved Query : %s' %result.get('resolvedQuery')

	
		

	customer = result.get('parameters').get('CustomerName')
	description =  result.get('resolvedQuery')
	qualification = 'WARM'
	
	
	resp = anw.createLead_quick(customer, description, qualification)
	print resp

	return  'Create lead %s for %s, qualification is hot' %(resp, customer)
		

def handleShowTopN(result):
	print 'Resolved Query : %s' %result.get('resolvedQuery')
	
	api = result.get('parameters').get('masterdata')
	number = result.get('parameters').get('number')
	
	resp = anw.topN(api, int(number))
	print resp

	speech = 'Top ' + str(number) + ' ' + api + ' are : '

	for obj in resp :
		if api == 'Customers' :
			speech += obj.get('displayName')
		elif api == 'SKUs' :
			speech += obj.get('name')
		elif api == 'Products' :
			speech += obj.get('name')
		elif api == 'Opportunities' :
			speech += obj.get('description')
		elif api == 'SalesOrders' :
			speech += obj.get('docNumber')

		speech += ', '

	return speech




if __name__ == '__main__':

    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')

