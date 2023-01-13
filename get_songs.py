#helpful websites
# https://towardsdatascience.com/extracting-song-data-from-the-spotify-api-using-python-b1e79388d50

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from os import environ as env
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

def get_songdf(playlist_link:str):
    '''
    get songs from the playlist and put them all into a pandas dataframe
    '''
    #Authentication - without user

    cid= env['Client_id']
    secret = env['Client_secret']
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

    # playlist_link = "https://open.spotify.com/playlist/16Qqul4nLbfLf45Zosgp3s" #"https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"

    playlist_URI = playlist_link.split("/")[-1].split("?")[0]
    track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

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
    print("lotf")
    for track in sp.playlist_tracks(playlist_URI)["items"]:
        #URI
        # track_uri.append(track["track"]["uri"])
        
        playlist_tracks_id.append(track["track"]["id"])    
        
        #Track name
        track_name.append(track["track"]["name"])
        print(track["track"]["name"])
        #Main Artist
        artist_uri=track["track"]["album"]["artists"][0]["uri"]
        artist_info=sp.artist(artist_uri)
        
        #Name, popularity, genre
        artist_name.append(track["track"]["artists"][0]["name"])
        artist_pop.append(artist_info["popularity"])
        artist_genres.append(artist_info["genres"])
        
        #Album
        album.append(track["track"]["album"]["name"])
        
        #Popularity of the track
        track_pop.append(track["track"]["popularity"])

 #create a dataframe
    features = sp.audio_features(playlist_tracks_id) #this is where we get all the good stuff. energy, livenes, etc
    features_df = pd.DataFrame(data=features, columns=features[0].keys())
    features_df['track_name'] = track_name
    features_df['artist_name'] = artist_name
    features_df['album'] = album
    features_df['artist_pop'] = artist_pop
    features_df['genres']= artist_genres
    features_df['track_pop'] = track_pop
    features_df = features_df[['id', 'track_name', 'artist_name','album', 'artist_pop', 'genres',
                                'track_pop', 'danceability', 'energy', 'key','speechiness', 
                                'loudness', 'acousticness', 'instrumentalness',
                                'mode', 'liveness', 'valence', 'tempo',
                                'duration_ms', 'time_signature']]

    
    features_df.to_excel('features_df.xlsx')
    print("kaizoku oni, Yvan")
    return features_df

# if __name__== "__main__":
#     get_songdf("https://open.spotify.com/playlist/6wdWqBYFdavB5V8A3HQwf5")