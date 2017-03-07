import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from geopy.distance import vincenty
import numpy as np
import timeit


""" Denver: 39.739236, -104.990251 """
""" Toronto: 43.653226, -79.383184 """
""" Mississauga: 43.589045, -79.644120 """
""" London: 42.984923, -81.245277 """


class Recommender:

    # Constants
    user_lat = 0
    user_long = 0
    num_past_user_events = 0

    # User data and pre-processed data
    user_events = ''
    nlp_data = ''

    # File paths for user and future data
    user_data_file = "testData/userEventsTest.json"
    future_event_data_file = "testData/VanLaNY3000output.json"


    def __init__(self):

        # assume that index 1 indicates most recently purchased event, then increases with past purchases

        """ USER DATA SOURCE """
        self.user_events = pd.read_json(self.user_data_file)
        self.num_past_user_events = len(self.user_events.index)
        if (self.num_past_user_events > 0):
            self.user_lat = self.user_events.loc[0].latitude
            self.user_long = self.user_events.loc[0].longitude

        """ EVENT DATA SOURCE """
        newEvents = pd.read_json(self.future_event_data_file)

        """ INITIAL LOCATION PRE-PROCESSING """
        pieces = {}
        for idx, event in self.user_events.iterrows():
            filtered = self.filterLocations(newEvents, event.latitude, event.longitude)
            pieces[idx+1] = filtered
        ds = pd.DataFrame(pd.concat(pieces))
        ds.drop_duplicates(subset='id',inplace=True)

        """ PRE-PROCESSING FOR NLP """
        self.nlp_data = self.preProcessNLP(ds)
        #print(nlp_data)


    def latLongToDistance(self, lat1, long1, lat2, long2):
        return vincenty((lat1, long1), (lat2, long2)).km


    def filterLocations(self, ds, lat, long):
        df = ds.copy()
        df['distance'] = df.apply(lambda row: self.latLongToDistance(lat, long, row['latitude'], row['longitude']), axis=1)
        filtered = df.loc[(df.loc[:,('distance')] <= 500)]
        return filtered


    def preProcessNLP(self, df):
        # if ticketmaster event, add genre and sub-genre to description then remove those columns from df
        df.loc[df['api'] == "ticketmaster", 'description'] = df['description'].str.cat([df['genre'], df['subGenre']], sep=' ')
        # only select specific columns from original dataframe
        ds = df.filter(['id', 'title', 'description'], axis=1)
        return ds


    def recommend(self):
        # add event to nlp_data
        frames = {}
        for a in range(0, self.num_past_user_events):
            newset = pd.DataFrame(np.array([[self.user_events.loc[a]['id'], self.user_events.loc[a]['title'], self.user_events.loc[a]['description']]]), columns=['id', 'title', 'description']).append(self.nlp_data, ignore_index=True)
            if (self.num_past_user_events > 1):
                weight = (a/self.num_past_user_events)*0.5
            else: weight = 0
            frames[a] = self.generateNLPRecommendations(newset, weight)

        # generate recommendations
        result = pd.DataFrame(pd.concat(frames, ignore_index=True))
        #print(result.loc[result['weight'] == 0.387071])
        result.groupby(by=['id'], sort=False)['weight'].sum()
        result.sort_values(by='weight', inplace=True, ascending=False)
        del result['title']

        # HANNES HI
        print(result['id'].tolist())
        print(result['weight'].tolist())
        print(result.set_index('id').T.to_dict(orient='records'))
        return(result.set_index('id').T.to_dict(orient='list'))


    def generateNLPRecommendations(self, ds, weight):

        """ TF-IDF for TITLES/DESCRIPTION COMBO """
        tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
        tfidf_matrix = tf.fit_transform(ds['title']+ " " + ds['description'])
        cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

        """ ITERATE THROUGH PANDAS DATAFRAME """
        for idx, row in ds.iterrows():
            similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
            similar_items = [{'id': ds['id'][i],'title': ds['title'][i], 'weight': cosine_similarities[idx][i]+weight} for i in similar_indices]
            return(pd.DataFrame(similar_items[1:]))



if __name__ == "__main__":
    recommender = Recommender()
    recommender.recommend()

