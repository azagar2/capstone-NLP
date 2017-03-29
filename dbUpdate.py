from crawlers import crawler
from utils import database

# Past events
db = database.DB()

SQL = 'SELECT listingid FROM universe OFFSET 5000 LIMIT 100000'
listingIds = db.get(SQL,[])
listingIds = list(k[0] for k in listingIds)
listingIds = list(set(listingIds))

c = crawler.Crawler()
c.listingsRequest(listingIds)

# Future events
c.baseUrl = crawler.Crawler.APIS['universe']
c.run()
