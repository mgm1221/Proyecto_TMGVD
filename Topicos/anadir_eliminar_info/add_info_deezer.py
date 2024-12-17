import requests
import json
import time
import os

directory_path = '/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/Final_data'

for filename in os.listdir(directory_path):
    if filename.endswith('.json'):
        file_path = os.path.join(directory_path, filename)
        
        with open(file_path, 'r') as file:
            data = json.load(file)

            for track in data['tracks']:
                artist = track['artist_name']
                song_name = track['track_name']
                url = f'https://api.deezer.com/search?q=artist:"{artist}" track:"{song_name}"'
                
                try:
                    response = requests.get(url)
                    
                    if response.status_code == 200:
                        data_response_1 = response.json()
                        if data_response_1['data']:
                            track_data = data_response_1['data'][0]
                            track_url = f'https://api.deezer.com/track/{track_data["id"]}'
                            
                            track_response = requests.get(track_url)
                            if track_response.status_code == 200:
                                track_info = track_response.json()
                                track['tempo'] = track_info.get('bpm', None)
                                track['loudness'] = track_info.get('gain', None)
                            else:
                                print(f'Failed request, status code {track_response.status_code}')
                                continue
                        else:
                            track['tempo'] = None
                            track['loudness'] = None
                    else:
                        print(f'Failed request, status code {response.status_code}')
                        continue  

                except requests.exceptions.RequestException as e:
                    print(f"Error fetching data for {song_name} by {artist}: {e}")
                    track['tempo'] = None
                    track['loudness'] = None

            
            time.sleep(0.35)

            print('playlist')
            try:
                with open(f'/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/Data_updated_bpm_loudness/updated_{filename}', 'w') as output_file:
                    json.dump(data, output_file, indent=2)
                os.remove(file_path)
            except Exception as e:
                print(f"Error processing {filename}: {e}")
