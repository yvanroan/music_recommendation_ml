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

playlist_tracks_id=[]
  
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


max_files = 5
cid= env['Client_id']
secret = env['Client_secret']
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# grant_type = 'client_credentials'

# # Make the POST request to the /api/token endpoint
# response = requests.post('https://accounts.spotify.com/api/token', auth=(cid, secret), data={'grant_type': grant_type})

# # Extract the access token from the response
# access_token = response.json()['access_token']

# headers = {
#     'Authorization': f'Bearer {access_token}'
# }


def process_mpd(path):
    count = 0
    filenames = os.listdir(path)
    for filename in sorted(filenames):
        if filename.startswith("mpd.slice.") and filename.endswith(".json"):
            fullpath = os.sep.join((path, filename))
            f = open(fullpath)
            js = f.read()
            f.close()
            mpd_slice = json.loads(js)
            for i in range(47):
                print(i)
                try:  
                    for track in mpd_slice["playlists"][i]["tracks"][:15]:
                    
                        track_id=track["track_uri"].split(":")[-1]
                        # response = requests.get(f'https://api.spotify.com/v1/tracks/{track_uri}', headers= headers)
                        # print(count,response)

                        # # Extract the track ID from the response
                        # track_id = response.json()['id']
                        # print(track_id)
                        
                        playlist_tracks_id.append(track_id)    

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
                    
                except Exception as e:
                        raise    
                    
                    #Popularity of the track
                    # track_pop.append(response.json()['popularity'])
                    # count+=1
                time.sleep(2)

            # count+=1   
            # print(count)
            # if count > max_files:
            break
    
    features = sp.audio_features(playlist_tracks_id) #this is where we get all the good stuff. energy, livenes, etc
    features_df = pd.DataFrame(data=features, columns=features[0].keys())
    features_df['track_name'] = track_name
    features_df['artist_name'] = artist_name
    features_df['album'] = album
    features_df['artist_pop'] = artist_pop
    features_df['genres']= artist_genres
    # features_df['track_pop'] = track_pop
    features_df = features_df[['id', 'track_name', 'artist_name','album', 'genres',
                                'danceability', 'energy', 'key','speechiness', 
                                'loudness', 'acousticness', 'instrumentalness',
                                'mode', 'liveness', 'valence', 'tempo',
                                'duration_ms', 'time_signature']]

            
        
    features_df.to_excel('spotifympd_df.xlsx')
            
    return features_df



# if __name__ == "__main__":
#     path = "C:/Users/roany/OneDrive/Desktop/spotify_million_playlist_dataset/data"
#     # if len(sys.argv) > 2 and sys.argv[2] == "--quick":
#     #     quick = True
#     process_mpd(path)
