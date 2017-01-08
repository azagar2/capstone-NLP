from handlers import Impressions
from utils import NetworkAdapter

if __name__ == '__main__':
	connector = NetworkAdapter.NetworkAdapter();
	
	impressionsHandler = Impressions.ImpressionsHandler();
	impressionsHandler.register(connector);

	connector.run();

