from utils import database;

class ImpressionsHandler:
	# enables / disables debug logging.
	DEBUG = True;

	CLICK = 'click';
	BUY = 'buy';
	EXCLUDE = 'exclude';
	# this class handles and saves incoming impression messages that can be
	# used to update the user models.
	def __init__(self):
		self.db = database.DB();
		self.commands = ['clickImpression','buyImpression','excludeImpression'];

	# For debug messages from this class
	def debug(self,message):
		if(self.DEBUG):
			print("DEBUG::ImpressionsHandler:",message);

	# register an impression to the database.
	# @param {int} userId
	# @param {String} impression type (one of CLICK, BUY or EXCLUDE)
	# @param {Function} callback.
	def __registerImpression(self,userId,impressionType,respond):
		self.debug("got "+impressionType+" impression");
		self.db.run("INSERT INTO Impressions VALUES (DEFAULT,%s,%s);",(userId,impressionType));
		respond(impressionType+" impression registered");

	# registers the handler with the main class.
	# @param {NetworkAdapter}
	def register(self, networkAdapter):
		for command in self.commands:
			networkAdapter.addCommand(command,getattr(self,command));

	# called when a click impression is recorded.
	# @param {Array} parameters from call (empty in this case)
	# @param {Function} callback
	def clickImpression(self,params,respond):
		self.__registerImpression(params[0],self.CLICK,respond);
		

	# called when a purchase impression is recorded.
	# @param {Array} parameters from call (empty in this case)
	# @param {Function} callback
	def buyImpression(self,params,respond):
		self.__registerImpression(params[0],self.BUY,respond);

	# called when an exclude impression is recorded.
	# @param {Array} parameters from call (empty in this case)
	# @param {Function} callback
	def excludeImpression(self,params,respond):
		self.__registerImpression(params[0],self.EXCLUDE,respond);
