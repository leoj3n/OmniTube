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
	OmniUtil.validStart()
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
	OmniUtil.validStart()
	feed = OmniUtil.Feedback()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_HISTORY)
	if gdataResults:
		feed.add_item(u'\u2329 Clear History \u232A', '', "{'key':'wipehistory'}", '', '', '%sErase.png' % OmniUtil.ICONS)
		for i in gdataResults:
			feed.add_item(i['title']['$t'], '%s - %s' % (i['media$group']['media$credit'][0]['yt$display'],
				OmniUtil.secondsToHuman(int(i['media$group']['yt$duration']['seconds']))),
				'http://www.youtube.com/watch?v=%s' % i['media$group']['yt$videoid']['$t'], '', '',
				'%sListBlock.png' % OmniUtil.ICONS)
	else:
		feed.add_item('No Results', 'No videos in your history could be found', '', '', '', '%sX.png' % OmniUtil.ICONS)
	return feed

"""
.. py:function:: selectPlaylist(text)
Select a playlist from the authenticated user's profile.

:param str text: Informative text of dropdown
:returns: URL of selected playlist
:rtype: str
"""
def selectPlaylist(text):
	OmniUtil.validStart()
	playlistHref = {}
	items = []
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_USER_PLAYLIST)
	if gdataResults:
		print gdataResults
		for i in gdataResults:
			playlistHref[i['title']['$t']] = 'http://www.youtube.com/playlist?list=%s' % i['yt$playlistId']['$t']
			items.append(i['title']['$t'])
		return playlistHref[OmniUtil.cocoaDropdown(text, items, '%s/icon.png' % OmniUtil.WORKFLOW)]
	else:
		OmniUtil.cocoaMsgBox('No playlists could be found!', 'Sorry, but no playlists could be found on this account.', '%sWarning.png' % OmniUtil.ICONS)
		sys.exit(0)

"""
.. py:function:: getPlaylists()
Get the authenticated user's playlists.

:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""
def getPlaylists():
	OmniUtil.validStart()
	feed = OmniUtil.Feedback()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_USER_PLAYLIST)
	feed.add_item(u'\u2329 New Playlist \u232A', '', "{'key':'newplaylist'}", '', '', '%sAddList.png' % OmniUtil.ICONS)
	if gdataResults:
		for i in gdataResults:
			feed.add_item(i['title']['$t'], '%s - %s videos' % (i['author'][0]['name']['$t'], i['yt$countHint']['$t']),
				'http://www.youtube.com/playlist?list=%s' % i['yt$playlistId']['$t'], '', '', '%sListBlock.png' % OmniUtil.ICONS)
	else:
		feed.add_item('No Results', 'No playlists on your account could be found', '', '', '', '%sX.png' % OmniUtil.ICONS)
	return feed

"""
.. py:function:: getPopular()
Get today's most popular YouTube videos.

:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""
def getPopular():
	OmniUtil.validStart()
	feed = OmniUtil.Feedback()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_POPULAR, param1 = {'time':'today'})
	if gdataResults:
		for i in gdataResults:
			feed.add_item(i['title']['$t'], '%s - %s' % (i['author'][0]['name']['$t'], 
				OmniUtil.secondsToHuman(int(i['media$group']['yt$duration']['seconds']))), 
				'http://www.youtube.com/watch?v=%s' % i['media$group']['yt$videoid']['$t'], '', '', 
				'%sListBlock.png' % OmniUtil.ICONS)
	else:
		feed.add_item('No Results', 'No videos from "Most Popular" could be found', '', '', '', '%sX.png' % OmniUtil.ICONS)
	return feed

"""
.. py:function:: getFavorites()
Get authenticated user's favorites list.

:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""
def getFavorites():
	OmniUtil.validStart()
	feed = OmniUtil.Feedback()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_FAVORITES)
	if gdataResults:
		for i in gdataResults:
			feed.add_item(i['title']['$t'], '%s - %s' % (i['media$group']['media$credit'][0]['yt$display'],
				OmniUtil.secondsToHuman(int(i['media$group']['yt$duration']['seconds']))),
				'http://www.youtube.com/watch?v=%s' % i['media$group']['yt$videoid']['$t'], '', '', 
				'%sListBlock.png' % OmniUtil.ICONS)
	else:
		feed.add_item('No Results', 'No videos from "Favorites" could be found', '', '', '', '%sX.png' % OmniUtil.ICONS)
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
			feed.add_item(i['title']['$t'], '%s - %s' % (i['media$group']['media$credit'][0]['yt$display'],
				OmniUtil.secondsToHuman(int(i['media$group']['yt$duration']['seconds']))),
				'http://www.youtube.com/watch?v=%s' % i['media$group']['yt$videoid']['$t'], '', '', 
				'%sListBlock.png' % OmniUtil.ICONS)
	else:
		feed.add_item('No Results', 'No videos from "Watch Later" could be found', '', '', '', '%sX.png' % OmniUtil.ICONS)
	return feed

"""
.. py:function:: getUploads()
Get authenticated user's uploads list.

:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""
def getUploads():
	OmniUtil.validStart()
	feed = OmniUtil.Feedback()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_UPLOADS)
	if gdataResults:
		for i in gdataResults:
			feed.add_item(i['title']['$t'], '%s - %s' % (i['author'][0]['name']['$t'],
				OmniUtil.secondsToHuman(int(i['media$group']['yt$duration']['seconds']))),
				'http://www.youtube.com/watch?v=%s' % i['media$group']['yt$videoid']['$t'], '', '', 
				'%sListBlock.png' % OmniUtil.ICONS)
	else:
		feed.add_item('No Results', 'No videos from your uploads could be found', '', '', '', '%sX.png' % OmniUtil.ICONS)
	return feed

"""
.. py:function:: getChannelFeed(query)
Get a channels recent upload feed.

:param str query: Channel URL
:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""
def getChannelFeed(query):
	OmniUtil.validStart()
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
.. py:function:: getPlaylistFeed(query)
Get a channels recent upload feed.

:param str query: Playlist URL
:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""
def getPlaylistFeed(query):
	OmniUtil.validStart()
	feed = OmniUtil.Feedback()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_PLAYLIST_FEED % OmniUtil.__urlParse__(query).query.split('=')[1])
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
	OmniUtil.validStart()
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
		feed.add_item('No Results', 'No results for your subscriptions could be found', '', '', '', '%sX.png' % OmniUtil.ICONS)
	return feed	

"""
.. py:function:: getProfile()
List information about the authenticated user's profile.

:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""
def getProfile():
	OmniUtil.validStart()
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
	try:
		feed.add_item('Playlists %s' % OmniUtil.jsonLoad(OmniUtil.BASE_USER_PLAYLIST)['feed']['openSearch$totalResults']['$t'],
		'', '{\'key\':\'playlists\'}', '', '', '%sList.png' % OmniUtil.ICONS)
	except ValueError:
		feed.add_item(u'\uFFFD Playlists \uFFFD', 'Sorry, for some reason your playlists could not be found', '', '', '', '%sList.png' % OmniUtil.ICONS)
	try:
		feed.add_item('Favorites %s' % OmniUtil.jsonLoad(OmniUtil.BASE_FAVORITES)['feed']['openSearch$totalResults']['$t'], 
			'', '{\'key\':\'favorites\'}', '', '', '%sHeart.png' % OmniUtil.ICONS)
	except ValueError:
		feed.add_item(u'\uFFFD Favorites \uFFFD', 'Sorry, for some reason your Favorites could not be found', '', '', '', '%sHeart.png' % OmniUtil.ICONS)
	try:
		feed.add_item('Watch Later %s' % OmniUtil.jsonLoad(OmniUtil.BASE_WATCHLATER)['feed']['openSearch$totalResults']['$t'], 
			'', '{\'key\':\'watchlater\'}', '', '', '%sClock.png' % OmniUtil.ICONS)
	except ValueError:
		feed.add_item(u'\uFFFD Watch Later \uFFFD' 'Sorry, for some reason your Watch Later could not be found', '', '', '', '%sClock.png' % OmniUtil.ICONS)
	return feed

"""
.. py:function:: queryVideo(query)
Search for a video on YouTube.

:param str query: Query to search on YouTube
:returns: Alfred 2 script filter feedback
:rtype: XML Feedback
"""	
def queryVideo(query):
	OmniUtil.validStart()
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
	OmniUtil.validStart()
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
	OmniUtil.validStart()
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
.. py:function:: addPlaylist()
Add a new playlist to the authenticated user's profile.
"""
def addPlaylist():
	OmniUtil.validStart()
	playlistTitle = OmniUtil.cocoaInputBox('Enter the title of your new playlist:', '%s/icon.png' % OmniUtil.WORKFLOW)
	playlistDescription = OmniUtil.cocoaInputBox('Enter a description for your new playlist:', '%s/icon.png' % OmniUtil.WORKFLOW)
	postLoad = OmniUtil.postLoad()
	postLoad['Content-Length'] = '1'
	requests.post(OmniUtil.BASE_USER_PLAYLIST,
		data = '<?xml version="1.0" encoding="UTF-8"?>\n<entry xmlns="http://www.w3.org/2005/Atom"\n\txmlns:yt="http://gdata.youtube.com/schemas/2007">\n<title type="text">%s</title>\n<summary>%s</summary>\n</entry>' % (playlistTitle, playlistDescription),
		headers = postLoad)
	OmniUtil.displayNotification(OmniUtil.TITLE, 'Created new playlist', playlistTitle, '')

"""
.. py:function:: removePlaylist(query)
Remove a playlist from the authenticated user's profile.

:param str query: URL of playlist to delete
"""
def removePlaylist(query):
	OmniUtil.validStart()
	playlistId = OmniUtil.__urlParse__(query).query.split('=')[1]
	query = '%s/%s' % (OmniUtil.BASE_USER_PLAYLIST, playlistId)
	if OmniUtil.cocoaYesNoBox('Deleting Playlist!', 'Are you sure you want to delete this playlist?', '%sWarning.png' % OmniUtil.ICONS):
		requests.delete(query, data = '', headers = OmniUtil.postLoad())
		OmniUtil.displayNotification(OmniUtil.TITLE, 'Deleted Playlist', playlistId, '')

"""
.. py:function:: addToPlaylist(video)
Add a video to a specific playlist on the authenticated user's profile.

:param str video: URL of the video to add
"""
def addToPlaylist(video):
	OmniUtil.validStart()
	if video[0] == "'":
		video = video[1:-1]
	postLoad = OmniUtil.postLoad()
	postLoad['Content-Length'] = '1'
	requests.post(OmniUtil.BASE_PLAYLIST_FEED % OmniUtil.__urlParse__(selectPlaylist('Add <%s> to which playlist?' % video)).query.split('=')[1],
		data = '<?xml version="1.0" encoding="UTF-8"?>\n<entry xmlns="http://www.w3.org/2005/Atom"\n\txmlns:yt="http://gdata.youtube.com/schemas/2007">\n<id>%s</id>\n<yt:position>1</yt:position>\n</entry>' % OmniUtil.__urlParse__(video).query.split('=')[1].split('&')[0],
		headers = postLoad)
	OmniUtil.displayNotification(OmniUtil.TITLE, 'Added video to playlist', '', '')

"""
.. py:function:: removeFromPlaylist(video, playlist)
Remove a video from a specific playlist on the authenticated user's profile.

:param str video: URL of the video to remove
:param str playlist: URL of the playlist to be removed from
"""		
def removeFromPlaylist(video):
	OmniUtil.validStart()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_PLAYLIST_FEED % OmniUtil.__urlParse__(selectPlaylist('Remove <%s> from which playlist?' % video)).query.split('=')[1])
	if gdataResults:
		for i in gdataResults:
			if i['media$group']['yt$videoid']['$t'] == OmniUtil.__urlParse__(video).query.split('=')[1].split('&')[0]:
				for j in i['link']:
					if j['rel'] == 'self':
						requests.delete(j['href'], data = '', headers = OmniUtil.postLoad())
						OmniUtil.displayNotification(OmniUtil.TITLE, 'Removed video from playlist', '', '')
	else:
		OmniUtil.cocoaMsgBox('Could not delete video from playlist', 'Sorry, but an error occured during the deletion process.', '%sWarning.png' % OmniUtil.ICONS)

"""
.. py:function:: addFavorite(query)
Add a video to the authenticated user's favorites.

:param str query: Video URL to be added to favorites
"""
def addFavorite(query):
	OmniUtil.validStart()
	query = OmniUtil.__urlParse__(query).query.split('v=')[-1].split('&')[0]
	OmniUtil.postLoad()['Content-Length'] = '1'
	requests.post(OmniUtil.BASE_FAVORITES, 
		data = '<?xml version="1.0" encoding="UTF-8"?>\n<entry xmlns="http://www.w3.org/2005/Atom">\n<id>%s</id>\n</entry>' % query,
		headers = OmniUtil.postLoad())
	OmniUtil.displayNotification(OmniUtil.TITLE, 'Added to Favorites', '', '')	
	
"""
.. py:function:: removeFavorite(query)
Remove a video from the authenticated user's favorites.

:param str query: Video URL to be removed from favorites
"""
def removeFavorite(query):
	OmniUtil.validStart()
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
	OmniUtil.validStart()
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
	OmniUtil.validStart()
	gdataResults = OmniUtil.gdataLoad(OmniUtil.BASE_WATCHLATER)
	if gdataResults:
		for i in gdataResults:
			if i['media$group']['yt$videoid']['$t'] == OmniUtil.__urlParse__(query).query.split('v=')[-1].split('&')[0]:
				query = i['id']['$t'].split(':')[-1]
		requests.delete('%s/%s' % (OmniUtil.BASE_FAVORITES, query), data = '', headers = OmniUtil.postLoad())
		OmniUtil.displayNotification(OmniUtil.TITLE, 'Removed from Watch Later', '', '')
	else:
		OmniUtil.displayNotification(OmniUtil.TITLE, 'Could not remove from "Watch Later"', '<unkown error occured>', '')
