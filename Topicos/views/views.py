import json

with open('/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/mod_slice.0-000.json', 'r') as f:
    data = json.load(f)

#view 1
view1 = [data['id'],data['duration_ms'],data['num_tracks'],data['num_followers']]
# view 2
popularity = 0
explicit = 0
danceability =0
energy =0
loudness =0
sadness_happines = 0
# extrayendo los datos
for track in data['tracks']:
    popularity += track['popularity']
    if track['explicit'] ==True:
        explicit+=1
    danceability += track['danceability']
    energy += track['energy']
    loudness += track['loudness']
    sadness_happines += track['sadness_happines']

popularity /= data['num_tracks']*100
explicit /= data['num_tracks']
danceability /= data['num_tracks']
energy /= data['num_tracks']
loudness /=data['num_tracks']
sadness_happines /= data['num_tracks']

view2 = [data['id'], popularity,explicit,danceability,energy,loudness,sadness_happines]

with open('view1.json', 'w') as f:
    json.dump(view1, f, indent=2)


with open('view2.json', 'w') as f:
    json.dump(view2, f, indent=2)