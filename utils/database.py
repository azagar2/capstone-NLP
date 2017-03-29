import psycopg2;
import json;
import os;
from utils import config;

class DB:
	class __DB:
		DEBUG = False;

		# Singleton used to access the database
		# @param {String} connection configuration text
		def __init__(self, connectionConfig):
			self.connected = False;
			params = (connectionConfig["host"],
				connectionConfig["database"],
				connectionConfig["username"],
				connectionConfig["password"],
				connectionConfig["port"]);
			self.__CONNECTION_STRING = "host='%s' dbname='%s' user='%s' password='%s' port='%s'" % params;

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
				cursor.execute(self.__validate(command),params);
				self.conn.commit();
			except Exception as e:
				self.connected = False;
				self.error("Uh oh, can't connect. Invalid dbname, user or password?")
				self.error(e);

		# Get
		# fetches the result of an executed command.
		# @param {String} SQL command
		# @param {Array} set of row objects
		def get(self,command,params):
			result = "ERROR: can't connect";
			try:
				cursor = self.__getCursor();
				cursor.execute(self.__validate(command),params);
				result = cursor.fetchall();
				self.debug(result);
				self.conn.commit();
			except Exception as e:
				self.connected = False;
				print("Uh oh, can't connect. Invalid dbname, user or password?")
				print(e);
			return result;

		def __validate(self,command):
			if command.endswith(";"):
				return command;
			return command + ";";

	# instance of singleton
	instance = None

	# singleton constructor
	def __init__(self):
		if not DB.instance:
			conf = config.Config();
			DB.instance = DB.__DB(conf.data["pgsql"]);

	# proxy function
	def __getattr__(self, name):
		return getattr(self.instance, name);