class ImpressionsHandler:
	# enables / disables debug logging.
	DEBUG = True;

	# this class handles and saves incoming impression messages that can be
	# used to update the user models.
	def __init__(self):
		self.commands = ['clickImpression','purchaseImpression','excludeImpression'];

	# For debug messages from this class
	def debug(self,message):
		if(self.DEBUG):
			print("DEBUG::ImpressionsHandler:"+message);

	# registers the handler with the main class.
	# @param {NetworkAdapter}
	def register(self, networkAdapter):
		networkAdapter.addCommand('clickImpression',self.clickImpression);
		networkAdapter.addCommand('purchaseImpression',self.purchaseImpression);
		networkAdapter.addCommand('excludeImpression',self.excludeImpression);

	# called when a click impression is recorded.
	# @param {Array} parameters from call (empty in this case)
	# @param {Function} callback
	def clickImpression(self,params,respond):
		self.debug("got click impression");
		respond("click impression registered");

	# called when a purchase impression is recorded.
	# @param {Array} parameters from call (empty in this case)
	# @param {Function} callback
	def purchaseImpression(self,params,respond):
		self.debug("got purchase impression");
		respond("purchase impression registered");

	# called when an exclude impression is recorded.
	# @param {Array} parameters from call (empty in this case)
	# @param {Function} callback
	def excludeImpression(self,params,respond):
		self.debug("got exclude impression");
		respond("exclude impression registered");
