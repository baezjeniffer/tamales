from flask import Flask,jsonify,request
from datetime import datetime

from main import transformation,save
from model import get_information,model

app = Flask(__name__)
@app.route("/reprocesamiento")
def process():
    try:
        date_exec = request.args.get('date_exec')
        date_exec = datetime(int(date_exec[:4]),int(date_exec[4:6]),int(date_exec[6:]))
        sales,fact_table,product_dim,region_dim,folder = transformation(date_exec=date_exec)
        save(sales,fact_table,product_dim,region_dim,folder=folder)
        return {"Flag":"True"}
    except:
        return {"Flag":"False"}

@app.route("/model")
def model_r():
    try:
        date = request.args.get('date')
        id_product = request.args.get('id_product')
        print(date,id_product)
        sales,category = get_information(id_product,date)
        print(sales,category)
        prediction = model(sales,category)
        return {"Flag":"True","Result":prediction}
    except:
        return {"Flag":"False","Result":None}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
