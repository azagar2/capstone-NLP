import random;
import tensorflow as tf;
import tensorflow.contrib.learn.python.learn as learn;
from sklearn import datasets, metrics;
import numpy as np;
from utils import database;
import datetime

class GeneralRecommender:
	class __GeneralRecommender:
		SQL = "SELECT weekday_bought, weekday_event, category, cost_of_ticket, days_before FROM purchase_metadata;";

		def __init__(self,metrics):
			self.db = database.DB();
			# Fetch all appropriate data
			positiveData = self.db.get(self.SQL,[])
			# randomize for good measure
			random.shuffle(positiveData);
			# validate using test sample only if running analysis
			if(metrics):
				n = int(len(positiveData)/10);
				validationData = positiveData[-n:]
				del positiveData[-n:]
				validationLabels = [1] * len(positiveData);

			# How many samples are we working with?
			NUMBER_OF_SAMPLES = len(positiveData);
			
			# all results are considered positive
			labelsPos = [1] * NUMBER_OF_SAMPLES;

			# generate random data to act as negative data.
			negativeData = [];
			for x in range(0,NUMBER_OF_SAMPLES):
				# generate random data
				negativeData.append([random.randint(0,6),random.randint(0,6),random.randint(0,12),random.randrange(0,150),random.randrange(0,300)]);
			labelsNeg = [0] * len(negativeData);
			if(metrics):
				for x in range(0,n):
					# generate random data
					randomData = [random.randint(0,6),0,random.randint(0,12),random.randrange(0,150),random.randrange(0,300)];
					randomData[1] = (randomData[0] + randomData[4]) % 7;
					validationData.append([random.randint(0,6),random.randint(0,6),random.randint(0,12),random.randrange(0,150),random.randrange(0,300)]);
				validationLabels += [0] * int(len(validationData) - n);

			# compile data
			testData = np.array(positiveData + negativeData);
			labels = np.array(labelsPos + labelsNeg)
			if(metrics):
				validationData = np.array(validationData);
				validationLabels = np.array(validationLabels);

			feature_columns = learn.infer_real_valued_columns_from_input(testData);
			self.classifier = learn.DNNRegressor(hidden_units=[20, 40,40, 20], feature_columns=feature_columns)
			self.classifier.fit(testData, labels, steps=200, batch_size=32);

		def recommend(self,events):
			return list(self.classifier.predict(np.array(self.__parseEvents(events)),as_iterable=True));

		def __parseEvents(self,events):
			parsedEvents = [];
			for event in events:
				parsedEvent = [];
				# Today's date
				today = datetime.datetime.today();
				# Event Date
				eventDate = event[4];
				parsedEvent.append(today.weekday());
				parsedEvent.append(eventDate.weekday());				
				#category
				parsedEvent.append(self.__getCategory(event[3]));
				#price
				parsedEvent.append(event[7]);
				# days until event
				parsedEvent.append((today - eventDate).days);
				parsedEvents.append(parsedEvent);
			return parsedEvents;

		def __getCategory(self, category):
			return {
				'sports': 0,
				'performing-arts': 1,
				'music':2,
				'comedy':3,
				'fashion':4,
				'film':5,
				'other':6,
				'crafts':7,
				'food-drink':8,
				'social':9,
				'business':10,
				'tech':11
			}.get(category, 6);

		
	# instance of singleton
	instance = None;
	ANALYSE = False;
	# singleton constructor
	def __init__(self):
		if not GeneralRecommender.instance:
			# TODO: load connection config in from a file here.
			GeneralRecommender.instance = GeneralRecommender.__GeneralRecommender(GeneralRecommender.ANALYSE);

	# proxy function
	def __getattr__(self, name):
		return getattr(self.instance, name);