import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#Allows to access spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="7dbc3e0b536a4dc8aff8f0e09a6a2014",
                                               client_secret="c3c5287f124d4621ae3383a3c307fad7",
                                               redirect_uri="https://www.pornhub.com/",
                                               scope="user-library-read"))
#dictionary of songs containing its data
d = {
    'artist': [], 
    'album': [], 
    'track': [], 
    'id': [], 
    'energy': [], 
    'liveness': [], 
    'tempo': [], 
    'speechiness': [], 
    'acousticness': [], 
    'instrumentalness': [], 
    'time_signature': [], 
    'danceability': [], 
    'key': [], 
    'duration_ms': [], 
    'loudness':[], 
    'valence': []
}
#list of columns name to create datatset
columns = [
    'artist', 
    'album', 
    'track', 
    'id', 'energy', 
    'liveness', 
    'tempo', 
    'speechiness', 
    'acousticness', 
    'instrumentalness', 
    'time_signature', 
    'danceability', 
    'key', 
    'duration_ms', 
    'loudness', 
    'valence'
]
#Creates a database of current users liked songs 
def liked():
    #stores saved tracks into results
    results = sp.current_user_saved_tracks()
    #stores only items from results which contains song information
    tracks = results['items']
    #Spotify API allows max of 50 songs this allows to parse to next 50 and extends dict
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    #looks throught each track
    for item in tracks:
        if (item['track'] == None):
            break
        else:
            getSongData(d, item)

    getAudioFeatures(d)

    df = pd.DataFrame(d, columns = columns)

    df.to_csv('user_music.csv', index = False)

#Creates a database of a specific playlist
def playlist():
    #stores playlist into results (userID, playlistID)
    results = sp.user_playlist_tracks(1216147948,"6ozzmfu02Olw7puFBVwaAo")
    #stores only items from results which contains song information
    tracks = results['items']
    #Spotify API allows max of 50 songs this allows to parse to next 50 and extends dict
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    #looks throught each track
    for item in tracks:
        if (item['track'] == None):
            break
        else:
            getSongData(d, item)

    getAudioFeatures(d)

    df = pd.DataFrame(d, columns = columns)

    df.to_csv('user_music.csv', index = False)

def getSongData(dataset, item):
    dataset['track'].append((item['track']['name']).encode('utf-8'))
    dataset['id'].append((item['track']['id']).encode('utf-8'))
    dataset['artist'].append((item['track']['artists'][0]['name']).encode('utf-8'))
    dataset['album'].append((item['track']['album']['name']).encode('utf-8'))

    return dataset

def getAudioFeatures(dataset):
    for ids in dataset['id']:
        results = sp.audio_features(ids)
        d['energy'].append(results[0]["energy"])
        d['liveness'].append(results[0]["liveness"])
        d['tempo'].append(results[0]["tempo"])
        d['speechiness'].append(results[0]["speechiness"])
        d['acousticness'].append(results[0]["acousticness"])
        d['instrumentalness'].append(results[0]["instrumentalness"])
        d['time_signature'].append(results[0]["time_signature"])
        d['danceability'].append(results[0]["danceability"])
        d['key'].append(results[0]["key"])
        d['duration_ms'].append(results[0]["duration_ms"])
        d['loudness'].append(results[0]["loudness"])
        d['valence'].append(results[0]["valence"])
    
    return dataset


def search():
    d = {
    'artist': [], 
    'album': [], 
    'track': [], 
    'id': [], 
    'energy': [], 
    'liveness': [], 
    'tempo': [], 
    'speechiness': [], 
    'acousticness': [], 
    'instrumentalness': [], 
    'time_signature': [], 
    'danceability': [], 
    'key': [], 
    'duration_ms': [], 
    'loudness':[], 
    'valence': []
    }

    artists = ["Travis Scott", "Lil Uzi Vert", "Kanye West", "Katy Perry", "Bruno Mars"]

    for term in artists:
        results = sp.search(term,1, 0, "artist")
        artist_name = term #ARTIST NAME 
        uri = results['artists']['items'][0]['uri'].encode('utf-8')

        results = sp.artist_albums(uri,album_type = 'album', country='US', limit=1)
        albums = results['items']

        while results['next']:
            results = sp.next(results)
            albums.extend(results['items'])

        results = sp.artist_albums(uri,album_type = 'single', country='US', limit=1)
        singles = results['items']
        while results['next']:
            results = sp.next(results)
            singles.extend(results['items'])

        albums+=singles

        for album in albums:
            if (album['name'].encode('utf-8') not in d['album']):

                album_name = album['name'].encode('utf-8') #ALBUM NAME

                uri = album['uri'].encode('utf-8')
                results = sp.album_tracks(uri)
                tracks = results['items']

                for track in tracks:

                    song_name = track['name'].encode('utf-8') #SONG NAME
                    print(song_name)
                    track_uri = track['id'].encode('utf-8') #TRACK URI 
        
                    attributes = sp.audio_features(track_uri)
        
                    d['track'].append(song_name)
                    d['id'].append(track_uri.encode('utf-8'))
                    d['artist'].append(artist_name)
                    d['album'].append(album_name)
                    d['energy'].append(attributes[0]["energy"])
                    d['liveness'].append(attributes[0]["liveness"])
                    d['tempo'].append(attributes[0]["tempo"])
                    d['speechiness'].append(attributes[0]["speechiness"])
                    d['acousticness'].append(attributes[0]["acousticness"])
                    d['instrumentalness'].append(attributes[0]["instrumentalness"])
                    d['time_signature'].append(attributes[0]["time_signature"])
                    d['danceability'].append(attributes[0]["danceability"])
                    d['key'].append(attributes[0]["key"])
                    d['duration_ms'].append(attributes[0]["duration_ms"])
                    d['loudness'].append(attributes[0]["loudness"])
                    d['valence'].append(attributes[0]["valence"])


                
    df = pd.DataFrame(d, columns = columns)

    df.to_csv('dataset.csv', index = False)

search()