class ImpressionsHandler:
	DEBUG = True;

	def __init__(self):
		self.commands = ['clickImpression','purchaseImpression','excludeImpression'];

	def debug(self,message):
		if(self.DEBUG):
			print("DEBUG::ImpressionsHandler:"+message);

	def register(self, networkAdapter):
		networkAdapter.addCommand('clickImpression',self.clickImpression);
		networkAdapter.addCommand('purchaseImpression',self.purchaseImpression);
		networkAdapter.addCommand('excludeImpression',self.excludeImpression);

	def clickImpression(self,params,respond):
		self.debug("got click impression");
		respond("click impression registered");

	def purchaseImpression(self,params,respond):
		self.debug("got purchase impression");
		respond("purchase impression registered");

	def excludeImpression(self,params,respond):
		self.debug("got exclude impression");
		respond("exclude impression registered");