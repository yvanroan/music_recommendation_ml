from recommendation import drop_duplicates
from recommendation import select_cols
from recommendation import create_feature_set
from recommendation import generate_playlist_feature
from recommendation import generate_playlist_recos
from conversion import process_mpd
from get_songs import get_songdf

def run():
    print("lotf")
    playlist_link=input("Enter the link of the playlist:\n")
    
    playlistDF= get_songdf(playlist_link)
    
    songDF = drop_duplicates(playlistDF)
    
    songDF = select_cols(songDF)
    floats = [col for col, dtype in songDF.dtypes.items() if dtype == 'float']
    
    songDF = create_feature_set(songDF,floats)
    path = "C:/Users/roany/OneDrive/Desktop/spotify_million_playlist_dataset/data"
    
    spotifyDF= process_mpd(path)
    
    vector_summary_playlist,songs_not_in_playlist= generate_playlist_feature(spotifyDF,songDF)
    
    result= generate_playlist_recos(spotifyDF,vector_summary_playlist,songs_not_in_playlist)
    result.to_excel('recommendationplaylist_df.xlsx')


if __name__== "__main__":
    run()
