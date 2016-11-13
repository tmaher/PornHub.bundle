from PHCommon import *
from PHCategories import *
from PHChannels import *
from PHPornStars import *
from PHPlaylists import *
from PHMembers import *

NAME =	L("ChannelTitle")

ART =	'art-' + Prefs["channelBackgroundArt"]
ICON =	'icon-' + Prefs["channelIconArt"]

def Start():

	# Set the defaults for Object Containers
	ObjectContainer.art =		R(ART)
	ObjectContainer.title1 =	NAME

	# Set the defaults of Directory Objects
	DirectoryObject.thumb =	R(ICON)
	PhotoAlbumObject.thumb =	R(ICON)

	# Set the default language
	Locale.DefaultLocale = "en"

	# Set the cache lifespan
	HTTP.CacheTime = CACHE_1MINUTE * 5

	# Set the user agent
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0'

def ValidatePrefs():
	ART =	'art-' + Prefs["channelBackgroundArt"]
	ObjectContainer.art =		R(ART)

	ICON =	'icon-' + Prefs["channelIconArt"]
	DirectoryObject.thumb =	R(ICON)

@handler(ROUTE_PREFIX, NAME, thumb=ICON, art=ART)
def MainMenu():

	my_playlists = []
	if Prefs["playlists"] != None:
		for playlist in Prefs["playlists"].split(','):
			pl_url = PH_PLAYLIST_URL + playlist
			my_playlists += [("%s (/playlist/%s)" % (GetPlaylistTitle(pl_url), playlist), {'function':ListVideos, 'functionArgs':{'url': pl_url}})]

	# Create a dictionary of menu items
	mainMenuItems = OrderedDict(my_playlists + [
		('Browse All Videos',	{'function':BrowseVideos}),
		('Categories',			{'function':BrowseCategories}),
		('Channels',			{'function':BrowseChannels}),
		('Porn Stars',			{'function':BrowsePornStars}),
		('Playlists',			{'function':BrowsePlaylists}),
		('Members',			{'function':BrowseMembers}),
		('Search',				{'function':SearchVideos, 'search':True, 'directoryObjectArgs':{'prompt':'Search for...','summary':'Enter Search Terms'}})
	])

	oc = GenerateMenu(NAME, mainMenuItems)

	oc.add(PrefsObject(
		title="Preferences"
	))

	return oc
