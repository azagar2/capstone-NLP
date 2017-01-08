import socket,json,sys


class NetworkTester:

	SOCKET_LOCATION = "/tmp/blue-shift-adapter";

	'''
	This is simply a sample for the node server to replace
	This is useful for testing your commands and making sure everything works.
	'''
	def __init__(self):
		self.counter = 0;
		self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.socket.connect(self.SOCKET_LOCATION)

	'''
	Send raw input to the socket.
	Checks the "ENTIRE result"
	'''
	def send(self,message,expectedResponse,testName):
		self.socket.send(message.encode("utf-8"));
		data = self.socket.recv(1024);
		self.printResult(data.decode("utf-8"),expectedResponse,testName);

	def sendCommand(self,command,expectedResponse,testName):
		self.counter += 1;
		command = {"id":self.counter,"command":command}
		self.socket.send(json.dumps(command).encode("utf-8"));
		data = self.socket.recv(1024);
		data = json.loads(data.decode("utf-8"));
		self.printResult(data.get("response"),expectedResponse,testName);

	def printResult(self,input,expected,type):
		if input == expected:
			sys.stdout.write(u'\u2713');
			sys.stdout.write(type);
		else:
			sys.stdout.write(u'\u2717');
			sys.stdout.write("Did not " + type);
			sys.stdout.write("\n")
			sys.stdout.write(input);
			sys.stdout.write("\n")
			sys.stdout.write(expected);
		sys.stdout.write("\n")
		sys.stdout.flush();

tester = NetworkTester();

tester.send('{"test":"true"}','{"error":"no id parameter"}',"fail on missing Id")
tester.send('{"id":1}','{"id": 1, "error": "no command parameter"}',"fail on missing command");
tester.send('{"id":2,"command":"test"}','{"id": 2, "error": "unknown command"}',"fail on unknown command");

tester.sendCommand("clickImpression","click impression registered","register click impressions");
tester.sendCommand("excludeImpression","exclude impression registered","register exclude impressions");
tester.sendCommand("purchaseImpression","purchase impression registered","register purchase impressions");