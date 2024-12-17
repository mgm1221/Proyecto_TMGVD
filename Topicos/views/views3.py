import json
import time
import os

directory_path = '/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/Data_updated_bpm_loudness'

view1_data = []
view2_data = []
order_playlists = []

for filename in os.listdir(directory_path):
    if filename.endswith('.json'):
        filepath = os.path.join(directory_path, filename)
        with open(filepath, 'r') as file:
            data = json.load(file)

            average_track_duration = data['duration_ms'] / data['num_tracks']

            popularity = 0
            popularity_known_tracks = data['num_tracks']
            bpm = 0
            bpm_known_tracks = data['num_tracks']
            explicit = 0
            explicit_known_tracks = data['num_tracks']
            loudness = 0
            loudness_known_tracks = data['num_tracks']

            for track in data['tracks']:
                # Popularity
                if track['popularity'] != 0 and track['popularity'] is not None:
                    popularity += track['popularity']
                else:
                    popularity_known_tracks -= 1

                # Bpm
                tempo = track.get('tempo', 0)
                if tempo != 0 and tempo is not None:
                    bpm += tempo
                else:
                    bpm_known_tracks -= 1

                # Explicit
                if track['explicit'] is not None and track['explicit'] is not False:
                    explicit += 1
                else:
                    explicit_known_tracks -= 1

                # Loudness
                loud = track.get('loudness', 0)
                if loud != 0 and loud is not None:
                    loudness += track['loudness']
                else:
                    loudness_known_tracks -= 1


            if popularity_known_tracks != 0:
                popularity /= popularity_known_tracks
            if bpm_known_tracks != 0:
                bpm /= bpm_known_tracks
            if explicit_known_tracks != 0:
                explicit /= explicit_known_tracks
            if loudness_known_tracks != 0:
                loudness /= loudness_known_tracks

            normalized_popularity = popularity / 100 

            normalized_explicit = explicit 

            normalized_bpm = bpm / 300 if bpm is not None else 0

            normalized_loudness = (loudness + 100) / 200 if loudness is not None else 0

            normalized_avg_duration = average_track_duration / 600000 if average_track_duration is not None else 0

            view2_data.append([
                normalized_popularity,
                normalized_bpm,
                normalized_explicit,
                normalized_loudness,
                normalized_avg_duration
            ])
            
            view1 = [data['duration_ms']/(data['num_tracks']*420000), data['num_tracks']/200, data['num_followers']/50]
            view1_data.append(view1)

            order_playlists.append(data['id'])

print(len(view1_data))
with open('/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/views_info/view1.json', 'w') as f:
    json.dump(view1_data, f, indent=2)

with open('/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/views_info/view2.json', 'w') as f:
    json.dump(view2_data, f, indent=2)

with open('/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/views_info/order_multiview.json', 'w') as f:
    json.dump(order_playlists, f, indent=2)

print(f"Data has been written to view1.json, view2.json, and order.json")
