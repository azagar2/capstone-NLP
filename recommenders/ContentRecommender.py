import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from math import radians, cos, sin, asin, sqrt, log
import os
from utils import config;
#from utils import database

""" Denver: 39.739236, -104.990251 """
""" Toronto: 43.653226, -79.383184 """
""" Mississauga: 43.589045, -79.644120 """
""" London: 42.984923, -81.245277 """


class ContentRecommender:

    # Constants
    user_lat = 0
    user_long = 0
    num_past_user_events = 0
    eventRadius = 500 # in km
    nlp_features = ['id', 'title', 'description']

    # User data and pre-processed data
    all_user_events = ''
    user_events = ''
    nlp_data = ''

    # File paths for user and future data
    src = os.path.dirname(os.path.realpath('__file__'));
    future_event_data_file = os.path.join(src, 'ContentBasedNLP','testData','futureEvents.json');
    user_data_file = os.path.join(src, 'ContentBasedNLP','testData','pastEvents.json');
    print(future_event_data_file);
    print(user_data_file);

    def __init__(self, userEvents):

        self.heuristics = config.Config().heuristics();
        #self.db = database.DB()

        # first grab top 3 events from the user using userID
        # now grab the future events

        # assume that index 1 indicates most recently purchased event, then increases with past purchases
        """ USER DATA SOURCE """
        self.all_user_events = pd.read_json(self.user_data_file)
        #self.all_user_events = pd.read_json("testData/userEventsTest.json")
        self.user_events = pd.DataFrame

        # print(self.all_user_events)
        found = False;
        parsedUserEvents = [];
        for i in range(0,len(userEvents)):
            if userEvents[i] != "None":
                parsedUserEvents.append(int(userEvents[i]));
                found = True;
                #tmp_row = self.all_user_events.loc[self.all_user_events['id'] == userEvents[i]]
                # if i == 0:
                #     self.user_events = pd.DataFrame(tmp_row)
                # else:
                #     self.user_events = self.user_events.append(pd.DataFrame(tmp_row))
        parsedUserEvents = list(map(int,parsedUserEvents));
        if not found:
            print("ERROR:events not found");
        print(self.user_events);
        self.user_events = self.all_user_events[self.all_user_events['id'].isin(parsedUserEvents)]
        self.user_events = self.user_events.reset_index(drop=True)
        self.num_past_user_events = len(self.user_events.index)
        if (self.num_past_user_events > 0):
            self.user_lat = self.user_events.loc[0].latitude
            self.user_long = self.user_events.loc[0].longitude

        """ EVENT DATA SOURCE """
        newEvents = pd.read_json(self.future_event_data_file)

        """ INITIAL LOCATION PRE-PROCESSING """
        # 1 deg lat = 111km
        # 1 deg long = cos(lat)*111.321 in km

        pieces = {}
        for idx, event in self.user_events.iterrows():
            longDist = abs(cos(radians(event.latitude)) * 111.321)
            df = newEvents.loc[(newEvents.loc[:,('latitude')] <= event.latitude+4.5) &
                               (newEvents.loc[:,('latitude')] >= event.latitude-4.5) &
                               (newEvents.loc[:,('longitude')] <= event.longitude+longDist) &
                               (newEvents.loc[:,('longitude')] >= event.longitude-longDist)]
            filtered = self.filterLocations(df, event.latitude, event.longitude)
            pieces[idx+1] = filtered
        ds = pd.DataFrame(pd.concat(pieces))
        ds.drop_duplicates(subset='id',inplace=False)
        print(ds);
        """ PRE-PROCESSING FOR NLP """
        self.nlp_data = self.preProcessNLP(ds)
        self.nlp_data = self.nlp_data.drop_duplicates(subset='id',inplace=False)
        #print(nlp_data)
        self.heuristicRecommendations = self.analyseHeuristics(ds);

    def analyseHeuristics(self,events):
        self.user_events["hour_of_day"] = self.user_events["start_time"].dt.hour;
        self.user_events["day_of_week"] = self.user_events["start_time"].dt.dayofweek;
        events["hour_of_day"] = events["start_time"].dt.hour;
        events["day_of_week"] = events["start_time"].dt.dayofweek;
        for idx, event in self.user_events.iterrows():
            events[("_hscore"+str(idx))] = events.apply(lambda row: self.scoreEvent(
                row['distance'],
                row['category'],
                row['price'],
                row['hour_of_day'],
                row['day_of_week'],
                event),axis=1);
        sum_of_weights = 0;
        events["_score"] = 0;
        event_weights = self.heuristics["split"][(len(self.user_events)-1)];
        idx = 0;
        for weight in event_weights:
            sum_of_weights += weight;
            events["_score"] += weight*events[("_hscore"+str(idx))];
            idx+=1;
        events["_score"] = events["_score"]/sum_of_weights;
        print(events);

    def scoreEvent(self,dist,category,price,hour,day,event):
        score = -log(dist+1) * self.heuristics["distance"];
        category = self.__getCategory(category);
        event_category = self.__getCategory(event.category);
        if category == event_category:
            score += self.heuristics["categories_match"];
        elif abs(category - event_category) == 1:
            score += self.heuristics["categories_near"];
        else :
            score += self.heuristics["categories_miss"];
        score += (abs(log(price+1) - log(event.price+1))*self.heuristics["price"]);
        if day < 4:
            if event.day_of_week < 4:
                score += self.heuristics["day_match"];
            else:
                score += self.heuristics["day_miss"];
        else:
            if event.day_of_week < 4:
                score += self.heuristics["day_miss"];
            else:
                score += self.heuristics["day_match"];
        score += abs(hour - event.hour_of_day)*self.heuristics["hour_of_day"];
        return score;

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

    def haversine(self, lon1, lat1, lon2, lat2):
        """ Calculate the great circle distance between two points on the earth (specified in decimal degrees) """
        # convert decimal degrees to radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6367 * c
        return km


    def filterLocations(self, ds, lat, long):
        df = ds.copy()
        df['distance'] = df.apply(lambda row: self.haversine(lat, long, row['latitude'], row['longitude']), axis=1)
        filtered = df.loc[(df.loc[:,('distance')] <= 500)]
        return filtered


    def preProcessNLP(self, df):
        # if ticketmaster event, add genre and sub-genre to description then remove those columns from df

        #df.loc[df['api'] == "ticketmaster", 'description'] = df['description'].str.cat([df['genre'], df['subGenre']], sep=' ')

        # only select specific columns from original dataframe
        ds = df.filter(self.nlp_features, axis=1)
        return ds


    def recommend(self):
        frames = {}
        new_df = self.user_events.copy().filter(self.nlp_features, axis=1)
        new_df = new_df.append(self.nlp_data, ignore_index=True)
        result = self.generateNLPRecommendations(new_df)

        # need to eliminate any instance of old events in recommendations
        for idx, row in self.user_events.iterrows():
            result = result.drop(result[result.id == row.id].index)

        # then group by id and add weights
        result.groupby(by=['id'], sort=False)['weight'].sum()
        result.sort_values(by='weight', inplace=True, ascending=False)

        #print(result)

        del result['title']

        # HANNES HI
        # print(result.set_index('id').T.to_dict(orient='records'))
        return([result['id'].tolist(),result['weight'].tolist()])


    def generateNLPRecommendations(self, ds):

        """ TF-IDF for TITLES/DESCRIPTION COMBO """
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
        tfidf_matrix = tf.fit_transform(ds['title']+ " " + ds['description'])
        cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

        ret_df = pd.DataFrame

        # weighting to add
        weight = 0

        """ ITERATE THROUGH PANDAS DATAFRAME """
        for idx, row in ds.iterrows():
            #if (self.num_past_user_events > 1):
                #weight = ((idx+1)/self.num_past_user_events)*0.5
            similar_indices = cosine_similarities[idx].argsort()[:-20:-1]
            similar_items = [{'id': ds['id'][i],'title': ds['title'][i], 'weight': cosine_similarities[idx][i]+weight} for i in similar_indices]
            if (idx == 0):
                ret_df = pd.DataFrame(similar_items[1:])
            else:
                ret_df = ret_df.append(pd.DataFrame(similar_items[1:]))
            if (idx == self.num_past_user_events-1):
                return(ret_df)

# for testing purposes only.
if __name__ == "__main__":
    recommender = ContentRecommender(["329060","330743","321507"])
    recommender.recommend()
