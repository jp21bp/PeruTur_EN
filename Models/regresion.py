"""
Este archivo sera la creacion de los modelos:
* Regression: para predecir num_visitantes dado el sitio, dept, y mes
"""

##### Importaciones
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
#### Regresion
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error,\
    root_mean_squared_error, r2_score
import joblib
import statsmodels.api as sm # OLS
from sklearn.linear_model import LinearRegression # Lin Regression
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import Lasso #Lasso regresion
from sklearn.ensemble import RandomForestRegressor # RF
from sklearn.model_selection import GridSearchCV
#### Hypothesis testing



###################################################
###### Setup

##### Leyendo datos
df_2_original = pd.read_csv(f'{os.getcwd()}/Datos/FeatEng/visitantes_sitios_turisticos_original.csv')
df_2_encoded = pd.read_csv(f'{os.getcwd()}/Datos/FeatEng/visitantes_sitios_turisticos_encoded.csv')
df_2_encoded.info()
##### Etiquetando datos
X = df_2_encoded.drop(columns='NUMERO_VISITANTES')
y = df_2_encoded['NUMERO_VISITANTES']
##### Verificando datos importados
df_2_encoded['NUMERO_VISITANTES'].values.tolist()[:10]
df_2_original['NUMERO_VISITANTES'].values.tolist()[:10]


##### Separando datos
X_train, X_test, y_train, y_test = \
    train_test_split(X,y,test_size=0.2, random_state=42)


#### Buscando los indices de datos originales
idxs = y_test.index.to_list()
df_2_org_test = df_2_original.iloc[idxs]

##### Haciendo reshapes
# X_train = X_train.values.reshape(-1,1)
# X_test = X_test.values.reshape(-1,1)
y_train = y_train.values.reshape(-1,1)
y_test = y_test.values.reshape(-1,1)


##### Normalizacion
    # X todos son bool
    # y es int64, implicando que necesita scaler
scaler = StandardScaler()
y_train = scaler.fit_transform(y_train)
joblib.dump(scaler, './Modelos/scaler.pkl')
y_test = scaler.transform(y_test)


##### Haciendo el accuracy score
def performance(nom, prediccion):
    mae = mean_absolute_error(y_test, prediccion)
    mse = mean_squared_error(y_test, prediccion)
    rmse = root_mean_squared_error(y_test, prediccion)
    r2 = r2_score(y_test, prediccion)
    return pd.DataFrame(
        {f'{nom}_metrics': [mae, mse, rmse, r2]},
        index=['MAE', 'MSE', 'RMSE', 'R2']
    )


#############################################
###### Modelos

##### OLS
#### Entrenando OLS
X_sm = sm.add_constant(X_train)
X_sm = X_sm.astype(float)
model_ols = sm.OLS(y_train, X_sm)
summary = model_ols.fit().summary()

#### Convirtiendo OLS summary en DF
tabla_arr = summary.tables[1]
df_ols = pd.DataFrame(tabla_arr.data[1:], columns=tabla_arr.data[0])
df_ols = df_ols.rename(columns={'':'Variable'})
for col in df_ols.columns.to_list()[1:]:
    df_ols[col] = df_ols[col].astype(float)
df_ols.info()
varaibles_sign = df_ols[df_ols['P>|t|'] < 0.05]['Variable']
varaibles_sign.head(20)




##### Linear regression
linear_reg = LinearRegression()
linear_reg.fit(X_train, y_train)
lr_y_pred = linear_reg.predict(X_test)
df_lr_results = performance('lin_reg', lr_y_pred)



##### Lasso regression
#### Buscando mejor alpha
alpha, error = [], []
for i in range(1,1000):
    alpha.append(i/1000)
    candidato = Lasso(alpha=(i/1000))
    error.append(
        np.mean(
            cross_val_score(
                candidato,
                X_train,
                y_train,
                scoring='neg_root_mean_squared_error',
                cv=3,
            )
        )
    )
plt.plot(alpha,error)
plt.show()
#### Escojiendo el mejor alpha
err= tuple(zip(alpha,error))
df_err = pd.DataFrame(err, columns = ['alpha', 'error'])
df_alpha = df_err[df_err.error == max(df_err.error)]['alpha']
mejor_alpha = df_alpha.values[0]
mejor_alpha
#### Usando el mejor alpha
lasso_reg = Lasso(alpha=mejor_alpha)
lasso_reg.fit(X_train,y_train)
lasso_y_pred = lasso_reg.predict(X_test)
df_lasso_results = performance('lasso', lasso_y_pred)
df_lasso_results



##### RF
#### Buscando los mejores parametros
rf = RandomForestRegressor()
params = {
    'n_estimators': range(10,300,10),
    'criterion': ('squared_error','absolute_error'),
    'max_features': ('auto', 'sqrt', 'log2')
}
gs = GridSearchCV(rf, params, scoring='neg_root_mean_squared_error', cv = 3)
gs.fit(X_train,y_train.reshape(-1))
gs.best_score_
gs.best_estimator_
#### Evaluando RF
rf_y_pred = gs.best_estimator_.predict(X_test)
df_rf_results = performance('rf', rf_y_pred)





##### Uniendo todos los resultados
df_resultados = pd.concat([
    df_lr_results, 
    df_lasso_results, 
    df_rf_results], axis=1)
df_resultados

##### Guardando el mejor modelo
joblib.dump(gs.best_estimator_, './Modelos/model.pkl')
