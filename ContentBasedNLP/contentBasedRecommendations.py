import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


""" STOP-WORDS """
#bad_words = set(['ticket', 'tickets', 'event', 'events', 'time', 'door', 'entrance'])


""" DATA SOURCE """
ds = pd.read_json("coolUser.json")
# eventually add new column to dataframe with recommendations for each event , for now use dictionary

""" DICTIONARIES """
di = dict()


""" TF-IDF for TITLES/DESCRIPTION COMBO """
tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df=0, stop_words='english')
tfidf_matrix = tf.fit_transform(ds['title']+ " " + ds['description'])
cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)
#print(cosine_similarities_T)


""" ITERATE THOUGH PANDAS DATAFRAME """

for idx, row in ds.iterrows():
    similar_indices = cosine_similarities[idx].argsort()[:-100:-1]

    similar_items = [(cosine_similarities[idx][i], ds['title'][i]) for i in similar_indices]
    #print(similar_indices)
    #print(similar_items)
    title = similar_items[0][1]
    di[title] = similar_items[1:]


#print(diTitles['Techweek | Chicago 2015'])

for key, value in di.items():
    print(key, value)

print("--------------")







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


