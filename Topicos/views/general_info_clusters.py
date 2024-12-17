import json
import os
from collections import Counter

directory_path = '/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/Data_updated_bpm_loudness'
final_data = []
order_playlists = []

genre_mapping = {
    'indie pop': 'pop',
    'electropop': 'pop',
    'alternative': 'pop',
    'pop': 'pop',
    'rock': 'rock',
    'metal': 'rock',
    'indie rock': 'rock',
    'classic rock': 'rock',
    'punk': 'rock',
    'hard rock': 'rock',
    'post-punk': 'rock',
    'grunge': 'rock',
    'hip-hop': 'hip-hop',
    'rap': 'hip-hop',
    'trap': 'hip-hop',
    'r&b': 'hip-hop',
    'electronic': 'electronic',
    'house': 'electronic',
    'techno': 'electronic',
    'trance': 'electronic',
    'dubstep': 'electronic',
    'ambient': 'electronic',
    'classical': 'classical',
    'jazz': 'jazz',
    'blues': 'jazz',
    'soul': 'hip-hop',  
    'funk': 'hip-hop',  
    'reggae': 'latino',  
    'latin': 'latino',  
    'world': 'world',
    'folk': 'pop',  
    'country': 'country',
    'bluegrass': 'country',
    'acoustic': 'pop',  
    'dance': 'electronic',
    'disco': 'electronic',  
    'ska': 'rock',
    'reggaeton': 'hip-hop',  
    'k-pop': 'pop',  
    'a cappella': 'pop',  
    'punk rock': 'rock',  
    'synthwave': 'electronic',  
    'chillwave': 'electronic',  
    'progressive rock': 'rock',
    'experimental': 'electronic',  
    'ambient': 'electronic',  
    'new age': 'classical',  
    'singer-songwriter': 'pop',  
    'disco': 'electronic',  
    'indie electronic': 'electronic', 
    'trap music': 'hip-hop',  
    'psytrance': 'electronic',  
    'dub': 'reggae', 
    'reggae fusion': 'reggae', 
    'vaporwave': 'electronic',  
    'lo-fi': 'electronic',  
    'metalcore': 'rock',   
    'post-rock': 'rock',   
    'hardstyle': 'electronic',   
    'dancehall': 'reggae',   
    'electropunk': 'electronic',   
    'future bass': 'electronic',   
    'neo-soul': 'hip-hop',   
    'darkwave': 'electronic',   
    'chillout': 'electronic',   
    'garage': 'electronic',   
    'deep house': 'electronic',   
    'dnb': 'electronic',   
    'afrobeat': 'world',   
    'zouk': 'world',   
    'soca': 'world',   
    'indie folk': 'pop',   
    'alt-country': 'country',   
    'swedish house': 'electronic',   
    'progressive trance': 'electronic',   
    'j-pop': 'pop',   
    'soulful house': 'electronic',   
    'new wave': 'rock',   
    'gothic rock': 'rock',   
    'alternative rock': 'rock',   
    'tropical house': 'electronic',   
    'future house': 'electronic',   
    'funk rock': 'rock',   
    'southern rock': 'rock',   
    'grime': 'hip-hop',   
    'trap soul': 'hip-hop',   
    'blues rock': 'rock',   
    'indie blues': 'blues',   
    'ska punk': 'rock',   
    'psychadelic rock': 'rock',   
    'latin jazz': 'jazz',   
    'reggae rock': 'rock',   
    'afrobeat': 'world'   
}
genre_to_power_map = {
    'hip-hop': 1,
    'country': 2,
    'world': 4,
    'reggae': 8,
    'blues': 16,
    'latino': 32,
    'pop': 64,
    'jazz': 128,
    'classical': 256,
    'rock': 512,
    'electronic': 1024
}

iterator =0

for filename in os.listdir(directory_path):

    if filename.endswith('.json'):
        filepath = os.path.join(directory_path, filename)

        with open(filepath, 'r') as file:
            data = json.load(file)
            order_playlists.append(data['id'])
            average_duration = data['duration_ms'] / data['num_tracks']
            num_tracks = data['num_tracks']
            num_followers = data['num_followers']
            all_genres = []

            
            for track in data['tracks']:
                genres_to_add = track.get('genre', [])
                if len(genres_to_add) ==0:
                    genres_to_add = track.get('genres', [])
               
                if genres_to_add != []:
                    if isinstance(genres_to_add[0], list):
                        genres_to_add = [genre for sublist in genres_to_add for genre in sublist]

                
                all_genres.extend(genres_to_add)

           
            simplified_genres = [genre_mapping.get(genre, None) for genre in all_genres]
            
            
            simplified_genres = [genre for genre in simplified_genres if genre is not None]
            
            genre_counts = Counter(simplified_genres)
            
            most_common_genre = genre_counts.most_common(3)
            final_text_genres =[]
            final_text_genres = [tuple[0] for tuple in most_common_genre]

            num_genres =[genre_to_power_map.get(genre,None) for genre in final_text_genres]
            final_genre = 0
            for genre_power in num_genres:
                if genre_power is not None:  
                    final_genre |= genre_power

            
            final_data.append([average_duration/420000, num_tracks/200, num_followers/50, final_genre/1792])


with open('/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/views_info/singleview.json', 'w') as f:
    json.dump(final_data,f,indent=2)

with open('/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/views_info/order_singleview.json', 'w') as f:
    json.dump(order_playlists,f,indent=2)