"""
Este archivo sera la creacion de los modelos:
* Regression: para predecir num_visitantes dado el sitio, dept, y mes
"""

##### Importaciones
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
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
from scipy import stats



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

#################################################################
###### Hypothesis testing
    # Performing test on top 5 tourist sites

##### Choosing corresponding data
#### Selecting the top 5 sites
top_X = 5
top_X_sitios = df_2_original.groupby(by='SITIO_TURISTICO', as_index=False)\
    ['NUMERO_VISITANTES'].agg('mean')\
    .sort_values(by='NUMERO_VISITANTES', ascending=False)\
    ['SITIO_TURISTICO'][:top_X].values.tolist()

#### Selecting site indices
idxs = df_2_original[df_2_original['SITIO_TURISTICO'].isin(top_X_sitios)].index
df_org_topX = df_2_original.iloc[idxs]
df_enc_topX = df_2_encoded.iloc[idxs].drop(columns='NUMERO_VISITANTES')


##### Predictions
#### Loading model and scaler
rf = joblib.load('./Models/model.pkl')
scaler = joblib.load('./Models/scaler.pkl')
#### Model invocation
y_pred = rf.predict(df_enc_topX)
#### Denormalizing
y_pred_denorm = scaler.inverse_transform(y_pred.reshape(-1,1))
#### Appending predictions to original data
df_org_topX['NUM_PRED'] = y_pred_denorm


##### Hypothesis testing on 5 sites
for site in top_X_sitios:
    # Extracting data from site on current iteration
    actual_nums = df_org_topX[df_org_topX['SITIO_TURISTICO'] == site]['NUMERO_VISITANTES']
    pred_nums = df_org_topX[df_org_topX['SITIO_TURISTICO'] == site]['NUM_PRED']
    # Test of normality
    _, actual_nums_pvalue = stats.shapiro(actual_nums.values)
    _, pred_nums_pvalue = stats.shapiro(pred_nums.values)
    # Formalizing
    actual_nums_normality = True if actual_nums_pvalue > 0.05 else False
    pred_nums_normality = True if pred_nums_pvalue > 0.05 else False
    print(f'Site {site} Normality - actual values: {actual_nums_normality}; predicted values: {pred_nums_normality}')
    # Hypothesis testing
    if actual_nums_normality and pred_nums_normality:
        # Both need to be normal to use T-test
        eq_var = True if actual_nums.std() == pred_nums.std() else False
        _, t_pvalue = stats.ttest_ind(
            actual_nums.values,
            pred_nums.values,
            equal_var=eq_var,
            alternative='two-sided'
        )
        if t_pvalue < 0.05:
            print(f'T-test p-value {t_pvalue}: accept the alternative hypothesis, the two samples are significantly different')
        else:
            print(f"T-test p-value {t_pvalue}: don't reject the null hypothesis, no significant difference between both samples")
    else:
        _, w_pvalue = stats.wilcoxon(
            actual_nums.values,
            pred_nums.values,
            alternative='two-sided'
        )
        if t_pvalue < 0.05:
            print(f'Wilcoxon p-value {w_pvalue}: accept the alternative hypothesis, the two samples are significantly different')
        else:
            print(f"Wilcoxon p-value {w_pvalue}: don't reject the null hypothesis, no significant difference between both samples")


#################################################################
    # Creating visuals #
##### Promedio de diferencia
df_org_topX['DIFF'] = abs(df_org_topX['NUMERO_VISITANTES'] - df_org_topX['NUM_PRED'])
diff_promedio = int(df_org_topX['DIFF'].mean().item())

##### Visuales
#### Configuracion inicial
ANCH = 8
ALT = 5
exp = 10000
fig, ax  = plt.subplots(figsize=(ANCH,ALT))
meses = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',\
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
colores = ["yellow", "purple", "cyan", "grey", "magenta", \
           "red", "black", "green", "orange", "blue"]
#### Graficando
for i in range(len(top_X_sitios)):
    ax.plot(
        range(len(meses)),
        df_org_topX[df_org_topX['SITIO_TURISTICO']==top_X_sitios[i]]['NUMERO_VISITANTES']/exp,
        label = top_X_sitios[i],
        marker='o',
        color = "#c0960cff",
        markerfacecolor = colores[i],
        markeredgecolor='black'
    )
    ax.plot(
        range(len(meses)),
        df_org_topX[df_org_topX['SITIO_TURISTICO']==top_X_sitios[i]]['NUM_PRED']/exp,
        label = top_X_sitios[i],
        marker='o',
        color = 'blue',
        markerfacecolor = colores[i],
        markeredgecolor='black'
    )
ax.set_xticks(range(len(meses)))
ax.set_xticklabels(meses)
ax.set_xlabel('Month', fontweight='bold')
ax.set_ylabel(f'Num Visitors (x{exp})', fontweight='bold')
ax.set_title(f'{diff_promedio} Average Tourist Difference between \nthe Prediction and Actual Value',
             fontweight='bold')
ax.set_ylim(0, max(df_org_topX['NUMERO_VISITANTES'])/exp + 2)
# Crear elementos personalizados para la leyenda
custom_lines = [
    Line2D([0], [0], color='blue', linestyle='-', lw=2),   
    Line2D([0], [0], color="#c0960cff", linestyle='-', lw=2),
]
for i in range(len(top_X_sitios)):
    custom_lines.append(
        Line2D([0], [0], color=colores[i], marker='o', lw=0, markersize=4)  # Puntos rojos
    )

# Agregar leyenda personalizada
ax.legend(
    custom_lines, 
    ['PREDICTIONS', 'ACTUAL VALUES'] + top_X_sitios, 
    loc='upper left',
    bbox_to_anchor =(-0.1, 1.04), 
    fontsize=7, 
    edgecolor='black',
    framealpha=1.0
    )
plt.show()