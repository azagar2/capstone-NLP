from utils import database;
from datetime import datetime;
from handlers import AbstractHandler

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

	# add a Bias
	# @param {[int,str,int,int,int]} params
	# @params {Function} respond
	def addBias(self,params,respond):
		if params[1] not in {self.ADMIN,self.PROMOTION,self.EXCLUDE}:
			return respond("invalid type");
		# params are: [eventId, type, weight, startDate, endDate];
		self.db.run("INSERT INTO Biases VALUES (DEFAULT,%s,%s,%s,%s,%s);",[
			params[0],
			params[1],
			params[2],
			datetime.fromtimestamp(params[3]/1000.0),
			datetime.fromtimestamp(params[4]/1000.0)
		]);
		respond("added Bias");

	# delete a Bias
	# @param {[int]} params
	# @params {Function} respond
	def deleteBias(self,params,respond):
		# params are: [biasId]
		self.debug("Deleting bias "+str(params[0]));
		self.db.run("DELETE FROM Biases WHERE id = %s",[params[0]]);
		respond("deleted Bias");

	# list all Biases
	# @param {[int]} params
	# @params {Function} respond
	def listBiases(self,params,respond):
		# params are: [activeOnly]
		SQL = "SELECT * FROM Biases"
		if params[0]:
			SQL += " WHERE NOW() BETWEEN startTime AND endTime";
		respond(self.db.get(SQL,[]));

