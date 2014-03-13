#!/usr/bin/env python
#-*- coding:UTF-8 -*-
#
# @author  Ritashugisha
# @contact ritashugisha@gmail.com
#
# This file is part of OmniTube.
#
# OmniTube is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OmniTube is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OmniTube. If not, see <http://www.gnu.org/licenses/>.

import sys, base64, json
import requests, splinter, urllib

"""
.. py:function:: isAuthorized()
Check if OmniTube is authorized to an account.

:returns: boolean OAUTH_JSON has been written
:rtype: boolean
"""
def isAuthorized():
	import OmniUtil
	return len(open(OmniUtil.OAUTH_JSON, 'r').read()) > 0
	
"""
.. py:function:: isValid()
Check if access token from OAUTH_JSON is valid

:returns: boolean OAUTH['access_token'] is valid
:rtype: boolean
"""
def isValid():
	import OmniUtil
	try:
		OmniUtil.jsonLoad(OmniUtil.BASE_PROFILE)
		return True
	except:
		return False
	
"""
.. py:function:: getOAuth()
Return the access specifications from OAUTH_JSON in json format

:returns: Dictionary of OAUTH_JSON data
:rtype: dict
"""
def getOAuth():
	import OmniUtil
	return json.loads(open(OmniUtil.OAUTH_JSON, 'r').read())

"""
.. py:function:: testAuthorization()
If OmniTube is not authorized (isAuthorized()) then begin authorization process.
"""
def testAuthorization():
	import OmniUtil
	if not isAuthorized():
		defaultBrowser = OmniUtil.getDefaultBrowser()
		if 'com.google.chrome' in defaultBrowser:
			newAuth = splinter.browser.Browser(driver_name = 'chrome', executable_path = '%s/Resources/webdrivers/chromedriver' % OmniUtil.WORKFLOW)
		elif 'org.mozilla.firefox' in defaultBrowser:
			newAuth = splinter.browser.Browser(driver_name = 'firefox')
		else:
			if OmniUtil.cocoaMsgBox('%s browser currently not supported!' % defaultBrowser, 
				'Your browser is not supported for authentication.\nOmniTube will default to Firefox to authenticate your profile.', '%sWarning.png' % OmniUtil.ICONS):
				newAuth = splinter.browser.Browser(driver_name = 'firefox')
			else:
				sys.exit(0)
		requestsLoad = {'client_id':base64.b64decode(OmniUtil.CLIENT_ID),
			'redirect_uri':'urn:ietf:wg:oauth:2.0:oob',
			'scope':'https://www.googleapis.com/auth/youtube',
			'response_type':'code',
			'access_type':'offline'}
		newAuth.visit('%s?%s' % (OmniUtil.BASE_OAUTH, urllib.urlencode(requestsLoad)))
		if 'Chrome' in newAuth.driver_name:
			OmniUtil.__runProcess__('osascript -e \'%s\'' % 'tell application "System Events" to tell process "Chrome" to set frontmost to true')
		else:
			OmniUtil.__runProcess__('osascript -e \'%s\'' % 'tell application "System Events" to tell process "firefox-bin" to set frontmost to true')
		while 'success code' not in newAuth.title.lower():
			pass
		requestsLoad = {'code':newAuth.title.split('=')[-1],
			'client_id':base64.b64decode(OmniUtil.CLIENT_ID),
			'client_secret':base64.b64decode(OmniUtil.CLIENT_SECRET),
			'redirect_uri':'urn:ietf:wg:oauth:2.0:oob',
			'grant_type':'authorization_code'}
		jsonBump = open(OmniUtil.OAUTH_JSON, 'w')
		jsonBump.write(urllib.urlopen(OmniUtil.BASE_OAUTH_TOKEN, urllib.urlencode(requestsLoad)).read())
		jsonBump.close()
		newAuth.quit()
		OmniUtil.introHtmlOpen()
		OmniUtil.introLoadThumbs()
	
"""
.. py:function:: refreshToken()
Refresh the access token if it is not valid (isValid()).
"""
def refreshToken():
	import OmniUtil
	if not isValid():
		requestsLoad = {'client_id':base64.b64decode(OmniUtil.CLIENT_ID),
			'client_secret':base64.b64decode(OmniUtil.CLIENT_SECRET),
			'refresh_token':getOAuth()['refresh_token'],
			'grant_type':'refresh_token'}
		newToken = json.loads(urllib.urlopen(OmniUtil.BASE_OAUTH_TOKEN, urllib.urlencode(requestsLoad)).read())
		jsonData = json.loads(open(OmniUtil.OAUTH_JSON, 'r').read())
		jsonData['access_token'] = newToken['access_token']
		jsonData['expires_in'] = newToken['expires_in']
		jsonBump = open(OmniUtil.OAUTH_JSON, 'w')
		jsonBump.write(json.dumps(jsonData))
		jsonBump.close()

"""
.. py:function:: validStart()
Makes sure that user is authorized and has a valid token before running.
"""
def validStart():
	testAuthorization()
	refreshToken()
			