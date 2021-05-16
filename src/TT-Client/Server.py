import csv
import numpy as np
import requests
import pandas as pd
from flask import Flask, flash, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/computacion')
def computacion():
    return render_template('computacion.html')

@app.route('/sistemas', methods=["GET", "POST"])
def sistemas():
    if request.method == 'POST':
        if request.form['custId'] == "1":
            code = 0
            ciclo = request.form['ciclo']
            programacion_1 = request.form['programacion_1']
            fisica_2 = request.form['fisica_2']
            algebra_lineal = request.form['algebra_lineal']
            calculo_diferencial = request.form['calculo_diferencial']
            calculo_integral = request.form['calculo_integral']
            lista = [int(algebra_lineal), int(calculo_diferencial), int(calculo_integral), int(programacion_1), int(fisica_2)]
            dictToSend = {"ciclo": ciclo, "data": [lista]}
            res = requests.post('https://cis-unl.herokuapp.com/predecir', json = dictToSend)
            dictFromServer = res.json()
            res = dictFromServer['Result']
            if res[0] == 1:
                text = "REPRUEBA"
            else:
                text = "APRUEBA"
        else:
            code = 1
            ciclo = request.form['ciclo']
            file = request.files["file"]
            dataset = pd.read_csv(file)
            dataset = dataset.astype(int)
            data = dataset.values.tolist()
            dictToSend = {"ciclo": ciclo, "data": data}
            res = requests.post('https://cis-unl.herokuapp.com/predecir', json = dictToSend)
            dictFromServer = res.json()
            res = dictFromServer['Result']
            reprueban = res.count(1)
            all = len(res)
            porcentaje = (100 * reprueban) / all
            text = "{0:.2f}".format(porcentaje)
        return render_template('result.html', code = code, ciclo = ciclo, result =  text)
        #Codigo cero representa la consulta por una muestra
        #codigo 1 representa la consulta en porcentaje
    return render_template('sistemas.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

def readNpy():
    ciclo = str(10)
    path_array = 'Includes/Data_numpy/array_X_cis_'+ciclo+'.npy'
    path_csv = 'Includes/Data_csv/Dataset_cis_'+ciclo+'.csv'
    data = np.load(path_array)
    np.savetxt(path_csv, data, delimiter=',')


def loadNummpyArray(ciclo):
    #ciclo = str(3)
    path_array_X = 'Includes/Data_numpy/array_X_cis_' + ciclo + '.npy'
    path_array_Y = 'Includes/Data_numpy/array_y_cis_' + ciclo + '.npy'
    X_test = np.load(path_array_X)
    y_test = np.load(path_array_Y)
    print(X_test.tolist())
    print(y_test.tolist())


if __name__ == "__main__":
    loadNummpyArray(str(10))
    app.run(host='127.0.0.1', port=50000, debug=True)