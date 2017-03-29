import psycopg2;
import json;
import os;

class Config:
	class __Config:
		data = {};
		# Singleton used to access the database
		# @param {String} connection configuration text
		def __init__(self,config):
			self.data = config;

		# Basic caching check
		# with guards incase of config errors.
		def cache(self):
			if not "mlEngine" in self.data:
				return False;
			if not "cache" in self.data["mlEngine"]:
				return False;
			return self.data["mlEngine"]["cache"];

		def heuristics(self):
			if not "mlEngine" in self.data:
				return {};
			if not "heuristics" in self.data["mlEngine"]:
				return {};
			return self.data["mlEngine"]["heuristics"];
	# instance of singleton
	instance = None

	# singleton constructor
	def __init__(self):
		if not Config.instance:
			fileDir = os.path.dirname(os.path.realpath('__file__'));
			fileName = os.path.join(fileDir, 'frontEnd','config','config.live.json');
			try:
				with open(fileName) as data_file:
					config_data = json.load(data_file);
			except IOError:
				fileName = os.path.join(fileDir, 'frontEnd','config','config.dev.json');
				try:
					with open(fileName) as data_file:
						config_data = json.load(data_file);
				except IOError:
					print("no config file found");
					sys.exit();
			except json.JSONDecodeError:
				print('Invalid output content')
				sys.exit()
			Config.instance = Config.__Config(config_data);

	# proxy function
	def __getattr__(self, name):
		return getattr(self.instance, name);