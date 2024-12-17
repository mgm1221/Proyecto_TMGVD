import json

with open('/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/Data/Dataset/data/mpd.slice.4000-4999.json', 'r') as file:
    data = json.load(file)
informacion_a_borrar_playlist =["collaborative", "pid","modified_at","num_artists","num_edits"]
informacion_a_borrar_track = ["pos","duration_ms","album_name"]


for playlist in data['playlists']:
    for inf in informacion_a_borrar_playlist:
        if inf in playlist:
            del playlist[inf]
    for track in playlist['tracks']:
        for inf in informacion_a_borrar_track:
            if inf in track:
                del track[inf]

with open('/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/mod_slice.0-000.json', 'w') as f:
    json.dump(data,f,indent=2)

