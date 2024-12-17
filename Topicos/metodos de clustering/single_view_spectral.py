import numpy as np

from sklearn.cluster import SpectralClustering
from sklearn.metrics import silhouette_score
import json
start_batch = 0
batch_size = 1500
num_clusters = 11

with open('/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/views_info/singleview.json','r') as file:
    data = json.load(file)
   
view1 = data[start_batch:start_batch+batch_size]

spectral= SpectralClustering(n_components=num_clusters,affinity='nearest_neighbors',random_state=42)

labels = spectral.fit_predict(view1)
score = silhouette_score(view1, labels)
np_array = np.array(labels)
np_array =np_array.tolist()


with open(f'/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/labels/spectral_single_view_batch_{start_batch}.json','w') as file:
    json.dump(np_array,file,indent=1)

print(score)    