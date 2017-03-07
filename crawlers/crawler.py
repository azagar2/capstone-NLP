import urllib.request
import urllib.error
import json
import sys
import argparse
import iso8601
import os

from utils import database

# Ticketmaster: Ry4V2S9yfBqhz1MFpeRJnEbAxcp0nSGQ

class Crawler:
    APIS = {
        'universe': 'https://discover.universe.com/api/v2/discover_events?',
        'ticketmaster': 'https://app.ticketmaster.com/discovery/v2/events.json?'
    }

    # General constants
    EQUALS = '='
    AMPERSAND = '&'
    SLASH = '/'
    ROOT = 'root'
    PATH = 'path'
    REQUIRED = 'required'
    TYPE = 'type'
    API = 'api'
    DEFAULT = 'default'
    CRAWLERS = 'crawlers'

    # Type constants
    STRING = 'string'
    FLOAT = 'float'
    INT = 'int'
    UNIXTIME = 'unixtime'

    # Config constants
    request_params_file = 'requestParams.json'
    mapping_file = 'mapping.json'
    output_file = 'output.json'


    def __init__(self, api='universe'):
        self.DB = database.DB()
        self.baseUrl = self.APIS[api]

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
    def pyToJson(self, text, pretty=False):
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
                    path = value
                    required = False
                    outputType = self.STRING
                    default = None

                    if isinstance(value, dict):
                        path = value[self.PATH]
                        required = value[self.REQUIRED] if self.REQUIRED in value.keys() else False
                        outputType = value[self.TYPE] if self.TYPE in value.keys() else self.STRING
                        default = value[self.DEFAULT] if self.DEFAULT in value.keys() else ''

                    feature = self.traverseDict(event, path)

                    feature = self.convertType(feature, outputType)

                    if feature is '':
                        feature = default

                    if feature is None and required:
                        print('Skipping')
                        skip = True
                        break

                    newEvent[key] = feature

                if skip:
                    continue

                for api in self.APIS.keys():
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
        feature = dictionary
        for split in path.split(self.SLASH):
            if isinstance(feature, list):
                feature = feature[0]  # todo: better array handling

            if split in feature.keys():
                feature = feature[split]
            else:
                feature = ''
                break

        if feature is None:
            return ''

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
            elif outputType == self.STRING:
                return str(feature)
        except ValueError as error:
            print("Value Error: " + str(error))
        except iso8601.iso8601.ParseError as error:
            print("ISO8601 Parse Error: " + str(error))
        except TypeError as error:
            print("Type Error: " + str(error))

        return None

    # reads the file that indicates the mapping for how information is parsed from the response
    def loadMapping(self, fileName):
        try:
            fileDir = os.path.dirname(os.path.realpath('__file__'))
            if self.CRAWLERS in fileDir:
                fileName = os.path.join(fileDir, fileName)
            else:
                fileName = os.path.join(fileDir, self.CRAWLERS, fileName)

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
        for event in output:
            self.DB.run("INSERT INTO Events VALUES (DEFAULT,%s,%s,%s,to_timestamp(%s),to_timestamp(%s),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);",[
                event.get("source_type"),
                event.get("currency"),
                event.get("category"),
                event.get("start_time"),
                event.get("event_end_time"),
                event.get("id"),
                event.get("price"),
                event.get("title"),
                event.get("description"),
                event.get("longitude"),
                event.get("latitude"),
                event.get("api"),
                event.get("genre"),
                event.get("subGenre"),
                event.get("city"),
                event.get("country")
            ])
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
    def buildOptions(self, options):
        strOptions = ""

        for index, key in enumerate(options):
            strOptions += str(key) + self.EQUALS + str(options[key])
            if index is not len(options) - 1:
                strOptions += self.AMPERSAND

        return strOptions

    # Opens the file with the JSON that specifics the parameters of the request
    def readRequestFile(self, fileName):
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        if self.CRAWLERS in fileDir:
            fileName = os.path.join(fileDir, fileName)
        else:
            fileName = os.path.join(fileDir, self.CRAWLERS, fileName)

        try:
            with open(fileName, 'r') as file:
                content = self.jsonToPy(file.read())
        except IOError:
            print('Could not read request parameters file')
            sys.exit()
        except json.JSONDecodeError:
            print('Invalid input options')
            sys.exit()
        return content

    # basic execution of the script
    def run(self):
        jsonOptions = self.readRequestFile(Crawler.request_params_file)
        strOptions = self.buildOptions(jsonOptions)
        response = self.request(strOptions)

        mapping = self.loadMapping(Crawler.mapping_file)
        output = self.parseEvents(response, mapping)
        self.outputEvents(Crawler.output_file, output)

        print('done')

    # make multiple requests in one command (call if request params is a list)
    def superRequest(self):
        optionsList = self.readRequestFile(Crawler.request_params_file)

        for options in optionsList:
            strOptions = self.buildOptions(options)
            response = self.request(strOptions)
            mapping = self.loadMapping(Crawler.mapping_file)
            output = self.parseEvents(response, mapping)
            self.appendEvents(Crawler.output_file, output)

            print('done')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--request')
    parser.add_argument('-m', '--mapping')
    parser.add_argument('-o', '--output')
    parser.add_argument('-a', '--api')
    parser.add_argument('-s', '--super', action='store_true')
    args = parser.parse_args()

    if args.request is not None:
        Crawler.request_params_file = args.request

    if args.mapping is not None:
        Crawler.mapping_file = args.mapping

    if args.output is not None:
        Crawler.output_file = args.output

    if args.api is not None:
        crawler = Crawler(args.api)
    else:
        crawler = Crawler()

    if args.super:
        crawler.superRequest()
    else:
        crawler.run()
