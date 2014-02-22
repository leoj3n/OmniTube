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

import os, requests, base64
import OmniUtil, OmniAuth

"""
.. py:function:: getFeed()
Get the authenticated user's subscription's upload feed.

:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""
def getFeed():
	feed = OmniUtil.Feedback()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_FEED)
	if gdataResults:
		for i in gdataResults:
			if not os.path.exists('%s%s.jpg' % (OmniUtil.SUBSCRIPTIONS, i['author'][0]['yt$userId']['$t'])):
				OmniUtil.retrieveThumb(i['author'][0]['yt$userId']['$t'])
			feed.add_item(i['title']['$t'], '%s - %s' % (i['author'][0]['name']['$t'], 
				OmniUtil.secondsToHuman(int(i['media$group']['yt$duration']['seconds']))), 
				'http://www.youtube.com/watch?v=%s' % i['media$group']['yt$videoid']['$t'], '', '', 
				'%s%s.jpg' % (OmniUtil.SUBSCRIPTIONS, i['author'][0]['yt$userId']['$t']))
	else:
		feed.add_item('No Results', 'No videos in your feed could be found', '', '', '', '%sX.png' % OmniUtil.ICONS)
	return feed
	
"""
.. py:function:: getHistory()
Get the authenticated user's viewing history.

:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""	
def getHistory():
	feed = OmniUtil.Feedback()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_HISTORY)
	if gdataResults:
		feed.add_item(u'\u2329Clear History\u232A', '', '{\'key\':\'wipehistory\'}', '', '', '%sErase.png' % OmniUtil.ICONS)
		for i in gdataResults:
			feed.add_item(i['title']['$t'], '%s - %s' % (i['media$group']['media$credit'][0]['yt$display'],
				OmniUtil.secondsToHuman(int(i['media$group']['yt$duration']['seconds']))),
				'http://www.youtube.com/watch?v=%s' % i['media$group']['yt$videoid']['$t'], '', '',
				'%sListBlock.png' % OmniUtil.ICONS)
	else:
		feed.add_item('No Results', 'No videos in your history could be found', '', '', '', '%sX.png' % OmniUtil.ICONS)
	return feed

"""
.. py:function:: getPopular()
Get today's most popular YouTube videos.

:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""
def getPopular():
	feed = OmniUtil.Feedback()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_POPULAR, param1 = {'time':'today'})
	if gdataResults:
		for i in gdataResults:
			feed.add_item(i['title']['$t'], '%s - %s' % (i['author'][0]['name']['$t'], 
				OmniUtil.secondsToHuman(int(i['media$group']['yt$duration']['seconds']))), 
				'http://www.youtube.com/watch?v=%s' % i['media$group']['yt$videoid']['$t'], '', '', 
				'%sListBlock.png' % OmniUtil.ICONS)
	else:
		feed.add_item('No Results', 'No videos from most popular could be found', '', '', '', '%sX.png' % OmniUtil.ICONS)
	return feed

"""
.. py:function:: getFavorites()
Get authenticated user's favorites list.

:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""
def getFavorites():
	feed = OmniUtil.Feedback()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_FAVORITES)
	if gdataResults:
		for i in gdataResults:
			feed.add_item(i['title']['$t'], '%s - %s' % (i['media$group']['media$credit'][0]['yt$display'],
				OmniUtil.secondsToHuman(int(i['media$group']['yt$duration']['seconds']))),
				'http://www.youtube.com/watch?v=%s' % i['media$group']['yt$videoid']['$t'], '', '', 
				'%sListBlock.png' % OmniUtil.ICONS)
	else:
		feed.add_item('No Results', 'No videos from favorites could be found', '', '', '', '%sX.png' % OmniUtil.ICONS)
	return feed

"""
.. py:function:: getWatchLater()
Get authenticated user's watch later list.

:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""
def getWatchLater():
	feed = OmniUtil.Feedback()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_WATCHLATER)
	if gdataResults:
		for i in gdataResults:
			feed.add_item(i['title']['$t'], '%s - %s' % (i['author'][0]['name']['$t'],
				OmniUtil.secondsToHuman(int(i['media$group']['yt$duration']['seconds']))),
				'http://www.youtube.com/watch?v=%s' % i['media$group']['yt$videoid']['$t'], '', '', 
				'%sListBlock.png' % OmniUtil.ICONS)
	else:
		feed.add_item('No Results', 'No videos from favorites could be found', '', '', '', '%sX.png' % OmniUtil.ICONS)
	return feed

"""
.. py:function:: getUploads()
Get authenticated user's uploads list.

:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""
def getUploads():
	feed = OmniUtil.Feedback()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_UPLOADS)
	if gdataResults:
		for i in gdataResults:
			feed.add_item(i['title']['$t'], '%s - %s' % (i['author'][0]['name']['$t'],
				OmniUtil.secondsToHuman(int(i['media$group']['yt$duration']['seconds']))),
				'http://www.youtube.com/watch?v=%s' % i['media$group']['yt$videoid']['$t'], '', '', 
				'%sListBlock.png' % OmniUtil.ICONS)
	else:
		feed.add_item('No Results', 'No videos from favorites could be found', '', '', '', '%sX.png' % OmniUtil.ICONS)
	return feed

"""
.. py:function:: getChannelFeed(query)
Get a channels recent upload feed.

:param str query: Channel URL
:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""
def getChannelFeed(query):
	feed = OmniUtil.Feedback()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_USER_UPLOADS % OmniUtil.__urlParse__(query).path.split('/')[-1], 
		param1 = {'orderby':'published'})
	if gdataResults:
		for i in gdataResults:
			feed.add_item(i['title']['$t'], '%s - %s' % (i['media$group']['media$credit'][0]['yt$display'], 
				OmniUtil.secondsToHuman(int(i['media$group']['yt$duration']['seconds']))), 
				'http://www.youtube.com/watch?v=%s' % i['media$group']['yt$videoid']['$t'], '', '', 
				'%sListBlock.png' % OmniUtil.ICONS)
	else:
		feed.add_item('No Results', 'No feed results for "%s" could be found' % query, '', '', '', '%sX.png' % OmniUtil.ICONS)
	return feed
	
"""
.. py:function:: getSubscriptions()
List some of the authenticated user's subscriptions.

:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""
def getSubscriptions():
	feed = OmniUtil.Feedback()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_SUBSCRIPTIONS)
	if gdataResults:
		for i in gdataResults:
			if not os.path.exists('%s%s.jpg' % (OmniUtil.SUBSCRIPTIONS, i['yt$channelId']['$t'])):
				OmniUtil.retrieveThumb(i['yt$channelId']['$t'])
			feed.add_item(i['yt$username']['display'], '%s videos' % i['yt$countHint']['$t'], 
				'http://www.youtube.com/channel/%s' % i['yt$channelId']['$t'], '', '', 
				'%s%s.jpg' % (OmniUtil.SUBSCRIPTIONS, i['yt$channelId']['$t']))
	else:
		feed.add_item('No Results', 'No results for subscriptions could be found', '', '', '', '%sX.png' % OmniUtil.ICONS)
	return feed
	
"""
.. py:function:: getProfile()
List information about the authenticated user's profile.

:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""
def getProfile():
	def filterFeeds(gdataResults, rel):
		count = 0
		for i in gdataResults['gd$feedLink']:
			if i['rel'] == rel:
				return count
			else:
				count += 1
	feed = OmniUtil.Feedback()
	i = OmniUtil.jsonLoad(OmniUtil.BASE_PROFILE)['entry']
	if not os.path.exists('%s%s.jpg' % (OmniUtil.SUBSCRIPTIONS, i['link'][0]['href'].split('/')[-1])):
		OmniUtil.retrieveThumb(i['link'][0]['href'].split('/')[-1])
	feed.add_item(i['author'][0]['name']['$t'], '%s years old [%s]' % (i['yt$age']['$t'],i['yt$username']['$t']), 
		i['link'][0]['href'], '', '', '%s%s.jpg' % (OmniUtil.SUBSCRIPTIONS, i['link'][0]['href'].split('/')[-1]))
	feed.add_item('Subscriptions %s' % i['gd$feedLink'][filterFeeds(i, 'http://gdata.youtube.com/schemas/2007#user.subscriptions')]['countHint'], 
		'', '{\'key\':\'subscriptions\'}', '', '', '%sGroup.png' % OmniUtil.ICONS)
	feed.add_item('Subscribers %s' % i['yt$statistics']['subscriberCount'], '', '{\'key\':\'subscribers\'}', 
		'', '', '%sGroupG.png' % OmniUtil.ICONS)
	feed.add_item('Uploads %s' % i['gd$feedLink'][filterFeeds(i, 'http://gdata.youtube.com/schemas/2007#user.uploads')]['countHint'], 
		'', '{\'key\':\'uploads\'}', '', '', '%sMulti.png' % OmniUtil.ICONS)
	feed.add_item('Favorites %s' % OmniUtil.jsonLoad(OmniUtil.BASE_FAVORITES)['feed']['openSearch$totalResults']['$t'], 
		'', '{\'key\':\'favorites\'}', '', '', '%sHeart.png' % OmniUtil.ICONS)
	feed.add_item('Watch Later %s' % OmniUtil.jsonLoad(OmniUtil.BASE_WATCHLATER)['feed']['openSearch$totalResults']['$t'], 
		'', '{\'key\':\'watchlater\'}', '', '', '%sClock.png' % OmniUtil.ICONS)
	return feed

"""
.. py:function:: clearHistory()
Clear the recent viewing history of the authenticated user.
"""
def clearHistory():
	requests.post('%s/watch_history/actions/clear' % OmniUtil.BASE_PROFILE,
		data = '<?xml version="1.0" encoding="UTF-8"?>\n<entry xmlns="http://www.w3.org/2005/Atom">\n</entry>',
		headers = OmniUtil.postLoad())
	OmniUtil.displayNotification(OmniUtil.TITLE, 'History Cleared', '', '')
	
"""
.. py:function:: queryVideo(query)
Search for a video on YouTube.

:param str query: Query to search on YouTube
:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""	
def queryVideo(query):
	feed = OmniUtil.Feedback()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_VIDEO, param1 = {'orderby':'relevance', 'q':query})
	if gdataResults:
		for i in gdataResults:
			feed.add_item(i['title']['$t'], '%s - %s' % (i['author'][0]['name']['$t'], 
				OmniUtil.secondsToHuman(int(i['media$group']['yt$duration']['seconds']))), 
				'http://www.youtube.com/watch?v=%s' % i['media$group']['yt$videoid']['$t'], '', '', 
				'%sListBlock.png' % OmniUtil.ICONS)
	else:
		feed.add_item('No Results', 'No results for "%s" could be found' % query, '', '', '', '%sX.png' % OmniUtil.ICONS)
	return feed
	
"""
.. py:function:: queryChannel(query)
Search for a channel on YouTube.

:param str query: Query to search on YouTube
:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""
def queryChannel(query):
	feed = OmniUtil.Feedback()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_CHANNEL, param1 = {'max-results':'9', 'q':query})
	if gdataResults:
		for i in gdataResults:
			channelSummary = i['summary']['$t']
			channelLink = 'http://www.youtube.com/channel/%s' % i['yt$channelId']['$t']
			if len(channelSummary) <= 0:
				channelSummary = channelLink
			feed.add_item(i['author'][0]['name']['$t'], channelSummary, channelLink, '', '', '%sListBlock.png' % OmniUtil.ICONS)
	else:
		feed.add_item('No Results', 'No results for "%s" could be found' % query, '', '', '', '%sX.png' % OmniUtil.ICONS)
	return feed
	
"""
.. py:function:: queryPlaylist(query)
Search for a playlist on YouTube.

:param str query: Query to search on YouTube
:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""
def queryPlaylist(query):
	feed = OmniUtil.Feedback()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_PLAYLIST, param1 = {'max-results':'9', 'q':query})
	if gdataResults:
		for i in gdataResults:
			feed.add_item(i['title']['$t'], '%s - %s videos' % (i['author'][0]['name']['$t'], i['yt$countHint']['$t']), 
				'http://www.youtube.com/playlist?list=%s' % i['yt$playlistId']['$t'], '', '', '%sListBlock.png' % OmniUtil.ICONS)
	else:
		feed.add_item('No Results', 'No results for "%s" could be found' % query, '', '', '', '%sX.png' % OmniUtil.ICONS)
	return feed

"""
.. py:function:: addFavorite(query)
Add a video to the authenticated user's favorites.

:param str query: Video URL to be added to favorites
"""
def addFavorite(query):
	query = OmniUtil.__urlParse__(query).query.split('v=')[-1].split('&')[0]
	OmniUtil.postLoad()['Content-Length'] = '1'
	requests.post(OmniUtil.BASE_FAVORITES, 
		data = '<?xml version="1.0" encoding="UTF-8"?>\n<entry xmlns="http://www.w3.org/2005/Atom">\n<id>%s</id>\n</entry>' % query,
		headers = OmniUtil.postLoad())
	OmniUtil.displayNotification(OmniUtil.TITLE, 'Added to favorites', '', '')	
	
"""
.. py:function:: removeFavorite(query)
Remove a video from the authenticated user's favorites.

:param str query: Video URL to be removed from favorites
"""	
def removeFavorite(query):
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_FAVORITES)
	if gdataResults:
		for i in gdataResults:
			if i['media$group']['yt$videoid']['$t'] == OmniUtil.__urlParse__(query).query.split('v=')[-1].split('&')[0]:
				query = i['yt$favoriteId']['$t']
		requests.delete('%s/%s' % (OmniUtil.BASE_FAVORITES, query), data = '', headers = OmniUtil.postLoad())
		OmniUtil.displayNotification(OmniUtil.TITLE, 'Removed from Favorites', '', '')
	else:
		OmniUtil.displayNotification(OmniUtil.TITLE, 'Could not remove from Favorites', '<unkown error occured>', '')

"""
.. py:function:: addWatchLater(query)
Add a video to the authenticated user's watch later playlist.

:param str query: Video URL to be added to watch later
"""		
def addWatchLater(query):
	query = OmniUtil.__urlParse__(query).query.split('v=')[-1].split('&')[0]
	OmniUtil.postLoad()['Content-Length'] = '1'
	requests.post(OmniUtil.BASE_WATCHLATER,
		data = '<?xml version="1.0" encoding="UTF-8"?>\n<entry xmlns="http://www.w3.org/2005/Atom"\nxmlns:yt="http://gdata.youtube.com/schemas/2007">\n<id>%s</id>\n<yt:position>1</yt:position>\n</entry>' % query,
		headers = OmniUtil.postLoad())
	OmniUtil.displayNotification(OmniUtil.TITLE, 'Added to Watch Later', '', '')

"""
.. py:function:: removeWatchLater(query)
Remove a video from the authenticated user's watch later playlist.

:param str query: Video URL to be removed from watch later
"""	
def removeWatchLater(query):
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_WATCHLATER)
	if gdataResults:
		for i in gdataResults:
			if i['media$group']['yt$videoid']['$t'] == OmniUtil.__urlParse__(query).query.split('v=')[-1].split('&')[0]:
				query = i['id']['$t'].split(':')[-1]
		requests.delete('%s/%s' % (OmniUtil.BASE_FAVORITES, query), data = '', headers = OmniUtil.postLoad())
		OmniUtil.displayNotification(OmniUtil.TITLE, 'Removed from Watch Later', '', '')
	else:
		OmniUtil.displayNotification(OmniUtil.TITLE, 'Could not remove from Watch Later', '<unkown error occured>', '')
