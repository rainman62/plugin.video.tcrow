import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import xbmc

import resolveurl

import requests
import re
from HTMLParser import HTMLParser

def getMoviesFromPage(url):
    inputHTML = requests.get(url).text
    returnValue = []
    class MyHTMLParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            if tag=='a' and len(attrs)==2 and attrs[0][0]=='href' and attrs[1][0]=='title':
                returnValue.append({'link':attrs[0][1], 'title': attrs[1][1], 'image':''})
    # instantiate the parser and fed it some HTML
    parser = MyHTMLParser()
    parser.feed(inputHTML)
    return returnValue

SERVER_BASE_URL = "http://tamilimac.net/"
CATEGORIES = {'hd': "category/movies/tamil-hd-movies/"}

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])


xbmcplugin.setContent(addon_handle, 'movies')

# returns url to move between tabs
def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

#
def webBuildPageURL(category,pageNumber):
    return SERVER_BASE_URL + CATEGORIES.get(category) + 'page/' + pageNumber

current_category = args.get('current_category',None)
current_level = args.get('level', 'MainMenu')
current_page = args.get('page', None)
current_movie = args.get('movieURL', None)

if current_level == 'MainMenu':
    for category in CATEGORIES.keys():
        url = build_url({'current_category': category, 'level': 'Folder'})
        li = xbmcgui.ListItem(category.capitalize())
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)
    xbmcplugin.endOfDirectory(addon_handle)
elif current_level[0] == 'Folder':
    my_current_page = '1' if current_page is None else current_page[0]
    webPageURL = webBuildPageURL(current_category[0], my_current_page)
    movieList = getMoviesFromPage(webPageURL)

    for movieItem in movieList:
        url = build_url({'level': 'Movie', 'movieURL': movieItem.get('link')})
        li = xbmcgui.ListItem(movieItem.get('title'))
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    url = build_url({'current_category': current_category[0], 'level': 'Folder', 'page': str(int(my_current_page)+1)})
    li = xbmcgui.ListItem('Next..')
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
elif current_level[0] == 'Movie':
    xbmc.log("------------------ Inside Movie -------------", level=xbmc.LOGNOTICE)
    my_current_movieURL = current_movie[0]
    xbmc.log("Current Movie URL: " + my_current_movieURL, level=xbmc.LOGNOTICE)
    inputHTML = str(requests.get(my_current_movieURL).text)
    _start = inputHTML.find('<iframe')
    _end = inputHTML.rfind('/iframe>')
    inputHTML = inputHTML[_start:_end]
    xbmc.log("Movie content : " + inputHTML, level=xbmc.LOGNOTICE)

    xbmc.log(inputHTML, level=xbmc.LOGNOTICE)
    videoList = resolveurl.scrape_supported(inputHTML, regex= '''=\s*['"]([^'"]+)''')
    xbmc.log(str(videoList), level=xbmc.LOGNOTICE)

    for video in videoList:
        playableURL = resolveurl.resolve(video)
        li = xbmcgui.ListItem(video)
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=playableURL, listitem=li)
    xbmcplugin.endOfDirectory(addon_handle)

# TODO : Render Main Menu from categories

# TODO : Render List of movies from current categoryd


