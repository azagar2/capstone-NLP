from abc import ABCMeta

class Handler:

	__metaclass__ = ABCMeta

	# For debug messages from this class
	def debug(self,message):
		if(self.DEBUG):
			print("DEBUG::ImpressionsHandler:",message);

	# registers the handler with the main class.
	# @param {NetworkAdapter}
	def register(self, networkAdapter):
		for command in self.commands:
			networkAdapter.addCommand(command[0],getattr(self,command[0]),command[1]);