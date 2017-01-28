from handlers import Impressions
from utils import NetworkAdapter

if __name__ == '__main__':
	connector = NetworkAdapter.NetworkAdapter();

	# add handlers for adding impressions
	impressionsHandler = Impressions.ImpressionsHandler();
	impressionsHandler.register(connector);

	# Run the connector
	connector.run();
	# ---- anything after this point never gets called ----
