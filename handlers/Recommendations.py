from utils import database;
from datetime import datetime;
from handlers import AbstractHandler;
from recommenders import GeneralRecommender, ContentRecommender;
from utils import config;

class RecommendationHandler(AbstractHandler.Handler):
	# enables / disables debug logging.
	DEBUG = True;
	ANONYMOUS_USER = "anon";

	# this class handles and saves incoming impression messages that can be
	# used to update the user models.
	def __init__(self,biases):
		self.db = database.DB();
		self.config = config.Config();
		self.commands = [["getAnonymousRecommendations",[int]],["getRecommendations",[str,str,str]]];
		self.__loadRecommenders();
		self.__cache = {};
		self.biases = biases;

	def getAnonymousRecommendations(self,params,respond):
		respond(self.__getAnonymousRecommendations()[:params[0]]);

	def __getAnonymousRecommendations(self):
		if self.config.cache() and self.ANONYMOUS_USER in self.__cache:
			respond(self.__cache[self.ANONYMOUS_USER][:params[0]]);
			return;
		Y = self.recommenders[0].recommend(self.events);
		Y = [x for (y,x) in sorted(zip(Y,self.events))];
		self.__cache[self.ANONYMOUS_USER] = Y;
		return Y;

	def getRecommendations(self,params,respond):
		self.debug(params);
		anon_recs = self.__getAnonymousRecommendations();
		recommendations = self.recommenders[1].recommend();

		# TODO: filter from biases
		# recs = self.biases.filter();
		# self.debug(recs)
		respond(recommendations[0])


	# load recommenders based on existing data.
	def __loadRecommenders(self):
		self.debug("Recommenders initializing...");
		DB = database.DB();
		self.events = DB.get("SELECT * FROM Events;",[]);

		self.recommenders = [GeneralRecommender.GeneralRecommender(),ContentRecommender.ContentRecommender()];
		self.debug("Recommenders initialized");
