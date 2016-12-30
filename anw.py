import urllib
import urllib2
from urllib2 import *
import json

api_key = '6332966829882765-iLZhFHwdTLS5B9XUqPrgzZYF38VLpvF3'
api_secret = 'PA16KvqFCeIs5QAcKueaHII0kBET'
refresh_token = '77b34ce2-4141-4adb-8943-e6d200294e12'
api_endpoint = 'https://api-us.sapanywhere.com:443/v1/'
auth_endpoint = 'https://my-us.sapanywhere.com:443/oauth2/token/'

global access_token


def init():
	try : 
		# Retrieve access token
		data = urllib.urlencode({'client_id' : api_key, 'client_secret' : api_secret, 'grant_type' : 'refresh_token', 'refresh_token' : refresh_token})
		req = urllib2.Request(auth_endpoint, data, {'Content-Type' : 'application/x-www-form-urlencoded'})		
		resp = urllib2.urlopen(req).read()

		global access_token
		access_token = json.loads(resp).get('access_token')
		
		print 'respones : %s'  %resp
		print 'access token : %s'  %access_token
		return 0

	except URLError, e:
		print e.reason
		return -1


def topN(api, n):
	global access_token
	
	print 'Show top %d of %s.' % (n, api)

	try:
		param = urllib.urlencode({'access_token' : access_token, 'limit' : str(n)})
		resp = urllib2.urlopen(api_endpoint + api + '?' + param).read()

		return json.loads(resp)
	except URLError as e: 
		print e.reason
		return None


def createLead(customer, description, qualification, mobile):
	global access_token

	print 'Create Lead for %s, %s, %s, %s' %(customer,description, qualification, mobile)

	try :
		data = json.dumps({'description' : description, 'qualification' : qualification, 'status' : 'OPEN', 'relatedName' : customer, 'relatedType' : 'CUSTOMER', 'mobile' : mobile})
		req = urllib2.Request(api_endpoint + 'Leads?access_token=' + access_token, data, {'Content-Type' : 'application/json'})
		resp = urllib2.urlopen(req)

		return resp.read()

	except URLError as e:
		print e.reason
		return None
	
def createLead_hot(customer, description, qualification):
	global access_token

	print 'Create Lead for %s, %s, %s, %s' %(customer,description, qualification)

	try :
		data = json.dumps({'description' : description, 'qualification' : qualification, 'status' : 'OPEN', 'relatedName' : customer, 'relatedType' : 'CUSTOMER'})
		req = urllib2.Request(api_endpoint + 'Leads?access_token=' + access_token, data, {'Content-Type' : 'application/json'})
		resp = urllib2.urlopen(req)

		return resp.read()

	except URLError as e:
		print e.reason
		return None

if __name__ == '__main__':
	init()
	# createLead('FAN', 'EXHIBITION', 'WARM', '12356')

	print topN('Customers', 5)
