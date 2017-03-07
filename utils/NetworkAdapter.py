import socket,os,_thread,time,json,datetime
from functools import partial

class NetworkAdapter:
	# this is where the unix file-socket lives
	SOCKET_LOCATION = "/tmp/blue-shift-adapter";
	# enables / disables debug logging.
	DEBUG = True;

	# Creates a linux file socket connection
	def __init__(self):
		self.callbacks = {};
		self.commandParameters = {};
		self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.date_handler = lambda obj: (
			int(time.mktime(obj.timetuple()) * 1000.0)
			if isinstance(obj, datetime.datetime)
			or isinstance(obj, datetime.date)
			else None
		)
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
	def addCommand(self,command,commandCallback, params):
		self.callbacks[command] = commandCallback;
		self.commandParameters[command] = params;

	# Validate
	# validates the params so that we can garantee types in all commands
	# @param {Object} params (checks that it's an array of the appropriate type)
	# @param {[Class]} types
	def validate(self,params,types):
		# params is an array
		if type(params) is not list:
			return False;
		# ... of the right number 
		if len(params) is not len(types):
			return False;
		# ... of appropriate variables.
		for idx, param in enumerate(params):
			if type(param) is not types[idx]:
				return False;
		return True;

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

				def respond(commandId,response):
					response = {'id':commandId,'response':response};
					self.debug("sending response:"+json.dumps(response,default=self.date_handler));
					response = json.dumps(response,default=self.date_handler);
					chunksize = 8000;
					chunks = [response[i:i+chunksize] for i in range(0, len(response), chunksize)];
					for idx,chunk in enumerate(chunks):
						identifier = str(commandId)+":"+str(idx)+":"+str(len(chunks)-1);
						conn.send((identifier + "|" + chunk).encode("utf-8"));

				if 'id' not in commandData:
					conn.send('e|{"error":"no id parameter"}'.encode("utf-8"));
					pass;
				elif 'command' not in commandData:
					error = {"error":"no command parameter","id":commandData.get("id")}
					conn.send(("e|"+json.dumps(error)).encode("utf-8"));
					pass;
				elif commandData.get('command') not in self.callbacks:
					error = {"error":"unknown command","id":commandData.get("id")}
					conn.send(("e|"+json.dumps(error)).encode("utf-8"));
					pass;
				else:
					callback = self.callbacks[commandData.get('command')];
					params = commandData.get("params",[]);
					if self.validate(params,self.commandParameters[commandData.get('command')]):
						_thread.start_new_thread(callback,(params,partial(respond,commandData.get("id")),));
					else:
						error = {"error":"invalid parameters","id":commandData.get("id")}
						conn.send(("e|"+json.dumps(error)).encode("utf-8"));
			self.debug("client went away");
			conn.close();