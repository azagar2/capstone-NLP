import socket,json,sys

FIYAAAAAAAH='🔥 ';
BOOOM='💣 ';

class NetworkTester:
	# this is where the unix file-socket lives
	SOCKET_LOCATION = "/tmp/blue-shift-adapter";

	# This is simply a sample for the node server to replace
	# This is useful for testing your commands and making sure everything works.
	def __init__(self):
		self.counter = 0;
		self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.socket.connect(self.SOCKET_LOCATION)

	# Send raw input to the socket.
	# Checks the *ENTIRE* result, so make sure you format your json properly
	def send(self,message,expectedResponse,testName):
		self.socket.send(message.encode("utf-8"));
		data = self.socket.recv(2048);
		self.printResult(data.decode("utf-8"),expectedResponse,testName);

	# Send a command (as a valid json) and receive a valid response
	# checks only the response portion.
	def sendCommand(self,command,params,expectedResponse,testName):
		self.counter += 1;
		command = {"id":self.counter,"command":command, "params":params}
		self.socket.send(json.dumps(command).encode("utf-8"));
		data = self.socket.recv(2048);
		data = json.loads(data.decode("utf-8"));
		response = data.get("response","ERROR:"+data.get("error","unknown"));
		self.printResult(response,expectedResponse,testName);
		return response;

	def printResult(self,input,expected,type):
		if expected == "":
			sys.stdout.write(FIYAAAAAAAH);
			sys.stdout.write(type);
			sys.stdout.write("\nreturned "+json.dumps(input));
		elif input == expected:
			sys.stdout.write(FIYAAAAAAAH);
			sys.stdout.write(type);
		else:
			sys.stdout.write(BOOOM);
			sys.stdout.write("Did not " + type);
			sys.stdout.write("\n Received:   ")
			sys.stdout.write(json.dumps(input));
			sys.stdout.write("\n Expected:   ")
			sys.stdout.write(json.dumps(expected));
		sys.stdout.write("\n")
		sys.stdout.flush();

tester = NetworkTester();

tester.send('{"test":"true"}','{"error":"no id parameter"}',"fail on missing Id")
tester.send('{"id":1}','{"error": "no command parameter", "id": 1}',"fail on missing command");
tester.send('{"id":2,"command":"test"}','{"error": "unknown command", "id": 2}',"fail on unknown command");

testUserId = 4;

tester.sendCommand("clickImpression",[testUserId],"click impression registered","register click impressions");
tester.sendCommand("excludeImpression",[testUserId],"exclude impression registered","register exclude impressions");
tester.sendCommand("buyImpression",[testUserId],"buy impression registered","register buy impressions");

tester.sendCommand("addBias",[4,"admin",100,1485957433624,1486907833624],"added Bias","added a bias");
biasList = tester.sendCommand("listBiases",[True],"","list all biases");
tester.sendCommand("deleteBias",[biasList[len(biasList)-1][0]],"deleted Bias","delete newly created bias");

