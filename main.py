import pandas as pd
import os 
from datetime import datetime,timedelta 
from utils import *

def transformation(date_exec=datetime.now()):
###Function to transform files to unique and centralized information
###Parameters:
###date_exec: datetime Execution date. Default today. 
    lst_dates = pd.date_range(date_exec-timedelta(days=7),date_exec).tolist()
    lst_dates = [x.strftime("%Y%m%d") for x in lst_dates]

    #Ventas
    source    = "tamales_inc"
    path      = "crudo/generador/"+source
    sales     = getDataByListDates(listDates=lst_dates, pathArg=path,file_name="ventas_mensuales")
    sales.columns = ["year","month","country","calorie_category","flavor","zone","product_code","product_name","sales"]
    folder    = [x for x in os.listdir(path) if x in lst_dates][-1]

    source    = "teinvento_inc"
    #fact_table
    path = "crudo/generador/"+source
    fact_table= getDataByListDates(listDates=lst_dates, pathArg=path,file_name="fact_table")
    fact_table.columns = ["year","month","sales","id_region","id_product"]

    #Product_dim
    product_dim = getDataByListDates(listDates=lst_dates, pathArg=path,file_name="product_dim")
    product_dim.columns = ["id_product","calorie_category","product","product_brand","producer"]

    #region_dim
    region_dim = getDataByListDates(listDates=lst_dates, pathArg=path,file_name="region_dim")
    region_dim.columns = ["id_region","country","region"]

    #id_product sales
    dict_id_product = dict(zip(product_dim["product"],product_dim["id_product"]))
    sales["product"] = [x+" "+y for x,y in zip(sales.product_name,sales.flavor)]
    sales["id_product"] = sales["product"].apply(lambda x:dict_id_product[x])
    #id_flavor product_dim
    dict_id_flavor = dict(zip(sales["id_product"],sales["flavor"]))
    product_dim["flavor"] = product_dim["id_product"].apply(lambda x: dict_id_flavor[x] if x in dict_id_flavor.keys() else None)
    #id_region sales
    dict_id_region = dict(zip(region_dim["region"],region_dim["id_region"]))
    sales["id_region"] = sales["zone"].apply(lambda x:dict_id_region[x])

    dict_months = dict(zip(['Dec','May','Jan','Feb','Mar','Apr','Jun','Jul','Aug','Sep','Oct','Nov'],[12,5,1,2,3,4,6,7,8,9,10,11]))

    sales["month2"] = sales["month"].apply(lambda x: dict_months[x])
    sales["date"] = list(map(lambda year,month: datetime(year,month,1),sales.year,sales.month2))
    sales = sales.sort_values(by="date",ascending=False).reset_index(drop=True)
    sales = sales[["date","sales","id_product","id_region"]]

    fact_table["month2"] = fact_table["month"].apply(lambda x: dict_months[x])
    fact_table["date"] = list(map(lambda year,month: datetime(year,month,1),fact_table.year,fact_table.month2))
    fact_table = fact_table.sort_values(by="date",ascending=False).reset_index(drop=True)
    fact_table = fact_table[["date","sales","id_product","id_region"]].rename(columns={"sales":"sales_teinvento"})


    sales = sales.groupby(["date","id_product","id_region"]).sum().reset_index()
    sales["sales_cum"] = sales["sales"].cumsum()
    sales["sales_dif%"]= [crecimiento(x,y) for x,y in zip(sales["sales"],[None]+sales["sales"].tolist()[:-1])]
    sales["sales_cum_dif%"]= [crecimiento(x,y) for x,y in zip(sales["sales_cum"],[None]+sales["sales_cum"].tolist()[:-1])]

    fact_table = fact_table.groupby(["date","id_product","id_region"]).sum().reset_index()
    fact_table["sales_teinvento_cum"] = fact_table["sales_teinvento"].cumsum()
    fact_table["sales_teinvento_dif%"]= [crecimiento(x,y) for x,y in zip(fact_table["sales_teinvento"],[None]+fact_table["sales_teinvento"].tolist()[:-1])]
    fact_table["sales_teinvento_cum_dif%"]= [crecimiento(x,y) for x,y in zip(fact_table["sales_teinvento_cum"],[None]+fact_table["sales_teinvento_cum"].tolist()[:-1])]
    print("Transformation is ready")
    for df,csv in zip([sales,fact_table,product_dim,region_dim],["ventas_mensuales.csv","fact_table.csv","product_dim.csv","region_dim.csv"]):
        df["date_exec"] = date_exec
        df["version"]   = 1
    return sales,fact_table,product_dim,region_dim,folder

def save(sales,fact_table,product_dim,region_dim,folder):
    for df,csv in zip([sales,fact_table,product_dim,region_dim],["ventas_mensuales.csv","fact_table.csv","product_dim.csv","region_dim.csv"]):
        if csv=="ventas_mensuales.csv":
            source = "tamales_inc"
            path = "procesado/generador/"+source+"/"+folder+"/"
            if folder not in os.listdir("procesado/generador/"+source+"/"):
                os.mkdir(path)
            df.to_csv(path+csv,sep=',',index=False)
            print(path+csv)
        else:
            source = "teinvento_inc"
            path = "procesado/generador/"+source+"/"+folder+"/"
            if folder not in os.listdir("procesado/generador/"+source+"/"):
                os.mkdir(path)
            df.to_csv(path+csv,sep=',',index=False)
            print(path+csv)
    print("Files saved")

def main():
    if len(sys.argv) >= 2:
        print(sys.argv[1])
        date_exec = str(sys.argv[1])
        date_exec = datetime(int(date_exec[:4]),int(date_exec[4:6]),int(date_exec[6:]))
        print("Date execution: ",date_exec)
    else:
        print ('Argument List:'+ str(sys.argv) )
        print ("Se requiere como argumento fecha de ejecución")
        exit()

    sales,fact_table,product_dim,region_dim,folder = transformation(date_exec=date_exec)
    save(sales,fact_table,product_dim,region_dim,folder=folder)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
