import spotipy  
from spotipy.oauth2 import SpotifyOAuth  
from spotipy import Spotify  
  
sp_oauth = SpotifyOAuth(client_id="6ccc82325a60410c9d0bbc5a7014537e", client_secret="5cac035e1acb4ba4acc94f014ee768ad", redirect_uri="http://localhost:8000", scope="user-soa-link")  
  
access_token = sp_oauth.get_access_token()  
refresh_token = sp_oauth.get_refresh_token()

sp = Spotify(auth_manager=sp_oauth)  
  
results = sp.search(q='track:dancing', type='track')   

track_id = '4uLU6hMCjMI75M1A2tKUQC'  
audio_features = sp.audio_features(track_id)

# # Create a playlist  
# playlist_name = "My new playlist"  
# sp.user_playlist_create("USERNAME", playlist_name)  
  
# #Add tracks to the playlist  
# track_ids = ['4uLU6hMCjMI75M1A2tKUQC', '1301WleyT98MSxVHPZCA6M']  
# sp.user_playlist_add_tracks("USERNAME", playlist_id, track_ids)  
  
# # Retrieve all the playlists of a user  
# playlists = sp.user_playlists("USERNAME")  