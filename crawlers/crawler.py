import urllib.request
import urllib.error
import json
import sys
import argparse
import iso8601

class Crawler:

    # Ticketmaster
    baseUrl = 'https://app.ticketmaster.com/discovery/v2/events.json?'
    apiKey = 'Ry4V2S9yfBqhz1MFpeRJnEbAxcp0nSGQ'

    # Universe
    # baseUrl = 'https://discover.universe.com/api/v2/discover_events?'
    # apiKey = ''

    # General constants
    EQUALS = '='
    AMPERSAND = '&'
    APIKEY = 'apikey'
    SLASH = '/'
    ROOT = 'root'
    PATH = 'path'
    REQUIRED = 'required'
    TYPE = 'type'
    API = 'api'
    APIS = ['universe', 'ticketmaster']

    # Type constants
    STRING = 'string'
    FLOAT = 'float'
    INT = 'int'
    UNIXTIME = 'unixtime'

    request_params_file = 'requestParams.json'
    mapping_file = 'mapping.json'
    output_file = 'output.json'

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
            if self.ROOT in mapping.keys():
                for split in mapping[self.ROOT].split(self.SLASH):
                    response = response[split]
                mapping.pop(self.ROOT)

            for event in response:
                newEvent = dict(mapping)
                skip = False

                for key, value in newEvent.items():
                    if isinstance(value, dict):
                        path = value[self.PATH]
                        required = value[self.REQUIRED]
                        outputType = value[self.TYPE]
                    else:
                        path = value
                        required = False
                        outputType = self.STRING

                    feature = self.traverseDict(event, path)

                    if outputType != self.STRING:
                        feature = self.convertType(feature, outputType)

                    if feature is '' and required:
                        print('Skipping')
                        skip = True
                        break

                    newEvent[key] = feature

                if skip:
                    continue

                for api in self.APIS:
                    if api in self.baseUrl:
                        newEvent[self.API] = api

                output.append(newEvent)


        except KeyError as error:
            print('Error parsing the key: ' + str(error))
            sys.exit()
        except IndexError as error:
            print(str(error))
            sys.exit()

        return output

    # iteratively traversely over through a dictionary to get a specified value
    def traverseDict(self, dictionary, path):
        splits = path.split(self.SLASH)

        feature = dictionary
        for split in path.split(self.SLASH):
            if isinstance(feature, list):
                feature = feature[0]  # todo: better array handling

            if split in feature.keys():
                feature = feature[split]
            else:
                feature = ''
                break

        return feature

    # handles all conversion of strings to the specified output type
    def convertType(self, feature, outputType):
        try:
            if outputType == self.FLOAT:
                return float(feature)
            elif outputType == self.INT:
                return int(float(feature))
            elif outputType == self.UNIXTIME:
                return iso8601.parse_date(feature).timestamp()
        except ValueError as error:
            print(error)
        except iso8601.iso8601.ParseError as error:
            print(error)

        return ''

    # reads the file that indicates the mapping for how information is parsed from the response
    def loadMapping(self, fileName):
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
    def outputEvents(self, fileName, output):
        try:
            with open(fileName, 'w') as file:
                file.write(self.pyToJson(output, True))

                print('Outputting events')
        except IOError:
            print('Could open or write to output file')
            sys.exit()
        except json.JSONDecodeError:
            print('Invalid output content')
            sys.exit()

    # same as outputEvents except adds the output events onto the ones existing in the file
    def appendEvents(self, fileName, output):
        try:
            with open(fileName, 'r+') as file:
                contents = file.read()

                if contents is not '':
                    contents = self.jsonToPy(contents)
                    sum = contents + output
                    file.seek(0)
                    file.truncate()
                    file.write(self.pyToJson(sum, True))
                else:
                    file.write(self.pyToJson(output, True))

                print('Appending events')
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
    def readRequestFile(self, fileName):
        try:
            with open(fileName, 'r') as file:
                content = file.read()
        except IOError:
            print('Could not read request parameters file')
            sys.exit()

        return content

    def run(self):
        jsonOptions = self.readRequestFile(Crawler.request_params_file)
        strOptions = self.buildOptions(jsonOptions)
        response = self.request(strOptions)

        # response = self.jsonToPy(open('temp.txt', 'r').read())  # this is for testing

        mapping = self.loadMapping(Crawler.mapping_file)
        output = self.parseEvents(response, mapping)
        self.outputEvents(Crawler.output_file, output)

        print('done')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--request')
    parser.add_argument('-m', '--mapping')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

    if args.request is not None:
        Crawler.request_params_file = args.request

    if args.mapping is not None:
        Crawler.mapping_file = args.mapping

    if args.output is not None:
        Crawler.output_file = args.output

    crawler = Crawler()
    crawler.run()