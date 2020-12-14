import pandas as pd
import numpy as np

# Load the data to a pandas dataframe
dataframe = pd.read_csv("netflix_titles.csv")

nb_movies = len(dataframe)
print(dataframe.head())
print("Number of movies:", nb_movies)

print("df infos :", dataframe.info())

print("columns of the dataset", dataframe.columns)

print("correlation matrix", dataframe.corr())

print("standard deviation", dataframe.std())