import requests
import base64
import json
import time
import hashlib

CLIENT_ID = '980671eadd4943449af7aab8e91167ba'
CLIENT_SECRET = 'e8871d8ad26941f4920dd19dbdb079ba'

client_credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
client_credentials_b64 = base64.b64encode(client_credentials.encode('utf-8')).decode("utf-8")

token_url = "https://accounts.spotify.com/api/token"
headers = {
    "Authorization": f"Basic {client_credentials_b64}"
}

data = {
    "grant_type": "client_credentials"
}


response = requests.post(token_url, headers=headers, data=data)
response_data = response.json()

access_token = response_data["access_token"]
print(f"Access Token: {access_token}")

with open('/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/mod_slice.0-000.json', 'r') as file:
    data = json.load(file)


try:
    with open('last_failed_playlist.json', 'r') as f:
        last_failed_playlist = json.load(f)["last_failed"]
except FileNotFoundError:
    last_failed_playlist = 0 

i = last_failed_playlist  
for playlist in data['playlists'][i:]: 
    playlist_id = f"f{playlist['name']},{playlist['duration_ms']}"
    playlist_id = hashlib.sha256(playlist_id.encode('utf-8')).hexdigest()
    playlist['id'] = playlist_id
    for track in playlist['tracks']:
        track_id = track["track_uri"].split(':')[-1]
        artist_id = track['artist_uri'].split(':')[-1]


        url = f"https://api.spotify.com/v1/artists/{artist_id}"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(url, headers=headers)
        
        genre = []
        if response.status_code == 200:
            artis_info = response.json()
            genre.append(artis_info['genres'])
        else:
            print(f"Failed to fetch data for artist {artist_id}. Status code: {response.status_code}")

            with open('last_failed_playlist.json', 'w') as f:
                json.dump({"last_failed": i}, f)
            exit()  
        track['genres'] = genre

        time.sleep(1)

        url = f"https://api.spotify.com/v1/tracks/{track_id}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            track_data = response.json()
            track['popularity'] = track_data['popularity']
            track['explicit'] = track_data['explicit']
        else:
            print(f"Failed to fetch data for track {track_id}. Status code: {response.status_code}")

            with open('last_failed_playlist.json', 'w') as f:
                json.dump({"last_failed": i}, f)
            exit()  

        time.sleep(3)
    
    print(f'Completed processing playlist {i+1}')
    with open(f'/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/Final_data/final_copy_{playlist_id}.json', 'w') as f:
        json.dump(playlist, f, indent=2)
    i += 1

import os
if os.path.exists('last_failed_playlist.json'):
    os.remove('last_failed_playlist.json')