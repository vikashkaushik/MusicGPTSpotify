
import pandas as pd
import openai


categories = ['song_name', 'genre', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']

songData = pd.read_json('genres.json')
print(songData['danceability'][1])

labels = [songData[x].split('.')[-1] for x in songData['danceability']]
texts = [text.strip() for text in songData['energy']]
df = pd.DataFrame(zip(texts, labels), columns = ['prompt','completion']) #[:300]
df.head()