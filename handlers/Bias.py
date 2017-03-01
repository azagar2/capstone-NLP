from utils import database;
from datetime import datetime;
from handlers import AbstractHandler
from threading import Timer

class BiasHandler(AbstractHandler.Handler):
	# enables / disables debug logging.
	DEBUG = True;

	ADMIN ='admin';
	PROMOTION = 'promotion';
	EXCLUDE = 'exclude';

	# this class handles and saves incoming impression messages that can be
	# used to update the user models.
	def __init__(self):
		self.db = database.DB();
		self.commands = [['addBias',[int,str,int,int,int]],['deleteBias',[int]],['listBiases',[bool]]];	
		self.__loadFilters();

	# add a Bias
	# @param {[int,str,int,int,int]} params
	# @params {Function} respond
	def addBias(self,params,respond):
		if params[1] not in {self.ADMIN,self.PROMOTION,self.EXCLUDE}:
			return respond("invalid type");

		# params are: [eventId, type, weight, startDate, endDate];
		startTime = datetime.fromtimestamp(params[3]/1000.0);
		endTime = datetime.fromtimestamp(params[4]/1000.0);
		if datetime.now() > startTime:
			self.__addBias(params[0],params[2]);
		self.db.run("INSERT INTO Biases VALUES (DEFAULT,%s,%s,%s,%s,%s);",[
			params[0],
			params[1],
			params[2],
			startTime,
			endTime
		]);
		respond("added Bias");

	# delete a Bias
	# @param {[int]} params
	# @params {Function} respond
	def deleteBias(self,params,respond):
		# params are: [biasId]
		bias = self.db.get("SELECT eventId,weight,case WHEN(NOW() BETWEEN startTime AND endTime) THEN 'TRUE' else 'FALSE' end as active_status FROM Biases WHERE id = %s",params);
		if len(bias) == 0:
			self.debug("Could not find Bias "+str(params[0]));
			respond("no such Bias");
			return;
		bias = bias[0];
		if bias[2] == "TRUE" and bias[0] in self.filter:
			self.filter[bias[0]] -= bias[1]
			if self.filter[bias[0]] == 0:
				del self.filter[bias[0]];
		self.db.run("DELETE FROM Biases WHERE id = %s",params);
		respond("deleted Bias");
		return;

	# list all Biases
	# @param {[int]} params
	# @params {Function} respond
	def listBiases(self,params,respond):
		# params are: [activeOnly]
		SQL = "SELECT * FROM Biases"
		if params[0]:
			SQL += " WHERE NOW() BETWEEN startTime AND endTime";
		respond(self.db.get(SQL,[]));

	# add a bias
	# @param {int} 
	def __addBias(self,eventId,weight):
		if eventId in self.filter:
			self.filter[eventId] += weight;
			return;
		self.filter[eventId] = weight;

	# filter events
	# by adjusting their weightings.
	# @param {[Events]}
	# @return {[Events]}
	def filter(self,eventList):
		for event in eventList:
			if eventId in self.filter:
				event.weight *= (100.0 + self.filter[eventId])/100.0
		return eventList;

	# reload Bias filter
	# should be performed once a day at midnight (00:00:01)
	# to ensure filter is up to date
	def __loadFilters(self):
		self.debug("biases initialized");
		SQL = "SELECT eventId, SUM(weight) FROM Biases WHERE NOW() BETWEEN startTime AND endTime GROUP BY eventId;";
		biases = self.db.get(SQL,[]);
		self.filter = {};
		for bias in biases:
			self.__addBias(bias[0],bias[1]);
		today=datetime.today()
		midnight=today.replace(day=today.day+1, hour=0, minute=0, second=0, microsecond=0)
		delta_t=midnight-today;
		self.t = Timer(delta_t.seconds+1, self.__loadFilters);
		self.t.start();
