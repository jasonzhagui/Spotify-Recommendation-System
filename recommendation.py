import pandas as pd
import numpy as np
import spotipy
from sklearn.cluster import KMeans
from spotipy.oauth2 import SpotifyOAuth
from sklearn.preprocessing import MinMaxScaler

#Allows to access spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="7dbc3e0b536a4dc8aff8f0e09a6a2014",
                                               client_secret="c3c5287f124d4621ae3383a3c307fad7",
                                               redirect_uri="https://www.google.com/",
                                               scope="user-library-read playlist-modify-public"))


def recommendation():

    songs = []
    df = pd.read_csv("newDataset.csv")

    #slices the dataset with the values we want to use kmeans on
    x = df.iloc[:, [1,2,3,4,5]].values

    #scale all values from 0-1
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(x)

    kmeans = KMeans(n_clusters = 10)
    y_kmeans = kmeans.fit_predict(scaled)

    #converts the clusters into a dataframe
    kmeans_new = pd.DataFrame(data= y_kmeans, dtype=int)
    kmeans_new.columns = ['k_cluster']

    #adds the clusters to the og dataset
    df_cluster = pd.concat([df, kmeans_new], axis=1)

    #Asks user for song link and grabs the URI
    userInput = raw_input("Enter Song Link: ")
    userInput = userInput.split("?", 1)
    userInput = userInput[0].split("track/", 1)
    userInput = userInput[1]
    songs.append(userInput)

    #looks for the uri in the database
    index = df_cluster.index[df_cluster.uri == userInput][0]

    #gets attributes of song
    energy = float(df_cluster.iloc[index][1])
    tempo = float(df_cluster.iloc[index][2])
    danceability = float(df_cluster.iloc[index][3])
    valence = float(df_cluster.iloc[index][4])
    key = float(df_cluster.iloc[index][5])
    cluster = int(df_cluster.iloc[index][13]) 

    #creates dataframe cluster song is located in
    df3 = df_cluster[(df_cluster['k_cluster'] == cluster)]

    #point a for euclidean distance
    point_a = np.array((energy,tempo,danceability, valence, key))

    #recommends 10 songs
    for i in range(1, 11):
        song = findSongs(userInput, df3, songs, point_a)
        songs.append(song)

    #information to create playlist
    userInputName = raw_input("Enter username: ")
    userInput = raw_input("Enter Playlist Name: ")
    
    #creates playlist
    playlist = sp.user_playlist_create(user = userInputName, name = userInput)
    sp.user_playlist_add_tracks(user = userInputName, playlist_id = playlist["uri"].encode('utf-8'), tracks = songs )

#find lowest distance to song
def findSongs(uri, data, lst, point_a):
  min = 999999999999999999999999
  for index, row in data.iterrows():
    if row['uri'] != uri and row['uri'] not in lst:
      point_b = np.array((row['energy'],row['tempo'],row['danceability'],row['key'],row['valence']))
      distance = np.linalg.norm(point_a - point_b)
      if distance<min:
        min = distance
        uri = row['uri']
  return uri

recommendation()