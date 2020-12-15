import pandas as pd
import os 

#Tamales INC

#homologar datos
fecha     = "20200801" ##AAAAMMDD
fuente    = "tamales_inc"
path      = fuente+"/"+"ventas_mensuales_tamales_inc/mx/"+fecha+"/csv/"

lst_csv_tamales   = []
longitud = 0
for region in os.listdir(path):
    aux   = pd.read_csv(path+region+"/ventas_mensuales_"+region+".csv",sep=',',header=None)
    #aux.columns = ["year","month","country","calorie_category","flavor","zone","product_code","product_name","sales"]
    lst_csv_tamales.append(aux)
    longitud+=len(aux)
print(longitud)
tamales = pd.concat(lst_csv_tamales,sort=True).reset_index(drop=True)
print(len(tamales))
path = "crudo/generador/"+fuente+"/"
if fecha not in os.listdir(path):
    os.mkdir(path+fecha)
tamales.to_csv(path+fecha+"/ventas_mensuales.csv",sep=',',index=False,header=False)

#Teinvento INC

#Homologar datos

##Fact
fuente = "teinvento_inc"
path = fuente+"/ventas_reportadas_mercado_tamales/mx/"+fecha+"/fact_table/"
lst_csv_teinvento_fact   = []
longitud = 0
lst_csv = [x for x in os.listdir(path) if x.endswith(".csv")]
for csv in lst_csv:
    aux   = pd.read_csv(path+csv,sep=',',header=None)
    #aux.columns = ["year","month","sales","id_region","id_product"]
    lst_csv_teinvento_fact.append(aux)
    longitud+=len(aux)
print(longitud)
fact = pd.concat(lst_csv_teinvento_fact,sort=True).reset_index(drop=True)
print(len(fact))
path = "crudo/generador/"+fuente+"/"
if fecha not in os.listdir(path):
    os.mkdir(path+fecha)
path = "crudo/generador/"+fuente+"/"
fact.to_csv(path+fecha+"/fact_table.csv",sep=',',index=False,header=False)

##product_dim
fuente = "teinvento_inc"
path = fuente+"/ventas_reportadas_mercado_tamales/mx/"+fecha+"/product_dim/"
lst_csv_teinvento_product_dim   = []
longitud = 0
lst_csv = [x for x in os.listdir(path) if x.endswith(".csv")]
for csv in lst_csv:
    aux   = pd.read_csv(path+csv,sep=',',header=None)
    #aux.columns = ["id_product","calorie_category","product","product_brand","producer"]
    lst_csv_teinvento_product_dim.append(aux)
    longitud+=len(aux)
print(longitud)
product_dim = pd.concat(lst_csv_teinvento_product_dim,sort=True).reset_index(drop=True)
print(len(product_dim))
path = "crudo/generador/"+fuente+"/"
if fecha not in os.listdir(path):
    os.mkdir(path+fecha)
path = "crudo/generador/"+fuente+"/"
product_dim.to_csv(path+fecha+"/product_dim.csv",sep=',',index=False,header=False)

##region_dim
fuente = "teinvento_inc"
path = fuente+"/ventas_reportadas_mercado_tamales/mx/"+fecha+"/region_dim/"
lst_csv_teinvento_region_dim   = []
longitud = 0
lst_csv = [x for x in os.listdir(path) if x.endswith(".csv")]
for csv in lst_csv:
    aux   = pd.read_csv(path+csv,sep=',',header=None)
    #aux.columns = ["id_region","country","region"]
    lst_csv_teinvento_region_dim.append(aux)
    longitud+=  len(aux)
print(longitud)
region_dim = pd.concat(lst_csv_teinvento_region_dim,sort=True).reset_index(drop=True)
print(len(region_dim))
path = "crudo/generador/"+fuente+"/"
if fecha not in os.listdir(path):
    os.mkdir(path+fecha)
path = "crudo/generador/"+fuente+"/"
region_dim.to_csv(path+fecha+"/region_dim.csv",sep=',',index=False,header=False)

