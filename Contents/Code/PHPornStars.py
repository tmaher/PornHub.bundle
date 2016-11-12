from PHCommon import *

PH_PORNSTARS_URL =			PH_ORIENTATION_URL + '/pornstars'
PH_PORNSTARS_SEARCH_URL =	PH_PORNSTARS_URL + '/search?search=%s'

MAX_PORNSTARS_PER_PAGE =	28

@route(ROUTE_PREFIX + '/pornstars')
def BrowsePornStars(title=L("DefaultBrowsePornStarsTitle")):

	# Create a dictionary of menu items
	browsePornStarsMenuItems = OrderedDict([
		('Search Porn Stars',		{'function':SearchPornStars, 'search':True, 'directoryObjectArgs':{'prompt':'Search for...','summary':'Enter Porn Star Search Terms'}}),
		('Most Popular - All Time',	{'function':ListPornStars, 'functionArgs':{'url':addURLParameters(PH_PORNSTARS_URL, {'t':'a'})}}),
		('Most Popular - Monthly',	{'function':ListPornStars, 'functionArgs':{'url':addURLParameters(PH_PORNSTARS_URL, {'t':'m'})}}),
		('Most Popular - Weekly',		{'function':ListPornStars, 'functionArgs':{'url':addURLParameters(PH_PORNSTARS_URL, {'t':'w'})}}),
		('Most Viewed - All Time',	{'function':ListPornStars, 'functionArgs':{'url':addURLParameters(PH_PORNSTARS_URL, {'o':'mv', 't':'a'})}}),
		('Most Viewed - Monthly',		{'function':ListPornStars, 'functionArgs':{'url':addURLParameters(PH_PORNSTARS_URL, {'o':'mv', 't':'m'})}}),
		('Most Viewed - Weekly',		{'function':ListPornStars, 'functionArgs':{'url':addURLParameters(PH_PORNSTARS_URL, {'o':'mv', 't':'w'})}}),
		('Most Viewed - Daily',		{'function':ListPornStars, 'functionArgs':{'url':addURLParameters(PH_PORNSTARS_URL, {'o':'mv', 't':'t'})}}),
		('Top Trending',			{'function':ListPornStars, 'functionArgs':{'url':addURLParameters(PH_PORNSTARS_URL, {'o':'t'})}}),
		('Most Subscribed',			{'function':ListPornStars, 'functionArgs':{'url':addURLParameters(PH_PORNSTARS_URL, {'o':'ms'})}}),
		('Alphabetical',			{'function':ListPornStars, 'functionArgs':{'url':addURLParameters(PH_PORNSTARS_URL, {'o':'a'})}}),
		('Number of Videos',			{'function':ListPornStars, 'functionArgs':{'url':addURLParameters(PH_PORNSTARS_URL, {'o':'nv'})}})
	])

	return GenerateMenu(title, browsePornStarsMenuItems)

@route(ROUTE_PREFIX + '/pornstars/list')
def ListPornStars(title, url = PH_PORNSTARS_URL, page=1):

	# Create a dictionary of menu items
	listPornStarsMenuItems = OrderedDict()

	# Add the page number into the query string
	if (int(page) != 1):
		url = addURLParameters(url, {'page':str(page)})

	# Get the HTML of the page
	html = HTML.ElementFromURL(url)

	# Use xPath to extract a list of porn stars
	pornStars = html.xpath("//div[contains(@class, 'pornstarFilterContainer')]/ul/li")

	# Loop through all channels
	for pornStar in pornStars:

		# Use xPath to extract porn star details
		pornStarName =		pornStar.xpath("./div/div[contains(@class, 'thumbnail-info-wrapper')]/a/text()")[0]
		pornStarURL =		BASE_URL + pornStar.xpath("./div/div[contains(@class, 'thumbnail-info-wrapper')]/a/@href")[0]
		pornStarThumbnail =	pornStar.xpath("./div/a/img/@src")[0]

		# Add a menu item for the porn star
		listPornStarsMenuItems[pornStarName] = {'function':BrowseVideos, 'functionArgs':{'url':pornStarURL}, 'directoryObjectArgs':{'thumb':pornStarThumbnail}}

	# There is a slight change that this will break... If the number of videos returned in total is divisible by MAX_VIDEOS_PER_PAGE with no remainder, there could possibly be no additional page after. This is unlikely though and I'm too lazy to handle it.
	if (len(pornStars) == MAX_PORNSTARS_PER_PAGE):
		listPornStarsMenuItems['Next Page'] = {'function':ListPornStars, 'functionArgs':{'title':title, 'url':url, 'page':int(page)+1}, 'nextPage':True}

	return GenerateMenu(title, listPornStarsMenuItems)

@route(ROUTE_PREFIX + '/pornstars/search')
def SearchPornStars(query):

	# Format the query for use in PornHub's search
	formattedQuery = formatStringForSearch(query, "+")

	try:
		return ListPornStars(title='Search Results for ' + query, url=PH_PORNSTARS_SEARCH_URL % formattedQuery)
	except:
		return ObjectContainer(header='Search Results', message="No search results found", no_cache=True)
