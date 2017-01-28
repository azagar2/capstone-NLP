import socket,os,_thread,time,json

class NetworkAdapter:
	# this is where the unix file-socket lives
	SOCKET_LOCATION = "/tmp/blue-shift-adapter";
	# enables / disables debug logging.
	DEBUG = False;

	# Creates a linux file socket connection
	def __init__(self):
		self.callbacks = {};
		self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		try:
			os.remove(self.SOCKET_LOCATION)
		except OSError:
			pass;

	# Sends a debug message
	# @param {String} message
	def debug(self, message):
		if self.DEBUG:
			print("DEBUG::NetworkAdapter: "+message);

	# Add a command
	# @param {String} command
	# @param {Function} callback for the command
	def addCommand(self,command,commandCallback):
		self.callbacks[command] = commandCallback;

	# actually runs the adapter
	# WARNING: BLOCKING CALL
	def run(self):
		self.socket.bind(self.SOCKET_LOCATION)
		self.socket.listen(1)
		self.debug("socket running at "+self.SOCKET_LOCATION);
		while 1:
			conn, addr = self.socket.accept()
			self.debug("got server connection");
			while 1:
				data = conn.recv(1024)
				if not data: break;
				commandData = json.loads(data.decode("utf-8"));
				self.debug("got message:"+data.decode("utf-8"));

				def respond(response):
					response = {'id':commandData.get('id'),'response':response};
					self.debug("sending response:"+json.dumps(response));
					conn.send(json.dumps(response).encode("utf-8"));

				if 'id' not in commandData:
					conn.send('{"error":"no id parameter"}'.encode("utf-8"));
					pass;
				elif 'command' not in commandData:
					error = {"error":"no command parameter","id":commandData.get("id")}
					conn.send(json.dumps(error).encode("utf-8"));
					pass;
				elif commandData.get('command') not in self.callbacks:
					error = {"error":"unknown command","id":commandData.get("id")}
					conn.send(json.dumps(error).encode("utf-8"));
					pass;
				else:
					callback = self.callbacks[commandData.get('command')];
					params = commandData.get("params",[]);
					_thread.start_new_thread(callback,(params,respond,));
			self.debug("client went away");
			conn.close();