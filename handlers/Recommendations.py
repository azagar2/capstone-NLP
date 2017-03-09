from utils import database;
from datetime import datetime;
from handlers import AbstractHandler;
from recommenders import GeneralRecommender, ContentRecommender;

class RecommendationHandler(AbstractHandler.Handler):
	# enables / disables debug logging.
	DEBUG = True;

	# this class handles and saves incoming impression messages that can be
	# used to update the user models.
	def __init__(self):
		self.db = database.DB();
		self.commands = [["getAnonymousRecommendations",[int]],["getContentRecommendations",[str,str,str]]];
		self.__loadRecommenders();

	def getAnonymousRecommendations(self,params,respond):
		Y = self.recommenders[0].recommend(self.events);
		respond([x for (y,x) in sorted(zip(Y,self.events))][:params[0]]);

	def getRecommendations(self,params,respond):
		print(params)
		recom = ContentRecommender.ContentRecommender(params)
		recs = recom.recommend()
		print(recs)


	# load recommenders based on existing data.
	def __loadRecommenders(self):
		self.debug("Recommenders initializing...");
		DB = database.DB();
		self.events = DB.get("SELECT * FROM Events;",[]);

		self.recommenders = [GeneralRecommender.GeneralRecommender()];
		self.debug("Recommenders initialized");
