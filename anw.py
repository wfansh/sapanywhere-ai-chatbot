import urllib
import urllib2
from urllib2 import *
import json

api_key = '0039877539884067-YP7qaphskKrdH6p2io8tHaV2BG8oHuMA'
api_secret = 'mZF6DNHGp5S4uzFBT-ML96GoRZ3F'
refresh_token = '32f9b637-1079-492d-b414-94f83811d692'
api_endpoint = 'https://api.sapanywhere.cn:443/v1/'
auth_endpoint = 'https://my.sapanywhere.cn:443/oauth2/token/'

global access_token


def init():
	try : 
		# Retrieve access token
		req = urllib2.Request(auth_endpoint)
		req.add_header('Content-Type', 'application/x-www-form-urlencoded')
		
		data = urllib.urlencode({'client_id' : api_key, 'client_secret' : api_secret, 'grant_type' : 'refresh_token', 'refresh_token' : refresh_token})
		resp = urllib2.urlopen(req, data).read()

		global access_token
		access_token = json.loads(resp).get('access_token')
		
		print 'respones : %s'  %resp
		print 'access token : %s'  %access_token
		return 0

	except URLError, e:
		print e.reason()
		return -1


def topN(api, n):
	global access_token
	
	print 'Show top %d of %s.' % (n, api)

	try:
		param = urllib.urlencode({'access_token' : access_token, 'limit' : str(n)})
		resp = urllib2.urlopen(api_endpoint + api + '?' + param).read()

		return json.loads(resp)
	except URLError as e: 
		print e.reason()
		return None