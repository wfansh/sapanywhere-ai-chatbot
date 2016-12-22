import urllib
import urllib2
from urllib2 import *
import json

api_key = 'DukY4kB5FjKn4DMMbqpXiei37yo21Gnz'
api_secret = 'PIi7Wab2wtLAEKXjDoD9W2LKzuyWwH85'
refresh_token = '9ffbe34-b169-49e4-8b47-5cf31d7805e9'
api_endpoint = 'https://api.sapanywhere.com/v1/'
auth_endpoint = 'https://go.sapanywhere.com/oauth2/token'
access_token = None


def init():
	print "asfsdafs"
	#try : 
	# Retrieve access token
	req = urllib2.Request(auth_endpoint)
	req.add_header('Content-Type', 'application/x-www-form-urlencoded')
	req.add_header('User-Agent', 'Mozilla/5.0')
	data = urllib.urlencode({'client_id' : api_key, 'client_secret' : api_secret, 'grant_type' : 'refresh_token', 'refresh_token' : refresh_token})
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	response = opener.open(req, data)

	print response
	print response.read()
	return 0
#	except URLError, e:
#		print e
#		return -1
	
