from flask import Flask, request, url_for, session, redirect, render_template
import spotipy  
from spotipy.oauth2 import SpotifyOAuth  
from spotipy import Spotify  
import time

app = Flask(__name__)

app.secret_key = "fdskjfdsnsdk"
app.config['SESSION_COOKIE_NAME'] = 'VK Cookie'
TOKEN_INFO = "token_info"

@app.route('/')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)

    session[TOKEN_INFO] = token_info
    return render_template(("index.html"))

    # return redirect(url_for('getTracks', _external=True))

@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        #redirect("/")
        return redirect(url_for('login', _external=False))
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    all_songs = []
    iteration = 0
    while True:
        items = (sp.current_user_saved_tracks(limit=50, offset=iteration*50)['items'])
        iteration += 1
        all_songs += items
        if(len(items) < 50): 
            break
    return str(len(all_songs))
    # return "Some Drake songs or something"
    


def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "exception"
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60
    if (is_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id="6ccc82325a60410c9d0bbc5a7014537e",
          client_secret="5cac035e1acb4ba4acc94f014ee768ad",
            redirect_uri=url_for('redirectPage', _external=True),
              scope="user-library-read"
    )
# # Create a playlist  
# playlist_name = "My new playlist"  
# sp.user_playlist_create("USERNAME", playlist_name)  
  
# #Add tracks to the playlist  
# track_ids = ['4uLU6hMCjMI75M1A2tKUQC', '1301WleyT98MSxVHPZCA6M']  
# sp.user_playlist_add_tracks("USERNAME", playlist_id, track_ids)  
  
# # Retrieve all the playlists of a user  
# playlists = sp.user_playlists("USERNAME")  