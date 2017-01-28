import psycopg2;

class DB:
	class __DB:
		DEBUG = False;

		# Singleton used to access the database
		# @param {String} connection configuration text
		def __init__(self, connectionConfig):
			self.connected = False;
			self.__CONNECTION_STRING = connectionConfig

		# Debug
		# prints debug messages iff DEBUG is set to true
		# @param {String} message
		def debug(self,message):
			if self.DEBUG:
				print("DEBUG::DB:",message);

		# Error
		# prints error message in red.
		def error(self,message):
			# the weird characters add red colour to error messages.
			# because everyone likes logs that are colourful.
			print("\033[0;31mERROR::DB:",message,'\033[0m');

		# @private
		# Get Cursor
		# prints debug messages iff DEBUG is set to true
		# @param {String} message
		def __getCursor(self):
			if not self.connected:
				self.__connect();
			return self.conn.cursor();

		# @private
		# Connect
		# connects to the database if no connection is present.
		def __connect(self):
			self.conn = psycopg2.connect(self.__CONNECTION_STRING);
			self.connected = True;
			self.debug("connected");

		# Run
		# runs a command and commits it.
		# @param {String} SQL command
		def run(self,command,params):
			try:
				cursor = self.__getCursor();
				self.debug("running command:"+command);
				cursor.execute(command,params);
				self.conn.commit();
			except Exception as e:
				self.connected = False;
				self.error("Uh oh, can't connect. Invalid dbname, user or password?")
				self.error(e);

		# Get
		# fetches the result of an executed command.
		# @param {String} SQL command
		# @param {Array} set of row objects
		def get(self,command):
			result = "ERROR: can't connect";
			try:
				cursor = self.__getCursor();
				cursor.execute(command);
				result = cursor.fetchall();
				self.debug(result);
				self.conn.commit();
			except Exception as e:
				self.connected = False;
				print("Uh oh, can't connect. Invalid dbname, user or password?")
				print(e);
			return result;

	# instance of singleton
	instance = None

	# singleton constructor
	def __init__(self):
		if not DB.instance:
			# TODO: load connection config in from a file here.
			DB.instance = DB.__DB("dbname='testdb'");

	# proxy function
	def __getattr__(self, name):
		return getattr(self.instance, name);