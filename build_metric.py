import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import re
import time
import networkx as nx
import math
from graphviz import Graph

# Load the data to a pandas dataframe
dataframe = pd.read_csv("data.csv")
dataframe = dataframe.head(100)

# get the number of movies
nb_movies = len(dataframe)
print("Number of movies:", nb_movies)

print(dataframe.head())

# number of rows with holes
# print(dataframe.isna().sum())

# delete columns with holes + not revelant values
dataframe.drop(['director', 'cast', 'rating', 'date_added', 'listed_in'], axis=1, inplace=True)

# fill missing values for country
dataframe['country'].fillna(dataframe['country'].mode()[0], inplace=True)

# check duplicate and drop them
dataframe[dataframe.duplicated()]
dataframe.drop_duplicates(inplace=True)

# convert to date time
dataframe['release_year'] = pd.to_datetime(dataframe['release_year'])
# convert to Epoch
dataframe['release_year'] = (dataframe['release_year'] - dt.datetime(1970, 1, 1)).dt.total_seconds()
print("columns of the dataset:\n", dataframe.columns)

print(dataframe['show_id'].loc[0])
movie_1_release_year = dataframe.loc[0][4]
print(movie_1_release_year)


#print(dataframe.dtypes)

def compute_dissimilarity(movie_1_id, movie_2_id):
    """
        Compute  dissimilarity betwwen two movies
        based on their id.
    """
    movie_1_release_year = dataframe.loc[movie_1_id][4]
    movie_2_release_year = dataframe.loc[movie_2_id][4]

    # movie_1_duration = dataframe.loc[movie_1_id][5]
    # movie_2_duration = dataframe.loc[movie_2_id][5]

    movie_1_country = dataframe.loc[movie_1_id][3]
    movie_2_country = dataframe.loc[movie_2_id][3]

    if movie_1_country == movie_2_country:
        dissimilarity_country = 0
    else:
        dissimilarity_country = 1

    # we build a hybrid dissimilarity
    dissimilarity = math.sqrt(
        (movie_1_release_year-movie_2_release_year)**2+dissimilarity_country)

    # # plot 
    # x = dataframe['release_year']
    # y = dataframe['release_year']
    # # plot x and y
    # plt.scatter(x, y)
    # plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.show()

    print("----")
    movie_1_name = dataframe.loc[movie_1_id]["title"]
    movie_2_name = dataframe.loc[movie_2_id]["title"]
    print(f"movie 1 {movie_1_name}, movie 2 {movie_2_name}, dissimilarity: {dissimilarity}")
    return dissimilarity

# build a dissimilarity matrix
dissimilarity_matrix = np.zeros((nb_movies, nb_movies))
print("compute dissimilarities")
for movie_1_id in range(nb_movies):
    for movie_2_id in range(movie_1_id + 1, nb_movies):
        dissimilarity = compute_dissimilarity(movie_1_id, movie_2_id)
        dissimilarity_matrix[movie_1_id, movie_2_id] = dissimilarity

print("dissimilarity matrix")
print(dissimilarity_matrix)

threshold = 15
# build a graph from the dissimilarity
dot = Graph(comment='Graph created from complex data',
            strict=True)
for movie_id in range(nb_movies):
    movie_name = dataframe.loc[movie_id][1]
    dot.node(movie_name)

for movie_1_id in range(nb_movies):
    for movie_2_id in range(nb_movies):
        # no self loops
        if not movie_1_id == movie_2_id:
            movie_1_name = dataframe.loc[movie_1_id][0]
            movie_2_name = dataframe.loc[movie_2_id][0]
            # use the threshold condition 
            if dissimilarity_matrix[movie_1_id, movie_2_id] > threshold:
                dot.edge(movie_1_name,
                         movie_2_name,
                         color='darkolivegreen4',
                         penwidth='1.1')

# visualize the graph
dot.attr(label=f"threshold {threshold}", fontsize='20')
graph_name = f"images/complex_data_threshold_{threshold}"
dot.render(graph_name)