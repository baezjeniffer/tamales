import numpy as np
import random
import os
import collections
import pandas as pd
from datetime import datetime
import sys

random.seed(28999)

def model(sales,categorie_calorie):
    calorie_cat = "Zero"
    if calorie_cat == "Zero":
        weight = 0.25
    elif calorie_cat == "Light":
        weight = 0.5
    elif calorie_cat == "Regular":
        weight = 1.5
    return (np.log(sales)*np.random.uniform(-1,1,1)[0]+weight)

def get_information(id_product,date):
    path = "procesado/generador/tamales_inc/"
    lst_folders = os.listdir(path)
    lst_folders.sort()
    folder_date = lst_folders[-1]
    sales = pd.read_csv(path+folder_date+"/ventas_mensuales.csv",sep=',')
    id_product = int(id_product)
    sales = sales[(sales["id_product"]==id_product) & (sales["date"]==date)]["sales"].sum()
    path = "procesado/generador/teinvento_inc/"
    category = pd.read_csv(path+folder_date+"/product_dim.csv",sep=',')
    category = category[category["id_product"]==id_product]["calorie_category"].tolist()[-1]
    return sales,category

def main():
    if len(sys.argv) >= 3:
        id_product = sys.argv[1]
        print("id_product: "+ id_product)
        date       = str(sys.argv[2]) 
        print("date: "+ date)
    else:
        print ('Argument List:'+ str(sys.argv) )
        exit()
    sales,category = get_information(id_product,date)
    print(model(sales,category))

if __name__ == "__main__":
    main()