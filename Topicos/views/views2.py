import json
import time
import os

directory_path = '/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/Data_updated_bpm_loudness'
view1_data = []
view2_data = []
order_playlists = []
i = 0

for filename in os.listdir(directory_path):
    if filename.endswith('.json'):
        filepath = os.path.join(directory_path,filename)

        with open(filepath,'r') as file:
            data = json.load(file)
            
            average_track_duration = data['duration_ms'] / data['num_tracks']

            #popularity
            popularity = 0
            popularity_known_tracks = data['num_tracks']
            
            #bpm
            bpm = 0
            bpm_known_tracks = data['num_tracks']
            
            # explicit
            explicit = 0
            explicit_known_tracks = data['num_tracks']
            
            #loudness
            loudness = 0
            loudness_known_tracks = data['num_tracks']

            for track in data['tracks']:
                
                # Popularity
                if track['popularity'] != 0 and track['popularity'] != None:
                    popularity += track['popularity']
                else:
                    popularity_known_tracks -= 1

                # Bpm
                if track['tempo'] != 0 and track['tempo'] != None:
                    bpm += track['tempo']
                else:
                    bpm_known_tracks -= 1
                
                # Explicit
                if track['explicit'] != None:
                    if track['explicit'] != False:
                        explicit += 1
                else:
                    explicit_known_tracks -= 1

                # Loudness
                if track['loudness'] != 0 and track['loudness'] != None:
                    loudness += track['loudness']
                else:
                    loudness_known_tracks -= 1
            
            if popularity_known_tracks!=0:
                popularity /= popularity_known_tracks
            
            if bpm_known_tracks !=0:
                bpm /= bpm_known_tracks
            
            if explicit_known_tracks !=0:
                explicit /= explicit_known_tracks
            
            if loudness_known_tracks !=0:
                loudness /= loudness_known_tracks

            view1 = [data['duration_ms'],data['num_tracks'],data['num_followers']]
            view2 = [popularity,bpm,explicit,loudness,average_track_duration]

            view1_data.append(view1)
            view2_data.append(view2)

            order_playlists.append(data['id'])

with open('view1.json', 'w') as f:
    json.dump(view1_data, f, indent=2)

with open('view2.json', 'w') as f:
    json.dump(view2_data, f, indent=2)
    
with open('order.json', 'w') as f:
    json.dump(order_playlists, f, indent=2)