import pandas as pd
import time
import matplotlib.pyplot as plt

""" PRE-PROCESSING EVENT DATA """

# load user history from another file
userEvents = pd.read_json("userEventsTest.json")

# load data from json file into pandas dataframe
ds = pd.read_json("vancouver400output.json", convert_dates=True)
print(ds)

# replace any instances of "none" with "other" for category column
ds.loc[ds['category'].isnull(), 'category'] = 'other' # IAN CHANGING ON HIS SIDE

# make all category labels lowercase due to overlap between ticketmaster and universe
ds['category'] = ds['category'].str.lower()


# apply one hot encoding to category column, get rid of original column and join new columns to df
#ds['category'] = LabelEncoder().fit_transform(ds['category'])
one_hot = pd.get_dummies(ds['category'])
ds = ds.drop('category', axis=1)
ds = ds.join(one_hot)

# if ticketmaster event, add genre and sub-genre to description then remove those columns from df
ds.loc[ds['genre'].isnull(), 'genre'] = "other" # IAN CHANGING ON HIS SIDE
ds.loc[ds['subGenre'].isnull(), 'subGenre'] = "other" # IAN CHANGING ON HIS SIDE
ds.loc[ds['api'] == "ticketmaster", 'description'] = ds['description'].str.cat([ds['genre'], ds['subGenre']], sep=' ')

# make duplicate of df - this is going to be modified and chopped further now (NOT for cosine similarity matrix)
df = ds.copy()

# drop some columns
df = df.drop(['description','id','event_end_time','genre','subGenre','city','country','status','api'], axis=1)

# find time to event by subtracting current unix time from "unix time" column
# derive other attributes based on unix time?
timestamp = int(time.time())
df['start_time'] = pd.to_numeric(df['start_time'])
df['start_time'] = (df['start_time'] - timestamp)/86400 # in days


# need to convert some ticketmaster locations to latitude and longitude


# print for debugging
print(df)



# pre-process event data to filter out location based on lat and long


good_columns = df._get_numeric_data()
#print(good_columns)


