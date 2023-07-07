from flask import Flask, request, url_for, session, redirect, render_template
import spotipy  
from spotipy.oauth2 import SpotifyOAuth  
from spotipy import Spotify  
import time
import openai
import json

openai.api_key = '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'
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
    return render_template(("index.html"))      # hi

    # return redirect(url_for('getTracks', _external=True))

def getTopItems(type, time_range):
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        #redirect("/")
        return redirect(url_for('login', _external=False))
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    top_songs = {

        "song": "power by kanye"
    }
    return json.dumps(top_songs)


@app.route('/getMessage', methods = ['POST'])
def getMessage():
    print("HI")
    input = request.form.get("data")
    print("the input is" + input)
    messages = [{"role": "user", "content": input}]
    functions = [
        {
            "name": "getTopItems",
            "description": "Get user's top items",
            "parameters": {
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["artists", "songs"]
                    },
                    "time_range": {"type": "string", "enum": ["long_term", "medium_term", "short_term"]}
                    
                },
                "required": ["type"]
            },
        },
        {
            "name": "getSavedTracks",
            "description": "Get the user's current saved tracks",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "The number of tracks the user wants to display"
                    },
                    "offset": {
                        "type": "integer",
                        "nullable": "true",
                        "defaultValue": 0

                    }
                }
            },
            "required": ["limit"]

        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=[getTopItems,getSavedTracks],
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]
    # Step 2: check if GPT wanted to call a function

    if response_message.get("function_call"):
        print("hi")
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "getTopItems": getTopItems,
            "getSavedTracks": getSavedTracks
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        kwargs = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(
            **kwargs
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        print(second_response)
        return second_response["choices"][0]["message"]
    print(response_message)
    
    return response_message





def getSavedTracks(limit, offset):
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
        items = (sp.current_user_saved_tracks(limit, offset)['items'])
        iteration += 1
        all_songs += items
        if(len(items) < limit): 
            break
    return json.dumps(all_songs)
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