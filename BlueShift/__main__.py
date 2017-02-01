from handlers import Impressions
from handlers import Bias
from utils import NetworkAdapter

if __name__ == '__main__':
	connector = NetworkAdapter.NetworkAdapter();

	# add handlers for adding impressions
	handlers = [
		Impressions.ImpressionsHandler(),
		Bias.BiasHandler()
	];
	for handler in handlers:
		handler.register(connector);

	# Run the connector
	connector.run();
	# ---- anything after this point never gets called ----
