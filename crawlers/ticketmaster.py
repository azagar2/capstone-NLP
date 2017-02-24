import urllib.request
import urllib.error
import json
import sys
import argparse


class TicketMasterCrawler:

    baseUrl = 'https://app.ticketmaster.com/discovery/v2/events.json?'
    apiKey = 'Ry4V2S9yfBqhz1MFpeRJnEbAxcp0nSGQ'

    EQUALS = '='
    AMPERSAND = '&'
    APIKEY = 'apikey'
    EMBEDDED = '_embedded'
    EVENTS = 'events'
    SLASH = '/'
    ROOT = 'root'
    PATH = 'path'
    REQUIRED = 'required'
    TYPE = 'type'

    STRING = 'string'
    FLOAT = 'float'
    INT = 'int'

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

                    if outputType == self.FLOAT:
                        feature = float(feature)
                    elif outputType == self.INT:
                        feature = int(float(feature))

                    newEvent[key] = feature

                output.append(newEvent)

        except KeyError as error:
            print('Error parsing the key: ' + str(error))
            sys.exit()
        except IndexError as error:
            print(str(error))
            sys.exit()

        return output

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
                for event in output:
                    file.write(self.pyToJson(output, True))

                print('Outputting events')
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
        jsonOptions = self.readRequestFile(crawler.request_params_file)
        strOptions = self.buildOptions(jsonOptions)
        response = self.request(strOptions)

        # response = self.jsonToPy(open('temp.txt', 'r').read())  # this is for testing

        mapping = self.loadMapping(crawler.mapping_file)
        output = self.parseEvents(response, mapping)
        self.outputEvents(crawler.output_file, output)

        print('done')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--request')
    parser.add_argument('-m', '--mapping')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

    if args.request is not None:
        TicketMasterCrawler.request_params_file = args.request

    if args.mapping is not None:
        TicketMasterCrawler.mapping_file = args.mapping

    if args.output is not None:
        TicketMasterCrawler.output_file = args.output

    crawler = TicketMasterCrawler()
    crawler.run()
