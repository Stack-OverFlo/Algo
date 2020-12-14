import pandas as pd
import numpy as np

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

print("columns of the dataset:\n", dataframe.columns)
