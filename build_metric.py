import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import datetime as dt
import re
# Load the data to a pandas dataframe
dataframe = pd.read_csv("netflix_titles.csv")

nb_movies = len(dataframe)
print(dataframe.head())
print("Number of movies:", nb_movies)

#print(dataframe.nunique())

# number of rows with holes
#print(dataframe.isna().sum())

# delete columns with holes + unused values
dataframe.drop(['director', 'cast', 'rating', 'date_added', 'listed_in'], axis=1, inplace=True)

# fill missing values for country
dataframe['country'].fillna(dataframe['country'].mode()[0], inplace=True)

dataframe.isna().sum()
# use show_id as index
dataframe.set_index('show_id', inplace=True)

# check duplicate and drop them
dataframe[dataframe.duplicated()]
dataframe.drop_duplicates(inplace=True)

dataframe["release_year"] = pd.to_datetime(dataframe['release_year'])
# convert to Epoch
# dataframe['release_year'] =int(dataframe['release_year'] / 1000000000) 
dataframe['release_year'] = (dataframe['release_year'] - dt.datetime(1970, 1, 1)).dt.total_seconds()
print(dataframe['release_year'])

print("columns of the dataset:\n", dataframe.columns)

df = dataframe
df.drop(['type', 'title', 'country', 'description'], axis=1, inplace=True)
#data = dict(Type=Type, Title=Title, Country=Country, Description=Description)

# type and country
x = dataframe['release_year']
y = dataframe['release_year']

 # plot x and y
plt.scatter(x, y)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
plt.xlabel('x')
plt.ylabel('y')
plt.show()