"""
Feature Engineering for Models
"""


##### Importing Libraries
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from sklearn.preprocessing import LabelEncoder

##### Verifying correlations for the one hot encoded DataFrame
def ohe_corr(df_enc):
    df_1_enc_corr= df_enc.corr().round(2)
    coords = list(zip(*np.where((df_1_enc_corr > 0.8) & (df_1_enc_corr<1.0))))
    cells_info = [
        (
            df_1_enc_corr.index[row], 
            df_1_enc_corr.columns[col], 
            df_1_enc_corr.iat[row, col]
        ) for row, col in coords
    ]
    for i, (col1, col2, num) in enumerate(cells_info):
        if col1 != col2: 
            print(cells_info[i])
    return cells_info


##### Reading Data
#### File paths
fpath_1 = 'Datos/Cleaned/visitantes_internacionales.csv'
fpath_2 = 'Datos/Cleaned/visitantes_sitios_turisticos.csv'

#### Loading data
df_1 = pd.read_csv(f'{os.getcwd()}/{fpath_1}')
df_2 = pd.read_csv(f'{os.getcwd()}/{fpath_2}')

############################################################
####### Datos 1


### Borrando columnas no necesarias
## Datos 1
df_1 = df_1.drop(columns=['FECHA_CORTE', 'TIPO_VISITANTE'])
## Eliminando columnas no necesarias
df_2 = df_2.drop(columns=['ï»¿FECHA_CORTE'])
## Filtracion de filas
df_2 = df_2[df_2['TIPO_VISITANTE'] == 'EXTRANJERO']
## Borrando columna no necesaria
df_2 = df_2.drop(columns=['TIPO_VISITANTE'])


############################################################
##### Datos 1
    # Cols: ANIO, ID_MES, ID_PAIS, PAIS, ID_CONTINENTE,
            # CONTINENTE, ID_OCM, OCM, DEPARTAMENTO_OCM,
            # NUMERO_VISITANTES
    # Estos datos se van a utilizar para hacer k-means en paises
        # Datos necesarios:
            # ID_MES, PAIS, CONTINENTE, OCM, NUMERO_VISITANTES
            # Entonces se tendra que codensar todas otras col
df_1.info()
#### Etapa 1: Correlacion
df_1[['ANIO', 'ID_MES', 'ID_PAIS', 'ID_CONTINENTE', 'ID_OCM', 'NUMERO_VISITANTES']].corr().round(4)
    # Ninguno de los |valores| >0.18 => no hay correlacion

#### Etapa 2: Escojer columnas
    # 'ID_MES', 'ID_PAIS', 'ID_CONTINENTE', 'ID_OCM', 'NUMERO_VISITANTES'

#### Etapa 3: Condensar datos
### Datos seleccionados
df_1_mod = df_1[['ID_MES', 'ID_PAIS', 'ID_CONTINENTE', 'ID_OCM', 'NUMERO_VISITANTES']]\
    .groupby(by=['ID_MES', 'ID_PAIS', 'ID_CONTINENTE', 'ID_OCM'], as_index=False)\
    ['NUMERO_VISITANTES'].sum()
### Datos originales de datos seleccionados
df_1_org = df_1[['MES', 'PAIS', 'CONTINENTE', 'OCM', 'NUMERO_VISITANTES']]\
    .groupby(by=['MES', 'PAIS', 'CONTINENTE', 'OCM'], as_index=False)\
    ['NUMERO_VISITANTES'].sum()

#### Etapa 4: Verificar correlacion final
df_1_mod.corr().round(4)
    # Ninguno de los |valores| >0.18 => no hay correlacion

#### Etapa 5: Hacer OHE (y normalizacion)
### OHE
df_1_encoded = pd.get_dummies(df_1_mod, columns=['ID_MES', 'ID_PAIS', 'ID_CONTINENTE', 'ID_OCM'], drop_first=False)
## Verificando correlacion de OHEs
ohe_corr(df_1_encoded)
## Eliminando columnas con alta correlacion
df_1_encoded = df_1_encoded.drop(columns='ID_CONTINENTE_11')
## Verificando correlacion de OHEs
ohe_corr(df_1_encoded)


### Normalizacion
df_1_encoded['NUMERO_VISITANTES'] =(
    (
        df_1_encoded['NUMERO_VISITANTES'] -\
        df_1_encoded['NUMERO_VISITANTES'].mean()
    ) / df_1_encoded['NUMERO_VISITANTES'].std()
)


#### Etapa 6: Guardar ambos datasets
df_1_org.to_csv(f'{os.getcwd()}/Datos/FeatEng/visitantes_internacionales_original.csv', index=False)
df_1_encoded.to_csv(f'{os.getcwd()}/Datos/FeatEng/visitantes_internacionales_encoded.csv', index=False)


############################################################
##### Datos 2
    # Cols: ANIO, ID_MES, DEPARTAMENTO,
            # SITIO_TURISTICO, NUMERO_VISITANTES
    # Esto se puede utilizar para hacer un regression
            # en los numero de visitantes por sitio
            # dado el mes

#### 1. Ver correlacion 
### Hacer label encoder
df_le = df_2.drop(columns='MES').copy()
vars_categoricales = ['DEPARTAMENTO', 'SITIO_TURISTICO']
for col in vars_categoricales:
    le = LabelEncoder()
    df_le[f'{col}_TRANS'] = le.fit_transform(df_le[col])
### Correlacion
df_le.drop(columns=['DEPARTAMENTO', 'SITIO_TURISTICO']).corr().round(4)
    # Ninguno de los |valores| > 0.177 => no correlacion

#### 2. Escojer columnas
    # Voy utilizar ['ID_MES', 'DEPARTAMENTO', 'SITIO_TURISTICO', 'NUMERO_VISITANTES']

#### 3. Condensar datos en columnas que no importan
### Modificados
df_2_mod = df_le.groupby(by=[
        'ID_MES', 
        'DEPARTAMENTO_TRANS', 
        'SITIO_TURISTICO_TRANS'
    ], as_index=False)\
    ['NUMERO_VISITANTES'].mean()
### Originales
df_2_org = df_le.groupby(by=[
    'ID_MES',
    'DEPARTAMENTO',
    'SITIO_TURISTICO'
    ], as_index=False)\
    ['NUMERO_VISITANTES'].mean()
df_2_mod['NUMERO_VISITANTES'].values.tolist()[:10]
df_2_org['NUMERO_VISITANTES'].values.tolist()[:10]

#### 4. Verificar correlacion final
df_2_mod.corr().round(4)
    # Ninguno de los |valores| > 0.2129 => no correlacion


#### 5. Hacer one hot encoding
### OHE
df_2_encoded = pd.get_dummies(df_2_mod, columns=['ID_MES', 'DEPARTAMENTO_TRANS', 'SITIO_TURISTICO_TRANS'], drop_first=False)
## Verificando correlacion de OHEs
cells = ohe_corr(df_2_encoded)

### Normalizacion
    # Lo voy hacer en otro codigo para poder exportarlo

#### 6. Guardar
df_2_org.to_csv('Datos/FeatEng/visitantes_sitios_turisticos_original.csv',index=False)
df_2_encoded.to_csv('Datos/FeatEng/visitantes_sitios_turisticos_encoded.csv',index=False)

