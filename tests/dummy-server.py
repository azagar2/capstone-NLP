import socket,json,sys


class NetworkTester:

	SOCKET_LOCATION = "/tmp/blue-shift-adapter";

	def __init__(self):
		self.counter = 0;
		self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.socket.connect(self.SOCKET_LOCATION)

	def send(self,message,expectedResponse,testName):
		self.socket.send(message.encode("utf-8"));
		data = self.socket.recv(1024);
		self.printResult(expectedResponse == data.decode("utf-8"),testName);

	def sendCommand(self,command,expectedResponse,testName):
		self.counter += 1;
		command = {"id":self.counter,"command":command}
		self.socket.send(json.dumps(command).encode("utf-8"));
		data = self.socket.recv(1024);
		data = json.loads(data.decode("utf-8"));
		self.printResult(expectedResponse == data.get("response"),testName);

	def printResult(self,result,type):
		if result:
			sys.stdout.write(u'\u2713');
		else:
			sys.stdout.write(u'\u2717');
		sys.stdout.write(type);
		sys.stdout.write("\n")
		sys.stdout.flush();

tester = NetworkTester();

tester.send('{"test":"true"}','{"error":"no id parameter"}',"fail on missing Id")
tester.send('{"id":1}','{"error":"no command parameter"}',"fail on missing command");
tester.send('{"id":2,"command":"test"}','{"error":"unknown command"}',"fail on unknown command");

tester.sendCommand("clickImpression","click impression registered","register click impressions");
tester.sendCommand("excludeImpression","exclude impression registered","register exclude impressions");
tester.sendCommand("purchaseImpression","purchase impression registered","register purchase impressions");