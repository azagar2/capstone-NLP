import urllib.request
import urllib.error
import json
import sys

class TicketMasterCrawler:

    baseUrl = 'https://app.ticketmaster.com/discovery/v2/events.json?'
    apiKey = 'Ry4V2S9yfBqhz1MFpeRJnEbAxcp0nSGQ'

    EQUALS = '='
    AMPERSAND = '&'
    APIKEY = 'apikey'

    outputParams = 'id, city, country, status, start_time, event_end_time (YYYY-MM-DD), title, description, category, latitude, longitude'

    def __init__(self):
        pass
        # load baseUrl and apiKey from db

    def request(self, options, decoding = 'utf-8'):
        url = self.baseUrl + options

        try:
            print('Sending request: ' + url)
            results = urllib.request.urlopen(url).read()
        except urllib.error.HTTPError as error:
            print(error)
            sys.exit()

        decoded = str(results, 'utf-8')

        return self.jsonToPy(decoded)

    def jsonToPy(self, text):
        return json.loads(text)

    def pyToJson(self, text):
        return json.dumps(text)

    def parseEvents(self, outputParams):
        # take outputs as format of output params... need to map ticketmaster params to ours
        pass

    def dbLastUpdated(self):
        # determine how update to date our db is (simple get value check)
        pass

    def updateDb(self):
        # push formatted events to db
        pass

    def buildOptions(self, jsonOptions):
        try:
            options = self.jsonToPy(jsonOptions)
        except json.JSONDecodeError:
            print('Invalid input options')
            sys.exit()

        strOptions = ""

        for key, item in options.items():
            strOptions += str(key) + self.EQUALS + str(item) + self.AMPERSAND

        strOptions += self.APIKEY + self.EQUALS + self.apiKey

        return strOptions

    def readInputFile(self, fileName = 'input.json'):
        try:
            with open(fileName, 'r') as file:
                content = file.read()
        except IOError:
            print('Could not read file')
            sys.exit()

        return content

crawler = TicketMasterCrawler()
jsonOptions = crawler.readInputFile()
strOptions = crawler.buildOptions(jsonOptions)
response = crawler.request(strOptions)

