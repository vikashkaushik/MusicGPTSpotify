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

def getTopItems(**kwargs):
    if(not kwargs.get("time_range")):
        time_range = "medium_term"
    else:
        time_range = kwargs.get("time_range")
    
    if(not kwargs.get("limit")):
        limit = 5
    else:
        limit = kwargs.get("limit")
    
    type = kwargs.get("type")
    try:
        token_info = get_token()
    except:
        print("user not logged in")
        #redirect("/")
        return redirect(url_for('login', _external=False))
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    top_songs = []
    iteration = 0
    while True:
        if(type == "artists"):
            items = (sp.current_user_top_artists(limit, 0, time_range)['items'][iteration]['name'])
            iteration += 1
            top_songs.append(items)
            if(iteration >= limit):
                break
        elif(type == "songs"):
            print(sp.current_user_top_artists(limit, 0, time_range)['items'])

            items = (sp.current_user_top_tracks(limit, 0, time_range)['items'][iteration]['name'])
            iteration += 1
            top_songs.append(items)
            if(iteration >= limit):
                break
    return json.dumps(top_songs)

def getRecs(**kwargs):
    if(not kwargs.get("time_range")):
        time_range = "medium_term"
    else:
        time_range = kwargs.get("time_range")
    
    if(not kwargs.get("limit")):
        limit = 5
    else:
        limit = kwargs.get("limit")
    

    try:
        token_info = get_token()
    except:
        print("user not logged in")
        #redirect("/")
        return redirect(url_for('login', _external=False))
    
    sp = spotipy.Spotify(auth=token_info['access_token'])

    # seeds = []
    # iteration = 0
    # values = []
    # while True:
    #     if(type == "artists"):
    #         items = (sp.current_user_top_artists(limit, 0, time_range)['items'][iteration]['id'])
    #         iteration += 1
    #         seeds.append(items)
    #         if(iteration >= limit):
    #             values = sp.recommendations(seed_artists = seeds, limit=5)
    #             break
    #     elif(type == "songs"):
    #         items = (sp.current_user_top_tracks(limit, 0, time_range)['items'][iteration]['id'])
    #         print(sp.current_user_top_tracks(limit, 0, time_range)['items'][iteration]['name'])
    #         iteration += 1
    #         seeds.append(items)
    #         if(iteration >= limit):
    #             values = sp.recommendations(seed_tracks = seeds, limit=5)
    #             break
    recommendationsArray = []
    print(limit)
    top_artists = []
    top_tracks = []
    iteration = 0
    while True:
        top_artists.append(sp.current_user_top_artists(limit, 0, time_range)['items'][iteration]['id'])
        top_tracks.append(sp.current_user_top_tracks(limit, 0, time_range)['items'][iteration]['id'])
        iteration +=1
        if(iteration >= 2):
            break
    
    # top_artists = sp.current_user_top_artists(limit, 0, time_range)['items']
    # top_tracks = sp.current_user_top_tracks(limit, 0, time_range)['items']
    genre_ids = sp.recommendation_genre_seeds()
    
    items = sp.recommendations(
        seed_artists=top_artists,
        seed_genres=genre_ids,
        seed_tracks=top_tracks,
        limit=limit
    )
    

    count = 0
    while count < limit:
        recommendationsArray.append(items['tracks'][count]['name'])
        count += 1
    
    return json.dumps(recommendationsArray)



    
    # count = 0
    # res = []
    # while count < 5:
    #     print(values['tracks'][count]['name'] + "   HIIIHIHIHIH")
    #     res.append(values['tracks'][count]['name'])
    #     count += 1
    # print(res)
    # return json.dumps(res)

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
                    "time_range": {"type": "string", "enum": ["long_term", "medium_term", "short_term"], "defaultValue": "medium_term"},
                    "limit": {
                        "type": "integer",
                        "description": "The number of tracks the user wants to display",
                        "defaultValue": 20
                    }, 
                },
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
                        "description": "The number of tracks the user wants to display",
                        "defaultValue": 20
                    }
                }
            },

        },
        {
            "name": "getRecommendations",
            "description": "Gets recommendations for the user based on his top songs",
            "parameters": {
                "type": "object",
                "properties": {
                    
                    "time_range": {"type": "string", "enum": ["long_term", "medium_term", "short_term"], "defaultValue": "medium_term"},
                    "limit": {
                        "type": "integer",
                        "description": "The number of seed items the user wants to get recommendations based on"
                    },
                    "genres": {
                        "type": "string",
                        "description": "The genres that the user wants to get recommendations of"
                    }
                }
            }
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
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
            "getSavedTracks": getSavedTracks,
            "getRecommendations": getRecs
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





def getSavedTracks(**kwargs):

    if(not kwargs.get("limit")):
        limit = 5
    else:
        limit = kwargs.get("limit")
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
        items = (sp.current_user_saved_tracks(limit, 0)['items'][iteration]['track']['name'])
        iteration += 1
        all_songs.append(items)
        if(iteration >= limit): 
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
        client_id="04dd3a00e6a04c8ab85ca26fd6477f72",
          client_secret="2bbff5ae6b4a4d1a83144a4983a693d9",
            redirect_uri=url_for('redirectPage', _external=True),
              scope="user-library-read user-top-read"
    )
# # Create a playlist  
# playlist_name = "My new playlist"  
# sp.user_playlist_create("USERNAME", playlist_name)  
  
# #Add tracks to the playlist  
# track_ids = ['4uLU6hMCjMI75M1A2tKUQC', '1301WleyT98MSxVHPZCA6M']  
# sp.user_playlist_add_tracks("USERNAME", playlist_id, track_ids)  
  
# # Retrieve all the playlists of a user  
# playlists = sp.user_playlists("USERNAME")  