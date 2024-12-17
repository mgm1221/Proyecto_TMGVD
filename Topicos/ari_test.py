import json
from sklearn.metrics import adjusted_rand_score

with open('/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/labels/spectral_multi_view_batch_0.json', 'r') as file:
    labels_1 = json.load(file)
with open('/Users/martingarces/Desktop/UdeC/2024-2/Topicos en manejos de grandes volumenes de datos/Proyecto_Semestral/labels/spectral_single_view_batch_0.json', 'r') as file:
    labels_2 = json.load(file)

ari_score = adjusted_rand_score(labels_1, labels_2)
print(f"ARI: {ari_score}")
