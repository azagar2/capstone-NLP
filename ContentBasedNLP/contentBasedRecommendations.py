import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import math
import numpy as np
import json


""" Denver: 39.739236, -104.990251 """
""" Toronto: 43.653226, -79.383184 """
""" Mississauga: 43.589045, -79.644120 """
""" London: 42.984923, -81.245277 """

lat = 43.653226
long = -79.383184



def main():

    """ ONE USER'S DATA """
    # Need to extract the event ID from each past event the user has gone to
    # Take most recent past 5 events (within the last 2 years?)
    # The most recent event has a higher weighting

    """ USER DATA SOURCE """
    # assume that index 1 indicates most recently purchased event, then increases with past purchases
    userEvents = pd.read_json("userEventsTest.json")

    """ EVENT DATA SOURCE """
    ds = pd.read_json("new-events.json")
    newEvents = ds.copy()

    """ MAKE CATEGORIES NUMERICAL """
    ds['category'] = ds['category'].replace(['music'], '1')
    print(ds)


    """ GET ALL PRE-PROCESSED EVENTS FROM SINGLE USER'S PAST PURCHASES """
    pieces = {}
    for idx, event in userEvents.iterrows():
        filt = preProcessEvents(newEvents, event.latitude, event.longitude, idx+1)
        pieces[idx+1] = filt
    result = pd.concat(pieces)
    #print(result)

    #nlp(ds)

    """ ADD  """


    """ APPLY NLP ON PRE-PROCESSED DATAFRAME """




def preProcessEvents(ds, lat, long, rank):

    df = ds.copy()
    df = df.loc[(df.loc[:,('latitude')] <= lat+2) & (df.loc[:,('latitude')] >= lat-2) & (df.loc[:,('longitude')] <= long+2) & (df.loc[:,('longitude')] >= long-2)]
    df.loc[:,('distance')] = df.apply(latLongToDistance, axis=1)
    filt = df.loc[(df.loc[:,('distance')] <= 3)]
    return filt


def latLongToDistance(row):

    return math.sqrt(math.pow(row['latitude']-lat,2) + math.pow(row['longitude']-long, 2))


def nlp(ds):

    """ DICTIONARIES """
    di = dict()


    """ TF-IDF for TITLES/DESCRIPTION COMBO """
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(ds['title']+ " " + ds['description'])
    cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)


    """ ITERATE THOUGH PANDAS DATAFRAME """

    for idx, row in ds.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-50:-1]
        similar_items = [(cosine_similarities[idx][i], ds['id'][i]) for i in similar_indices]
        title = similar_items[0][1]
        di[title] = similar_items[1:]
        #break


    #print(diTitles['Techweek | Chicago 2015'])

    for key, value in di.items():
        print(key, value)

    print("--------------")


""" STOP-WORDS """
#bad_words = set(['ticket', 'tickets', 'event', 'events', 'time', 'door', 'entrance'])


"""
Need to do:
First, make sure that only future events are loaded
filter/sort based on....
    latitude and longitude
    event category
    start date (the sooner the better)

do we recommend events based on proximity or weigh category more heavily?

find way to weigh attributes ....
look at events the user has gone to in the past
the more recent events have more weight
go through the most recent 5 or 10 (cap yes or no?)
check to see if user has marked an event as "gift" - if so, do not include in recommendations

"""


""" EXTRA CODE FOR DATAFRAMES """

# data = np.array(['Event','Sim1','Sim2','Sim3','Sim4','Sim5','Sim6'])   #, ['Row1',1,2],['Row2',3,4]])
# df = pd.DataFrame(columns=data)
# print(df)

"""
print(pd.DataFrame(data=data[1:,1:],
                  index=data[1:,0],
                  columns=data[0,1:]))
df.loc[2] = [11, 12, 13]
print(len(df.index))
"""




if __name__ == "__main__":
    main()

