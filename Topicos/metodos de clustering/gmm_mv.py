import time
import psutil
import os
import numpy as np
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score
import json
start_batch = 0
batch_size = 1500
num_clusters = 11
view1_value = 0.3
view2_value = 0.7

# data
with open('/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/views_info/view1.json','r') as file:
    data_view1 = json.load(file)

with open('/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/views_info/view2.json','r') as file:
    data_view2 = json.load(file)

view1 = data_view1[start_batch:start_batch+batch_size]
view2 = data_view2[start_batch:start_batch+batch_size]

# informacion de proceso
process = psutil.Process(os.getpid())
start = time.time()
initial_memory = process.memory_info().rss 

# Modelo para view 1 y clustering
gmm1 = GaussianMixture(n_components=num_clusters, random_state=42)
gmm_model_1 = gmm1.fit(view1)
label_gmm_1 = gmm_model_1.predict_proba(view1)

# Modelo para view 2 y clustering
gmm2 = GaussianMixture(n_components=num_clusters, random_state=42)
gmm_model_2 = gmm1.fit(view2)
label_gmm_2 = gmm_model_2.predict_proba(view2)

# Promedio de labels
combined_prob = (label_gmm_1 * view1_value) + (label_gmm_2 * view2_value)
consensus_labels = np.argmax(combined_prob, axis=1)

# memoria final y tiempo
final_memory = process.memory_info().rss
end = time.time() - start
memory_used = final_memory - initial_memory

# pasar a np array para medir silhouette
np_array = np.array(consensus_labels)
np_array =np_array.tolist()

# silhouette 
score1 = silhouette_score(view1,consensus_labels)
score2 = silhouette_score(view2,consensus_labels)
score = (score1+score2)/2

with open(f'/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/labels/gmm_multi_view_batch_{start_batch}.json','w') as file:
    json.dump(np_array,file,indent=1)

print(f"Memory used: {memory_used / (1024 ** 2):.2f} MB")
print(f"time: {end}")
print(f'score: {score}')

