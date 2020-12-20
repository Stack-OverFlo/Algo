import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import datetime as dt
import re
import time
import networkx as nx
import math
from graphviz import Graph
import csv

# Load the data to a pandas dataframe
dataframe = pd.read_csv("netflix_titles.csv")

# get the number of movies
nb_movies = len(dataframe)
print("Number of movies:", nb_movies)

print(dataframe.head())

#print(dataframe.nunique())

# number of rows with holes
#print(dataframe.isna().sum())

# delete columns with holes + unused values
dataframe.drop(['director', 'cast', 'rating', 'date_added', 'listed_in'], axis=1, inplace=True)

# fill missing values for country
dataframe['country'].fillna(dataframe['country'].mode()[0], inplace=True)

dataframe.isna().sum()
# use show_id as index
#dataframe.set_index('show_id', inplace=True)

# check duplicate and drop them
dataframe[dataframe.duplicated()]
dataframe.drop_duplicates(inplace=True)

# convert to date time
dataframe['release_year'] = pd.to_datetime(dataframe['release_year'])
# convert to Epoch
dataframe['release_year'] = (dataframe['release_year'] - dt.datetime(1970, 1, 1)).dt.total_seconds()
print("columns of the dataset:\n", dataframe.columns)

#dataframe['duration'] = int(dataframe['duration'])

print(dataframe['show_id'].loc[0])
# release year in Epoch
movie_1_release_year = dataframe.loc[0][4]
print(movie_1_release_year)


def compute_dissimilarity(movie_1_id, movie_2_id):
    """
        Compute  dissimilarity betwwen two movies
        based on their id.

        The meal is not a quantitative attribute.
        It is called a categorical variable.
        We must handle it differently than quantitative
        attributes.
    """
    movie_1_release_year = dataframe.loc[movie_1_id][4]
    movie_2_release_year = dataframe.loc[movie_2_id][4]

    movie_1_duration = dataframe.loc[movie_1_id][5]
    movie_2_duration = dataframe.loc[movie_2_id][5]

    movie_1_country = dataframe.loc[movie_1_id][3]
    movie_2_country = dataframe.loc[movie_2_id][3]

    if movie_1_country == movie_2_country:
        dissimilarity_country = 0
    else:
        dissimilarity_country = 1

    # we build a hybrid dissimilarity
    dissimilarity = math.sqrt(
        (movie_1_release_year-movie_2_release_year)**2+dissimilarity_country)

#   dissimilarity = math.sqrt(
#        (movie_1_release_year-movie_2_release_year)**2+(movie_1_speed-movie_2_speed)**2+dissimilarity_country)

    #print("----")
    movie_1_name = dataframe.loc[movie_1_id]["title"]
    movie_2_name = dataframe.loc[movie_2_id]["title"]
    #print(f"movie 1 {movie_1_name}, movie 2 {movie_2_name}, kois {movie_1_release_year}, dissimilarity: {dissimilarity}")
    return dissimilarity

file = open("result.csv", "w", newline="\n")
writer = csv.writer(file)

movie_1_id = 0
movie_2_id = 0

while movie_1_id < nb_movies:
    cluster = []
    #print( "movie 1: " + dataframe.loc[movie_1_id]["title"])
    while movie_2_id < nb_movies:
        dissimilarity = compute_dissimilarity(movie_1_id, movie_2_id)
        #print(dissimilarity)
        if dissimilarity < .01 and dataframe.loc[movie_1_id]["title"] != dataframe.loc[movie_2_id]["title"]:
            #print(dissimilarity)
            cluster.append(dataframe.loc[movie_2_id]["title"].encode('utf-8'))
            dataframe.drop(movie_2_id, inplace= True)
            nb_movies = nb_movies - 1
            dataframe.reset_index(inplace = True, drop=True)
        else:
            movie_2_id = movie_2_id + 1
    if len(cluster) > 1:
        writer.writerow(cluster)
        print(len(cluster))
        dataframe.drop(movie_1_id, inplace = True)
        nb_movies = nb_movies - 1
        dataframe.reset_index(inplace = True, drop=True)
        print(nb_movies)
    else:
        movie_1_id = movie_1_id + 1