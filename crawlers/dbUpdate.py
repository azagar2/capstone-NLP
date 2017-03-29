from crawlers import crawler
from utils import database

# Past events
db = database.DB()

SQL = 'SELECT listingid FROM universe'
listingIds = db.get(SQL,[])

# listingIds = [
#     '5193948268eacb41f7000fa0',
#     '4f1794782078f9444100004b', # this one fails
#     '566b4f2969c81c84a600000e'
# ]

c = crawler.Crawler()
c.listingsRequest(listingIds)


# Future events
c.run()
