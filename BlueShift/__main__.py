from handlers.Impressions import ImpressionsHandler;
from handlers.Bias import BiasHandler;
from handlers.Recommendations import RecommendationHandler;
from utils.NetworkAdapter import NetworkAdapter;

if __name__ == '__main__':
	connector = NetworkAdapter();

	#add handlers for adding impressions
	biases = BiasHandler()
	handlers = [
		ImpressionsHandler(),
		biases,
		RecommendationHandler(biases)
	];
	for handler in handlers:
		handler.register(connector);

	# Run the connector
	connector.run();
	# ---- anything after this point never gets called ----
