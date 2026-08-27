"""

Data Cleaing

This file will clean and concatenate data

Details of the data files:
1. Directory: 'Visitantes Internacionales'
    * A: Excursionists
    * B: Tourists
    * C: Visitors
2. Dir: 'Visitantes en sitios Turisticos'
    * A: Tourist site visitors
3. Dir : 'List of tourist resources'
    * List
"""

##### Importing libraries
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re 

############################################################

##### Reading data
#### File names
nom_1A = 'Llegada_excursionistas_internacionales.csv'
nom_1B = 'Llegada_turistas_internacionales.csv'
nom_1C = 'Llegada_visitantes_internacionales.csv'
nom_2A = 'Visitantes_sitios_turisticos_2019_2025.csv'
nom_3A = 'web_scrapped_inventario_recursos_turisticos.csv'

#### Paths
    # 1 = Ingresos internacionales
    # 2 = Ingresos a sitios turisticos
    # 3 = Lista de recursos de sitios turisticos
path_1A = os.path.join(os.getcwd(), 'Datos', 'Originales', 'VisitantesInternacionales', nom_1A)
path_1B = os.path.join(os.getcwd(), 'Datos', 'Originales', 'VisitantesInternacionales', nom_1B)
path_1C = os.path.join(os.getcwd(), 'Datos', 'Originales', 'VisitantesInternacionales', nom_1C)
path_2A = os.path.join(os.getcwd(), 'Datos', 'Originales', 'VisitantesSitios', nom_2A)
path_3A = os.path.join(os.getcwd(), 'Datos','WebScrapped', nom_3A)

############################################################

# ##### Investigando relationship betwee: 1A, 1B, y 1C
# #### Cargando datos
# df1 = pd.read_csv(path_1A, sep=';', encoding='latin-1', header=0)
# df2 = pd.read_csv(path_1B, sep=';', encoding='latin-1', header=0)
# df3 = pd.read_csv(path_1C, sep=';', encoding='latin-1', header=0)

# #### Viendo value counts de tipo de visitantes
#     # RAzon por esta columna: la diferencia en los nombre de los
#             # datos son entre "excursionista", "turista", y "visitante"
# df1['TIPO_VISITANTE'].value_counts()
# df2['TIPO_VISITANTE'].value_counts()
# df3['TIPO_VISITANTE'].value_counts()

# #### RESULTS: 1C is the concatenation of 1A and 1B
#     # So we can simply focus on 1C
# del df1
# del df2
# del df3

############################################################
###### Cleaning non-scrapped data

##### Seleccionando los datos 
    # Nos vamos a enfocar en 1C y 2A
#### Leyendo datos
df_1c = pd.read_csv(path_1C, sep=';', encoding='latin-1', header=0)
df_2a = pd.read_csv(path_2A, sep=';', encoding='latin-1', header=0)

#### Resumen
df_1c.info()
df_2a.info()

#### Ordenando por anio y mes
df_1c = df_1c.sort_values(by=['ANIO', 'ID_MES'], ascending=[True, True])
df_2a = df_2a.sort_values(by=['ANIO', 'ID_MES'], ascending=[True, True])

############################################################

##### Reviewing null values
#### Contando cantidad de veces aparecidos
df_1c.isnull().sum()
    # Tiene nulos en 'BLOQUE', la cual no es necesario
df_2a.isnull().sum()
    # No tiene ningun nulo

#### Arreglando nulos
df_1c = df_1c.dropna(axis=1, how='any')
df_1c.info()

##### Limpiando nombres
df_2a['SITIO_TURISTICO'].value_counts()
df_2a['SITIO_TURISTICO'] = df_2a['SITIO_TURISTICO'].apply(lambda fila: fila.encode('latin-1').decode('utf-8'))
df_2a['SITIO_TURISTICO'].value_counts()

############################################################

##### Reviewing duplications
#### Contando numero de duplicados
df_1c.duplicated().sum()
    # 0 => nungun duplicado de filas completas
        # PERO si hay duplicados dentro columnas mismas
df_2a.duplicated().sum()
    # 0 => nungun duplicado de filas completas
        # PERO si hay duplicados dentro columnas mismas

############################################################

##### Savind cleaned data
path_save_1c = os.path.join('Datos','Limpios', 'visitantes_internacionales.csv')
path_save_2a = os.path.join('Datos','Limpios', 'visitantes_sitios_turisticos.csv')

if not os.path.exists(path_save_1c): 
    df_1c.to_csv(path_save_1c, index=False)

if not os.path.exists(path_save_2a):
    df_2a.to_csv(path_save_2a, index=False)








############################################################
###### Cleaning scrapped

##### SEleccionando los datos 
    # Nos vamos a enfocar en 1C y 2A
#### Leyendo datos
df_3a = pd.read_csv(path_3A, sep=',', encoding='utf-8', header=0)

#### Resumen
df_3a.info()
df_3a.head()


############################################################

##### Reviewing nulls
#### Contando cantidad de veces aparecidos
df_3a.isnull().sum()

#### Investigando areas de nulos
### 'Latitud' y 'longitud'
    # Son variables continuos - no categorical
    # Detalla la latitud y longitud del sitio turistico
df_3a[['LATITUD', 'LONGITUD']].describe()
df_3a.boxplot(column='LATITUD');plt.show()
df_3a.boxplot(column='LONGITUD');plt.show()
    # CONLUSION: no se va a utilizar estos datos -> ignorar los nulos



### "tipo"
    # Es una variable categorical
    # Detalla como ingresar al sitio
df_3a['TIPO'].value_counts()
    # Las categorias de ingresos son pocos y estructuradas
len(df_3a['TIPO'].value_counts().to_list())
    # Hay muchos valores repetidos => solo hay 16 valores unicos
df_3a['TIPO'].isna()
    # Boolean de las filas que tienen "Nan" en la columna 'TIPO'
df_3a_tipo_nulos = df_3a[df_3a['TIPO'].isna()]
    # Enfocandose en datos solo donde 'TIPO' = 'NaN'
df_3a_tipo_nulos.info()
    # Verificacion de que todos 'tipo' son nulos
    # Existen 1531 sitios/registros
df_3a_tipo_nulos['NOMBRE DEL RECURSO'].value_counts()
    # Viendo cuales son los sitios que tienen 'tipo' nulo
    # Parece que la mayoria de recursos son eventos diferentes
len(df_3a_tipo_nulos['NOMBRE DEL RECURSO'].value_counts().to_list())
    # Existe 1524 valores unicos (recordar que son 1531 registros)
    # Parece que son diferentos eventos en diferentes lugares
    # Posiblemente ocurren una o dos veces al anio
df_3a_tipo_nulos['CATEGORÍA'].value_counts()
    # Son mayoramente 2 categorias: 'folclore' y 'acontecimientos programados'
        # Esto es mas evidencia de que son eventos
df_3a_tipo_nulos['NOMBRE DEL RECURSO'].str.contains(
    r'fiesta|festival|feria',
    case=False,
    na = False
).value_counts()
    # Viendo cuantos recursos tienen 'fiesta,festival,feria' en nombre
listas = []   # Creando dict para ver frecuencias de palabras
df_3a_tipo_nulos['NOMBRE DEL RECURSO'].apply(
    lambda fila: listas.extend(list(
        pd.Series(fila.lower().split())
        .value_counts(sort=True)
        .to_dict()
        .items()))
)   # Contando las palabras dentro cada fila
freq = {}    # Creando lista de frecuencias
for key,value in listas:    # Llenando dict de frecuencias
    freq[key] = freq.get(key,0) + value
pd.Series(freq)\
    .sort_values(axis=0, ascending=False)\
    .head(30)   # Creado DF de palabras mas comunes
    # Aparte de articulos ("de", "la", etc), las palabras comunes son:
        # danza, fiesta, festividad, patronal, festival, carnaval
    # CONCLUSION: los 'tipo' nulos son eventos publicos y no sitios 
        # Por eso no tienen un precio/detalla al poder ingresar
        # No se ingresa a un evento publico, solo se aparece uno



### 'observacion'
    # Es una variables categorical
    # Detalla explicaciones sobre como ingresar al sitio
    # Hipotesis: parece que esto solo se activa cuando 
len(df_3a['OBSERVACION'].value_counts())
    # Existen 2007 valores unicos 
    # Recorda: Existen 2190 no-nulos observaciones
    # Por ende, las observaciones son generalmente unicas
df_3a_obser_nulos =  df_3a[df_3a['OBSERVACION'].isna()]
    # Creando df de solo 'observacion' nulos
df_3a_obser_nulos.info()
    # Viendo info de neuvo DF
    # Recordar que existe relacion entre 'tipo' y 'observacion'
df_3a_obser_nulos['TIPO'].value_counts()
    # Se investiga que las observaciones nulas son generalmente cuando 'tipo' = 'libre'
    # CONCLUSION: las 'obseracion' nulas son cuando el ingreso al sitio es libre
        # En otras palabras, cuando el sitio es libre no es necesario dar mas explicaciones



#### Fixing nulls
### Longitud y Latitud
    # Eliminar todos los nulos
df_3a = df_3a.dropna(subset=['LONGITUD', 'LATITUD'])
## Las dos columnas se confundieron: Long = Lat y vice verse
df_3a = df_3a.rename(columns={'LONGITUD':'LATITUD', 'LATITUD':'LONGITUD1'})
df_3a = df_3a.rename(columns={'LONGITUD1':'LONGITUD'})

### 'TIPO'
    # La mayoria de 'tipo' nulos son eventos
        # danza, fiesta, festividad, patronal, festival, carnaval
    # Enfoques de proyecto:
        # Segmentos K: touristas internacionales
        # Probabilidad p_k: marketing probabilidad
        # Ingreso r_k: ingreso promedio por turista
        # Costo c_k: costo promeio por turista
    # Entonces: solo enfocarnos en sitios con ingresos
        # Se va a utilizar para prediccir r_k
        # Eliminar nulos
df_3a = df_3a.dropna(subset=['TIPO'])
df_3a.info()

### 'OBSERVACION'
    # Similar a 'TIPO'
    # Se va a utilizar para ver el ingreso para touristas internacionales
    # Generalmente, as observaciones nulos son de 'tipo' = 'libre'
    # Ende: sustituir nulos por 'libre'
df_3a['OBSERVACION'] = df_3a['OBSERVACION'].fillna('Libre')
df_3a.info()


### Reseteando los indices
df_3a = df_3a.reset_index(drop=True)



############################################################

##### Review duplicates
#### Contando numero de duplicados
df_3a.duplicated().sum()

############################################################

##### Renaming columns
#### 'REGION' -> 'DEPARTAMENTO'
df_3a = df_3a.rename(columns={'REGIÓN':'DEPARTAMENTO'})

#### Borrando acentos
df_3a = df_3a.rename(columns={
    'CATEGORÍA':'CATEGORIA',
    'TIPO DE CATEGORÍA': 'TIPO_CATEGORIA',
    'SUB TIPO CATEGORÍA': 'SUBTIPO_CATEGORIA',
})
df_3a.info()

############################################################
###### Detailed investigation:  'TIPO' y 'OBSERVACION'

##### Cambiando ingresos y observaciones a sus valores numericos
#### Investigando 'INGRESO' general
df_3a[['TIPO','OBSERVACION']].info()    # Existen 4556 registros
df_3a['TIPO'].value_counts()
    # Existen 2 categorias generales
        # 1. Ingresos con solo 1 nota (sin "#")
        # 2. Ingresos con 2+ notas (con "#")



#### Investigando 'INGRESO' y 'OBSERVACION' con "#"
### Investigacion general
df_3a[df_3a['TIPO'].str.contains("#", case=False)].info()
    # Contiene 97 registros
df_3a[df_3a['OBSERVACION'].str.contains("#", case=False)].info()
    # Contiene 99 registros
### Viendo intereseccion entre los indices
df_3a[df_3a['OBSERVACION'].str.contains("#", case=False)].index.difference(
    df_3a[df_3a['TIPO'].str.contains("#", case=False)].index
)
    # Identificacion de los 2 indices: 3292, 3414
### Investigando ambos indices
df_3a.iloc[[3293, 3414]][['TIPO','OBSERVACION']]
df_3a.loc[3293, 'OBSERVACION']
df_3a.loc[3414, 'OBSERVACION']
    # Estas observacion con '#' solo lo tienen para cambiar
            # la notacion: 'numero cel' -> '#'
        # Si lo hubiera tenido previsto no huiera 
                # utilizado el delimiter '#'



#### Investigando cuantos registros tiene 'Libre' para ambos
    # CASO 1: ingreso = 0
df_3a[(df_3a['TIPO']=='Libre') & (df_3a['OBSERVACION']=='Libre')].info() # Existen 2365



#### Investigando cuantos registros tiene 'Libre' para 'TIPO' pero no 'OBSERVACION'
df_3a[(df_3a['TIPO']=='Libre') & (df_3a['OBSERVACION']!='Libre')].info() # Existen 633
df_3a[(df_3a['TIPO']=='Libre') & (df_3a['OBSERVACION']!='Libre')]['OBSERVACION']
    # Parece que ingreso es libre pero 'OBSERVACION' son recommendaciones generales
df_3a[(df_3a['TIPO']=='Libre') & (df_3a['OBSERVACION']!='Libre')][df_3a['OBSERVACION'].str.contains('s/', case=False)].info()
    # Existen 11 registros donde 'TIPO'='libre', 'OBSERVACION'!='Libre', pero 'OBSERVACION' contiene 's/
df_3a[(df_3a['TIPO']=='Libre') & (df_3a['OBSERVACION']!='Libre')]\
    [df_3a['OBSERVACION'].str.contains('s/', case=False)]['OBSERVACION']
    # 'TIPO' ='Libre' para nacionales pero tiene diferente precio para etranjeros
        # Reconociendo el scope es internacional, se tiene que considerar estos precios



#### Investigando cuantos registros tiene 'Libre' para 'TIPO' pero no 'OBSERVACION', pero igual es libre para todos
    #CASO 2: ingreso = 0
df_3a[(df_3a['TIPO']=='Libre') & (df_3a['OBSERVACION']!='Libre')][~df_3a['OBSERVACION'].str.contains('s/', case=False)].info()
    # Existen 622 = 633-11 registros que solo son recomendaciones => ingreso = 0



#### Investigando cuantos registros tiene 'Libre' para 'TIPO' pero no 'OBSERVACION', pero no es libre para todos
    # CASO 3: ingreso != 0
### Creando lista general
lista_precio = df_3a[(df_3a['TIPO']=='Libre') & (df_3a['OBSERVACION']!='Libre')]\
    [df_3a['OBSERVACION'].str.contains('s/', case=False)]\
    ['OBSERVACION'].to_list()
lista_precio_idx = df_3a[(df_3a['TIPO']=='Libre') & (df_3a['OBSERVACION']!='Libre')]\
    [df_3a['OBSERVACION'].str.contains('s/', case=False)]\
    ['OBSERVACION'].index.to_list()
### Haciendo "split" en 's/'
ingreso_caso3 = [] # List de oracion post 's/'
for obser, idx in zip(lista_precio, lista_precio_idx):
    ingreso = [float(num) for num in re.findall(r'\d+\.\d*', obser)]
    if len(ingreso) > 1: 
        ingreso = [sum(ingreso)/len(ingreso)]
    ingreso_caso3.append([ingreso[0], idx])


##### Conclusion de investigacion
    # Parece que 'TIPO' no tiene mucho impacto en la creacion de precio 'INGRESO'
    # En vez, toda esa informacion se encuentra en 'OBSERVACION'
        # si observacion tiene algun float: ingreso = procesamiento de esos floats
        # si observacion no tiene un float: ingreso = 0 





############################################################
###### Converting 'TIPO' y 'OBSERVACION' en 'INGRESO' numeric value

#### Creando DS variable numerico 'INGRESO'
ds_ingreso = pd.Series(np.nan, index=df_3a.index)
ds_ingreso.name = 'INGRESO'

#### Viendo cuantos 'INGRESO' son nulos
ds_ingreso.isna().sum() # 4556


#### Existen 2 casos para rellenar 'INGRESOS'
### Caso 1: 'OBSERVACION' no tiene ningun 's/' => ingreso = 0
ds_ingreso.iloc[
    df_3a[~df_3a['OBSERVACION'].str.contains('s/', case=False)].index
] = 0
ds_ingreso.isna().sum() # 795
### Caso 2: 'OBSERVACION' tiene algun 's/' => ingreso != 0
lista_precio = df_3a[df_3a['OBSERVACION'].str.contains('s/', case=False)]\
    ['OBSERVACION'].to_list()
lista_precio_idx = df_3a[df_3a['OBSERVACION'].str.contains('s/', case=False)]\
    ['OBSERVACION'].index.to_list()
for obser, idx in zip(lista_precio, lista_precio_idx):
    ingreso = [float(num) for num in re.findall(r'\d+\.*\d*', obser)] 
        # Buscar todos los valores numericos, incluyendo numeros
    ingreso = [num for num in ingreso if num < 200 and num != 51]
        # Solo enfocarse en valores numeros que puedan ser entradas
        # "51" = codigo de peru
    if len(ingreso) == 0: ingreso = [0]
    elif len(ingreso) > 1: ingreso = [sum(ingreso)/len(ingreso)]
    ds_ingreso.iloc[idx] = ingreso[0]
ds_ingreso.isna().sum() # 0 nulos




##### Uniendo 'INGRESO' columna a df_3a
df_3a.info()
df_3a = pd.concat([df_3a,ds_ingreso], axis=1)
df_3a.info()


############################################################


##### Saving cleaned data
path_save_3a = os.path.join('Datos','Limpios', 'inventario_recursos_turisticos.csv')

if not os.path.exists(path_save_3a):
    df_3a.to_csv(path_save_3a, index=False)
