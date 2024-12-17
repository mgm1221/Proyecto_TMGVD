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
    last_failed_playlist = 141 

iterator = last_failed_playlist  
for playlist in data['playlists'][iterator:]:  
    playlist_id = f"f{playlist['name']},{playlist['duration_ms']}"
    playlist_id = hashlib.sha256(playlist_id.encode('utf-8')).hexdigest()
    playlist['id'] = playlist_id
    contador = 0
    max_batch = 10
    first_update = 0
    while contador < playlist['num_tracks']:
        first_update = contador
        colect_artist_id=[]
        colect_track_id=[]
        for i in range(max_batch):
            if contador >= playlist['num_tracks']:
                break
            artist_id = playlist['tracks'][contador]['artist_uri'].split(':')[-1]
            track_id = playlist['tracks'][contador]['track_uri'].split(':')[-1]
            colect_artist_id.append(artist_id)
            colect_track_id.append(track_id)
            contador +=1
        every_artist_id = ",".join(colect_artist_id)
        url = f"https://api.spotify.com/v1/artists?ids={every_artist_id}"
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            artists_info = response.json()

            j = 0
            for i in range(first_update,contador):
                playlist['tracks'][i]['genre'] = artists_info['artists'][j]['genres']
                j += 1

        else:
            print(f"Failed to fetch data for artist {artist_id}. Status code: {response.status_code}")

            with open('last_failed_playlist.json', 'w') as f:
                json.dump({"last_failed": iterator}, f)
            exit() 
        time.sleep(0.75)
        every_track_id = ",".join(colect_track_id)
        
        url = f"https://api.spotify.com/v1/tracks?ids={every_track_id}"
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            tracks_data = response.json()
          
            j = 0
            for i in range(first_update,contador):
                playlist['tracks'][i]['popularity'] = tracks_data['tracks'][j]['popularity']
                playlist['tracks'][i]['explicit'] = tracks_data['tracks'][j]['explicit']
                j += 1
        else:
            print(f"Failed to fetch data for track {track_id}. Status code: {response.status_code}")
            
            with open('last_failed_playlist.json', 'w') as f:
                json.dump({"last_failed": iterator}, f)
            exit() 
        time.sleep(1.5)

    print(f'Completed processing playlist {iterator+1}')
    with open(f'/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/Final_data/final_copy_{playlist_id}.json', 'w') as f:
        json.dump(playlist, f, indent=2)
    iterator += 1

import os
if os.path.exists('last_failed_playlist.json'):
    os.remove('last_failed_playlist.json')