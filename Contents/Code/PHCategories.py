from PHCommon import *

PH_CATEGORIES_URL =				PH_ORIENTATION_URL + '/categories'
PH_CATEGORIES_ALPHABETICAL_URL =	PH_CATEGORIES_URL + '?o=al'

@route(ROUTE_PREFIX + '/categories')
def BrowseCategories(title=L("DefaultBrowseCategoriesTitle"), url = PH_CATEGORIES_ALPHABETICAL_URL):

	# Create a dictionary of menu items
	browseCategoriesMenuItems = OrderedDict()

	# Get the HTML of the page
	html = HTML.ElementFromURL(url)

	# Use xPath to extract a list of catgegories
	categories = html.xpath("//div[@id='categories%sImages']/ul[contains(@class, 'categories-list')]/li/div" % Prefs['orientation'])

	# Loop through all categories
	for category in categories:

		# Use xPath to extract category details
		categoryTitle =		category.xpath("./h5/a/strong/text()")[0]
		categoryURL =		BASE_URL + category.xpath("./h5/a/@href")[0]
		categoryThumbnail =	category.xpath("./a/img/@src")[0]

		# Add a menu item for the category
		browseCategoriesMenuItems[categoryTitle] = {'function':BrowseVideos, 'functionArgs':{'url':categoryURL}, 'directoryObjectArgs':{'thumb':categoryThumbnail}}

	return GenerateMenu(title, browseCategoriesMenuItems)
