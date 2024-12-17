import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score
import json

batch_size = 1500
num_clusters = 11

with open('/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/views_info/singleview.json','r') as file:
    data = json.load(file)
   
view1 = data[0:batch_size]

gmm= GaussianMixture(n_components=num_clusters,random_state=42)
gmm_model = gmm.fit(view1)

labels = gmm_model.predict(view1)
score = silhouette_score(view1, labels)

np_array = np.array(labels)
np_array =np_array.tolist()


with open('/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/labels/gmm_single_view.json','w') as file:
    json.dump(np_array,file,indent=1)

print(score)