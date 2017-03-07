import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing
from sklearn.cluster import KMeans, MiniBatchKMeans
from geopy.distance import vincenty
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from sklearn.metrics.pairwise import pairwise_distances_argmin


""" Denver: 39.739236, -104.990251 """
""" Toronto: 43.653226, -79.383184 """
""" Mississauga: 43.589045, -79.644120 """
""" London: 42.984923, -81.245277 """

user_lat = 0
user_long = 0
global num_past_user_events


def main():

    """ ONE USER'S DATA """
    # Need to extract the event ID from each past event the user has gone to
    # Take most recent past 3 events (within the last 2 years?)
    # The most recent event has a higher weighting

    global user_lat, user_long, num_past_user_events

    """ USER DATA SOURCE """
    # assume that index 1 indicates most recently purchased event, then increases with past purchases
    userEvents = pd.read_json("testData/userEventsTest.json")
    num_past_user_events = len(userEvents.index)
    user_lat = userEvents.loc[0].latitude
    user_long = userEvents.loc[0].longitude

    """ EVENT DATA SOURCE """
    newEvents = pd.read_json("testData/VanLaNY3000output.json")

    """ FilTER LOCATIONS BASED ON EVENTS FROM SINGLE USER'S PAST PURCHASES """
    pieces = {}
    for idx, event in userEvents.iterrows():
        if idx == 0:
            user_lat = event.latitude
            user_long = event.longitude
        filt = filterLocations(newEvents, event.latitude, event.longitude) # event.latitude
        pieces[idx+1] = filt
    ds = pd.DataFrame(pd.concat(pieces))
    ds.drop_duplicates(subset='id',inplace=True)

    # for Ian to change on his end
    ds.loc[ds['price'] == "", 'price'] = "0"


    """ PRE-PROCESSING FOR K-MEANS CLUSTERING DATAFRAME"""
    #kmeans_data = preProcessKmeans(ds)
    #print(kmeans_data)

    #means_recs = {}
    #for a in range(0,num_past_user_events):
        #kmeans_data = pd.DataFrame(np.array([[userEvents.loc[a]['id'], userEvents.loc[a]['title'], userEvents.loc[a]['description']]]), columns=['id', 'title', 'description']).append(kmeans_data, ignore_index=True)

    # could try to get rid of distance and just try to do kmeans per past event, per city
    # add all past events to kmeans data originally
    # do kmeans for each past location (up to 3), clusters based on categories and other
    # end up with 3 sets, one per city

    """ APPLY KMEANS ON PRE-PROCESSED DATAFRAME """
    #generateKmeansRecommendations(kmeans_data)


    """ PRE-PROCESSING FOR NLP DATAFRAME"""
    nlp_data = preProcessNLP(ds)
    #print(nlp_data)

    """ APPLY NLP ON PRE-PROCESSED DATAFRAME """
    #nlp_recommendations = {}

    # add event to nlp_data
    frames = {}
    for a in range(0,num_past_user_events):
        newset = pd.DataFrame(np.array([[userEvents.loc[a]['id'], userEvents.loc[a]['title'], userEvents.loc[a]['description']]]), columns=['id', 'title', 'description']).append(nlp_data, ignore_index=True)
        #nlp_recommendations[a] = generateNLPRecommendations(newset,a,num_past_user_events)
        frames[a] = generateNLPRecommendations(newset,a,num_past_user_events)

    # generate recommendations
    result = pd.concat(frames)
    result = pd.DataFrame(result)
    #result.groupby('id')['weight'].sum()
    #result.groupby('weight').sum()

    #result = result['id'].groupby(result['weight']).sum()
    print(result.tail(100))


def preProcessKmeans(df):

    tmp = df.copy()

    # make all category labels lowercase due to overlap between ticketmaster and universe
    tmp['category'] = tmp['category'].str.lower()

    # apply one hot encoding to category column, get rid of original column and join new columns to df
    one_hot = pd.get_dummies(tmp['category'])
    del tmp['category']
    tmp = tmp.join(one_hot)

    # re-calculate distance
    tmp['distance'] = tmp.apply(lambda row: latLongToDistance(user_lat, user_long, row['latitude'], row['longitude']), axis=1)

    # drop some columns
    #ds = tmp[['price','start_time','distance','arts & theatre','business','comedy','crafts','fashion','music','other','performing arts','social','sports','tech','hourOfDay','dayOfWeek','dayOfYear','daysUntilEvent']]
    ds = tmp.drop(['latitude','longitude','description','id','event_end_time','genre','subGenre','city','country','status','api', 'title'], axis=1)

    # derive other attributes based on start_time
    ds['hourOfDay'] = ds['start_time'].dt.hour
    ds['dayOfWeek'] = ds['start_time'].dt.dayofweek
    ds['dayOfYear'] = ds['start_time'].dt.dayofyear
    #ds['year'] = ds['start_time'].dt.year
    ds['daysUntilEvent'] = (ds['start_time'] - pd.datetime.now().date())
    ds['daysUntilEvent'] = ds['daysUntilEvent'].dt.total_seconds() / 86400 # in days

    # filter out more
    ds = ds[ds.daysUntilEvent <= 60]

    # now apply standardization to distance and dayUntilEvent, dayOfWeek, dayOfYear, hourOfDay columns
    ds['price'] = preprocessing.scale(ds['price'])
    ds['hourOfDay'] = preprocessing.scale(ds['hourOfDay'])
    ds['dayOfWeek'] = preprocessing.scale(ds['dayOfWeek'])
    ds['dayOfYear'] = preprocessing.scale(ds['dayOfYear'])
    ds['daysUntilEvent'] = preprocessing.scale(ds['daysUntilEvent'])
    min_max_scaler = preprocessing.MinMaxScaler()
    ds['distance'] = min_max_scaler.fit_transform(ds['distance'])

    return ds._get_numeric_data()


def filterLocations(ds, lat, long):

    df = ds.copy()
    df['distance'] = df.apply(lambda row: latLongToDistance(lat, long, row['latitude'], row['longitude']), axis=1)
    filt = df.loc[(df.loc[:,('distance')] <= 500)]
    return filt


def latLongToDistance(lat1, long1, lat2, long2):
    #return math.sqrt(math.pow(row['latitude']-lat,2) + math.pow(row['longitude']-long, 2))
    return vincenty((lat1, long1), (lat2, long2)).km


def preProcessNLP(df):

    # if ticketmaster event, add genre and sub-genre to description then remove those columns from df
    df.loc[df['api'] == "ticketmaster", 'description'] = df['description'].str.cat([df['genre'], df['subGenre']], sep=' ')

    # only select specific columns from original dataframe
    ds = df.filter(['id', 'title', 'description'], axis=1)

    return ds


def generateKmeansRecommendations(ds):

    """ K-MEANS """
    #kmeans_model = KMeans(n_clusters=(3*6), random_state=1)
    k_means = KMeans(init='k-means++', n_clusters=3, n_init=10)
    k_means.fit(ds)
    labels = k_means.labels_

    """ MINI BATCH """
    batch_size = 50
    clusters_num = 3
    mbk = MiniBatchKMeans(init='k-means++', n_clusters=clusters_num, batch_size=batch_size, n_init=10, max_no_improvement=10, verbose=0)
    mbk.fit(ds)
    labels2 = mbk.labels_

    """ NOW TRY TO GRAPH EVERYTHING """
    df = ds.copy()
    df['Cluster Class'] = pd.Series(labels, index=df.index)
    #print(df)

    # Create a PCA model
    pca_2 = PCA(2)
    # Fit the PCA model on the numeric columns from earlier.
    plot_columns = pca_2.fit_transform(ds)
    # Make a scatter plot of each game, shaded according to cluster assignment.
    plt.scatter(x=plot_columns[:,0], y=plot_columns[:,1], c=labels)
    # Show the plot.
    #plt.show()

    """ TRY ELBOW TESTING METHOD """
    clusters=range(1,clusters_num)
    clus_train = ds.copy()
    meandist=[]
    for k in clusters:
        #model=KMeans(n_clusters=k)
        model = MiniBatchKMeans(init='k-means++', n_clusters=k, batch_size=batch_size, n_init=10, max_no_improvement=10, verbose=0)
        model.fit(clus_train)
        #clusassign=model.predict(clus_train)
        meandist.append(sum(np.min(cdist(clus_train, model.cluster_centers_, 'euclidean'), axis=1))
        / clus_train.shape[0])

    """
    Plot average distance from observations from the cluster centroid
    to use the Elbow Method to identify number of clusters to choose
    """
    plt.plot(clusters, meandist)
    plt.xlabel('Number of clusters')
    plt.ylabel('Average distance')
    plt.title('Selecting k with the Elbow Method') # pick the fewest number of clusters that reduces the average distance
    #plt.show()


def generateNLPRecommendations(ds, rank, numEvents):

    """ DICTIONARIES """
    di = dict()
    #print(ds)

    # weighting to add
    if (numEvents > 1):
        weight = (rank/numEvents)*0.5
    else:
        weight = 0

    """ TF-IDF for TITLES/DESCRIPTION COMBO """
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(ds['title']+ " " + ds['description'])
    cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)


    """ ITERATE THROUGH PANDAS DATAFRAME """
    d = []
    df = pd.DataFrame

    for idx, row in ds.iterrows():
        similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
        similar_items = [(cosine_similarities[idx][i], ds['title'][i]) for i in similar_indices]
        things = [{'id': ds['id'][i],'title': ds['title'][i], 'weight': cosine_similarities[idx][i]+weight, 'rank': rank } for i in similar_indices]
        things = things[1:]
        df = pd.DataFrame(things)
        title = similar_items[0][1]
        d = similar_items[1:]
        di[title] = similar_items[1:]
        break

    return df
    #for key, value in di.items():
    #    print(key, value)

    #print("--------------")


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


if __name__ == "__main__":
    main()

