"""
This file will perform K-Mean: To create Tourist Clusters
"""

##### Importaciones
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np
import os
import matplotlib.pyplot as plt
#### KMeans
from sklearn.cluster import KMeans, MiniBatchKMeans, BisectingKMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.decomposition import PCA
from matplotlib.colors import ListedColormap, BoundaryNorm




###################################################
###### K Means

##### Importando datos
#### Cargando
df_1_original = pd.read_csv(f'{os.getcwd()}/Datos/FeatEng/visitantes_internacionales_original.csv')
df_1_encoded = pd.read_csv(f'{os.getcwd()}/Datos/FeatEng/visitantes_internacionales_encoded.csv')
#### Eliminando columnas no necesarias
# df_1_encoded = df_1_encoded.drop(columns=['NUMERO_VISITANTES'])
# df_1_encoded = df_1_encoded.drop(columns=['CONTINENTE'])

#### Renombrando Aeropuerto
#### Cambiando AIJC abbreviacion
tmp = df_1_original[df_1_original['OCM']=='AEROPUERTO INTERNACIONAL JORGE CHÁVEZ'].index
df_1_original.loc[tmp, 'OCM'] = 'AIJCH'
del tmp

##### Buscando optimo numero de clusters
    # Elbow metodo
#### Buscando inercias
inercias = []
for k in range(1,15):
    kmeans=KMeans(n_clusters=k, random_state=42)
    kmeans.fit(df_1_encoded)
    inercias.append(kmeans.inertia_)

#### Graficando inercias
fig = plt.figure(figsize=(8,5))
plt.plot(
    range(1,15),
    inercias,
    marker='o'
)
plt.show()

#### Eligiendo optimo numero de clusters
num_clus = 6


##### Haciendo los 3 diferentes KMeans
#### KMeans <-> 'CLUSTER_1'
m1 = KMeans(n_clusters=num_clus, random_state=42)
m1.fit(df_1_encoded)
df_1_original['CLUSTERS_KMEANS'] = m1.labels_

#### MiniBatchKMeans <-> 'CLUSER_2'
m2 = MiniBatchKMeans(n_clusters= num_clus, random_state=42)
m2.fit(df_1_encoded)
df_1_original['CLUSTERS_MINIBATCH'] = m2.labels_

#### BisectingKMeans <-> 'CLUSTER_3'
m3 = BisectingKMeans(n_clusters=num_clus, random_state=42)
m3.fit(df_1_encoded)
df_1_original['CLUSTERS_BISECTING'] = m3.labels_ 


##### Evaluacion de los 3 clustering algs
#### Correlacion
cluster_corr = df_1_original[['CLUSTERS_KMEANS','CLUSTERS_MINIBATCH','CLUSTERS_BISECTING']].corr()
    # Resultados: Ningun |valor| > 0.121
    # Ende: No hay correlacion entre los diferentes clusteres
#### Silhouette scores, mayor es mejor
m1_ss = silhouette_score(df_1_encoded, m1.labels_)
m2_ss = silhouette_score(df_1_encoded, m2.labels_)
m3_ss = silhouette_score(df_1_encoded, m3.labels_)
#### Davie-Bouldin, menor es mejor
m1_db = davies_bouldin_score(df_1_encoded, m1.labels_)
m2_db = davies_bouldin_score(df_1_encoded, m2.labels_)
m3_db = davies_bouldin_score(df_1_encoded, m3.labels_)
#### Creando DF de resultados
resultados={
    'corr_c1':cluster_corr['CLUSTERS_KMEANS'].values.tolist(),
    'corr_c2':cluster_corr['CLUSTERS_MINIBATCH'].values.tolist(),
    'corr_c3':cluster_corr['CLUSTERS_BISECTING'].values.tolist(),
    'silhouette': [m1_ss, m2_ss, m3_ss],
    'davies': [m1_db, m2_db, m3_db]
}
df_resultados = pd.DataFrame(resultados, index=['clusters_kmeans', 'clusters_minibatch', 'clusters_bisecting'])
df_resultados
    # 'Kmeans' tuvo los mejores resultados

df_1_original = df_1_original.drop(columns=['CLUSTERS_MINIBATCH','CLUSTERS_BISECTING'])

##### Examinando los clusteres establecidos
df_1_original['CLUSTERS_KMEANS'].value_counts()
    # Existen 6 clusters: 0 - 5
clus_eda={}

for clus in range(df_1_original['CLUSTERS_KMEANS'].value_counts().shape[0]):
    df_clus = df_1_original[df_1_original['CLUSTERS_KMEANS']==clus].drop(columns='CLUSTERS_KMEANS')
    tmp = []
    for col in df_clus.columns:
        tmp_ds = df_clus[col]
        if is_numeric_dtype(tmp_ds):
            tmp.append(tmp_ds.mean())
        else:
            tmp.append(tmp_ds.value_counts().shape[0])
    clus_eda.update({f'cluster_{clus}': tmp})

tmp = []
for col in df_1_original.drop(columns='CLUSTERS_KMEANS').columns:
    tmp_ds = df_1_original[col]
    if is_numeric_dtype(tmp_ds):
        tmp.append(tmp_ds.mean())
    else:
        tmp.append(tmp_ds.value_counts().shape[0])
clus_eda.update({f'valores_distintos': tmp})

df_clu_eda = pd.DataFrame(clus_eda, index=df_clus.columns).round(2)
df_clu_eda

##### Analisis de clusters
df_1_original[df_1_original['CLUSTERS_KMEANS']==5]['OCM'].value_counts()
'CHILE' in df_1_original[df_1_original['CLUSTERS_KMEANS']==5]['PAIS'].values.tolist()
df_1_original[df_1_original['CLUSTERS_KMEANS']==1].shape[0]
df_1_encoded.info()

###### Visualizando KMeans clusteres
##### Colores
colores = ['indigo', 'green', 'blue', 'orange', 'violet', 'yellow']
cmap = ListedColormap(colores)
##### Boundary 
bounds = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
norm = BoundaryNorm(bounds, cmap.N)
##### Visual 2D
#### Creando PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(df_1_encoded)
fig = plt.figure(figsize=(10, 7))
#### Graficando clusteres
scatter = plt.scatter(
    X_pca[:,0],
    X_pca[:,1],
    c=df_1_original['CLUSTERS_KMEANS'],
    cmap=cmap,
    norm=norm,
    edgecolors='k'
)
#### Graficando clusteres centros
centers_pca = pca.transform(m1.cluster_centers_)
print(centers_pca)
plt.scatter(
    centers_pca[:,0],
    centers_pca[:,1],
    c='red',
    s=200,
    marker='X',
    label='Centros'
)
#### Configuraciones
cbar = plt.colorbar(scatter, ticks=[1,2,3,4,5,6], label='Cluster')
cbar.ax.set_yticklabels([1,2,3,4,5,6])
plt.title('Clusteres')
plt.xlabel("Componente Principal 1")
plt.xlim(-0.1, -0.05)
plt.ylim(-0.1, 0.1)
plt.ylabel("Componente Principal 2")
plt.legend()
# plt.colorbar(scatter, label='Cluster')
plt.show()




##### Visual 3D
#### Creando PCA
pca = PCA(n_components=3)
X_pca = pca.fit_transform(df_1_encoded)
#### Graficando clusteres
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(
    X_pca[:,0],
    X_pca[:,1],
    X_pca[:,2],
    c=df_1_original['CLUSTERS_KMEANS'],
    cmap=cmap,
    norm=norm,
    alpha=0.7,
    edgecolor='k'
)
#### Graficando clusteres centros
centers_pca = pca.transform(m1.cluster_centers_)
print(centers_pca)
ax.scatter(
    centers_pca[:,0],
    centers_pca[:,1],
    centers_pca[:,2],
    c='red',
    s=200,
    marker='X',
    label='Centros',
)
#### Configuraciones
ax.title('Clusteres')
ax.set_xlabel("Componente Principal 1")
ax.set_xlim(-0.1, 0.1)
ax.set_ylabel("Componente Principal 2")
ax.set_zlabel("Componente Principal 3")
ax.legend()
cbar = plt.colorbar(scatter, ticks=[1,2,3,4,5,6], label='Cluster')
cbar.ax.set_yticklabels([1,2,3,4,5,6])
# fig.colorbar(scatter, label='Cluster')
plt.show()
###########################################
##### Insights de KMeans
"""
It appears that K-Means yielded the best results with 6 clusters.

The 6 clusters are divided as follows:
Cluster 1
* OCM = Santa Rosa
* All: Months, Countries, Continents
* That is, simply arriving at the Santa Rosa OCM automatically creates a group
    - This is consistent with the EDA, considering that 32.9% of international visitors
            are Chilean and 80.3% of them enter through Santa Rosa
Cluster 2
* OCM = Cebaf - Tumbes, AIJC
* COUNTRY = Chile, U.S.
* CONTINENT = South America and North America
* All Months
* I.e., the mere fact of being Chilean or American automatically places them in a group
    - This is consistent with EDA, considering that these two countries account for 48% of all international visitors
Cluster 3
* OCM = AIJCH, Cebaf - Tumbes
* All: Months, Countries, Continents
* I.e., coming from the AIJCH and Cebaf-Tumbes OCMs constitutes a group
Cluster 4
* OCM = Others
* All: Months, Countries, Continents
* I.e., coming from the “OTHERS” OCMs constitutes a group
Cluster 5
* OCM = Desaguadero
* All: Months, Countries, Continents
* I.e., coming from the ‘DESAGUADERO’ OCMs constitutes a group
Cluster 6
* OCM = Kasani
* All: Months, Countries, Continents
* I.e., coming from the ‘KASANI’ OCMs constitutes a group
"""