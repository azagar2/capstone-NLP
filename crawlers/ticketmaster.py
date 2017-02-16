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
    EMBEDDED = '_embedded'
    EVENTS = 'events'
    SLASH = '/'

    def __init__(self):
        pass
        # load baseUrl and apiKey from db

    # Makes an HTTP request
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

    # convert json string to python dict
    def jsonToPy(self, text):
        return json.loads(text)

    # convert python dict or list into a json string
    def pyToJson(self, text, pretty = False):
        if pretty:
            return json.dumps(text, indent = 4, separators = (',', ': '))
        else:
            return json.dumps(text)

    # parses the events from the request response
    def parseEvents(self, response, mapping):
        output = list()

        try:
            for event in response[self.EMBEDDED][self.EVENTS]:
                newEvent = dict(mapping)

                for key, value in newEvent.items():
                        if self.SLASH not in value:
                            newEvent[key] = event[value]
                        else:
                            feature = event
                            for split in value.split(self.SLASH):
                                if (isinstance(feature, list)):
                                    feature = feature[0][split]
                                else:
                                    feature = feature[split]
                            newEvent[key] = feature

                output.append(newEvent)

        except KeyError as error:
            print('Error parsing the key: ' + str(error))
            sys.exit()
        except IndexError as error:
            print(str(error))
            sys.exit()

        return output

    # reads the file that indicates the mapping for how information is parsed from the response
    def loadMapping(self, fileName = 'mapping.json'):
        try:
            with open(fileName, 'r') as file:
                content = self.jsonToPy(file.read())
        except IOError:
            print('Could not read mapping file')
            sys.exit()
        except json.JSONDecodeError:
            print('Invalid mapping contents')
            sys.exit()

        mapping = dict((k, v) for k, v in content.items() if v)

        return mapping

    # write the parsed events to the output file
    def outputEvents(self, output, fileName = 'output.json'):
        try:
            with open(fileName, 'w') as file:
                for event in output:
                    file.write(self.pyToJson(output, True))
        except IOError:
            print('Could open or write to output file')
            sys.exit()
        except json.JSONDecodeError:
            print('Invalid output content')
            sys.exit()

    # determine how update to date our db is (simple get value check)
    def dbLastUpdated(self):
        pass

    # push formatted events to db
    def updateDb(self):
        pass

    # converts the request parameters from json to a string
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

    # Opens the file with the JSON that specifics the parameters of the request
    def readRequestFile(self, fileName = 'requestParams.json'):
        try:
            with open(fileName, 'r') as file:
                content = file.read()
        except IOError:
            print('Could not read request parameters file')
            sys.exit()

        return content


# run
crawler = TicketMasterCrawler()

jsonOptions = crawler.readRequestFile()
strOptions = crawler.buildOptions(jsonOptions)
response = crawler.request(strOptions)

# response = crawler.jsonToPy(open('temp.txt', 'r').read())  # this is for testing

mapping = crawler.loadMapping()
output = crawler.parseEvents(response, mapping)
crawler.outputEvents(output)
