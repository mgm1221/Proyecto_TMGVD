import time
import psutil
import os
import numpy as np
import json
from mvlearn.cluster import MultiviewKMeans
from sklearn.metrics import silhouette_score

start_batch = 0
batch_size = 1500

with open('/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/views_info/view1.json','r') as file:
    data_view1 = json.load(file)

with open('/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/views_info/view2.json','r') as file:
    data_view2 = json.load(file)

view1 =data_view1[start_batch:start_batch+batch_size]
view2 =data_view2[start_batch:start_batch+batch_size]

multi_view_data = [np.array(view1),np.array(view2)]

# informacion de proceso
process = psutil.Process(os.getpid())
start = time.time()
initial_memory = process.memory_info().rss 

model = MultiviewKMeans(n_clusters=11, random_state=42)
labels = model.fit_predict(multi_view_data)

# memoria final
final_memory = process.memory_info().rss
end = time.time() - start
memory_used = final_memory - initial_memory

np_array = np.array(labels)
np_array =np_array.tolist()
score1 = silhouette_score(view1,labels)
score2 = silhouette_score(view2,labels)
score = (score1+score2)/2
with open(f'/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/labels/kmeans_multi_view_batch_{start_batch}.json','w') as file:
    json.dump(np_array,file,indent=1)

print(f"Memory used: {memory_used / (1024 ** 2):.2f} MB")
print(f"time: {end}")
print(f'score: {score}')