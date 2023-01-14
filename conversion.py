"""
    inspired by stats.py, 
"""
import json
import time
import requests
import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
from os import environ as env
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

playlist_track_ids=[]
  
#Track name
track_name = []        
       
#Name, popularity, genre
artist_name = []
artist_pop = []
artist_genres = []

#Album
album=[]
      
#Popularity of the track
track_pop=[]


# max_files = 5
cid= env['Client_id']
secret = env['Client_secret']
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)


batch_size = 50

grant_type = 'client_credentials'

response = requests.post('https://accounts.spotify.com/api/token', auth=(cid, secret), data={'grant_type': grant_type})

# Extract the access token from the response
access_token = response.json()['access_token']

headers = {
    'Authorization': f'Bearer {access_token}'
}


def process_mpd(path):
    count = 0
    
    fullpath = os.sep.join((path, 'dataset.json'))
    f = open(fullpath)
    js = f.read()
    f.close()
    mpd_slice = json.loads(js)
    for i in range(10):
        print(i)  
        for track in mpd_slice["playlists"][i]["tracks"][:50]:
                    
            track_uri= track["track_uri"]
            response = requests.get(f'https://api.spotify.com/v1/tracks/{track_uri}', headers= headers)
                        # print(count,response)

                        # # Extract the track ID from the response
                        # track_id = response.json()['id']
                        # print(track_id)
                        
            playlist_track_ids.append(track["track_uri"].split(":")[-1])    

                            #Track name
            track_name.append(track["track_name"])
            print(track["track_name"])
                            
                            #Main Artist
            artist_uri=track["artist_uri"]
            artist_info=sp.artist(artist_uri)
                            
                            #Name, popularity, genre
            artist_name.append(track["artist_name"])
            artist_pop.append(artist_info["popularity"])
            artist_genres.append(artist_info["genres"])
                            
                            #Album
            album.append(track["album_name"])

                    #Popularity of the track
            track_pop.append(response.json()['popularity'])
                    
    
    features = sp.audio_features(playlist_track_ids) #this is where we get all the good stuff. energy, livenes, etc
    features_df = pd.DataFrame(data=features, columns=features[0].keys())
    features_df['track_name'] = track_name
    features_df['artist_name'] = artist_name
    features_df['album'] = album
    features_df['artist_pop'] = artist_pop
    features_df['genres']= artist_genres
    # features_df['track_pop'] = track_pop
    features_df = features_df[['id', 'track_name', 'artist_name','album', 'artist_pop','genres',
                                'danceability', 'energy', 'key','speechiness', 
                                'loudness', 'acousticness', 'instrumentalness',
                                'mode', 'liveness', 'valence', 'tempo',
                                'duration_ms', 'time_signature']]

            
        
    features_df.to_excel('spotifympd_df.xlsx')
            
    return features_df
