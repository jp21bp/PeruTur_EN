"""
This file creates a web scraper in order to extract entry price information of turist sites in Peru
"""

#########################################
##### Setup general
#### Importing libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import pandas as pd
import os

#### Reading data
datos_path = os.path.join(
    os.getcwd(),
    'Datos', 
    'Original',
    'InventorioRecursosTuristicos',
    'Inventario_recursos_turisticos.csv')
df = pd.read_csv(datos_path, sep=';', encoding='latin-1', header=0)
urls = df['URL'].values.tolist()


#########################################
##### Web scrapping entry prices
#### Setup
filas = []
start = 0
#### For loop 
for i, url in enumerate(urls[start:]):
    print(i + start)
    ### SEtup
        # Each page has "tipo" and "observacion"
    tipo = []
    observacion = []
    ### Loading page
    driver = webdriver.Edge()
    driver.get(url)
    WebDriverWait(driver, 120).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#accordionContent"))
    )  

    ### Finding main list
    acordion = driver.find_element(By.CSS_SELECTOR, "#accordionContent")
        # Main list
    categorias_tags = acordion.find_elements(By.CSS_SELECTOR, ":scope > h3")
        # List children
    categorias = [categoria.text.lower() for categoria in categorias_tags]
        # De-capitalizing

    ### Cases
    if "tipo de ingreso" in categorias:
        idx = categorias.index('tipo de ingreso')
            # Finding the category with "tipo de ingreso"
        ingreso_div = acordion.find_element(By.CSS_SELECTOR, f'#ui-accordion-accordionContent-panel-{idx}')
            # Finding associated div
        driver.execute_script("arguments[0].setAttribute('style', 'display: block;');", ingreso_div)
            # Activating the javascript of the associated div
        ingreso_table = ingreso_div.find_elements(By.XPATH, ".//td[@align='left']")
            # Finding the elements of the tables
        impar = True
        for itm in ingreso_table: 
            if impar: tipo.append(itm.text)
            else: observacion.append(itm.text)
            impar = not impar
        filas.append(["#".join(tipo), "#".join(observacion)])
    else:
        filas.append(['NA','NA'])
    driver.quit()

##########################################
##### Finalizing web scrapping
#### Transforming data in DataFrame
tmp = pd.DataFrame(filas, columns=['TIPO','OBSERVACION'])
tmp_path = os.path.join('Datos', 'Webscapped', 'ingresos_web_scrapped.csv')
tmp.to_csv(tmp_path, index=False, encoding='utf-8')

#### Concatenating DataFrames
df_final = pd.concat([df, tmp], ignore_index=False, axis=1)

#### Saving final concatenated DF
limpio_path = os.path.join('Datos', 'WebScapped', 'web_scrapped_inventario_recursos_turisticos.csv')
df_final.to_csv(limpio_path, index=False, encoding='utf-8')
