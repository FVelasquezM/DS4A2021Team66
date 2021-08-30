from flask import Flask, request, render_template, jsonify, make_response, after_this_request, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
import os
from flask_cors import CORS

app = Flask(__name__)

#Config del entorno
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
CORS(app)
#Creacion de forms
class LoadImageForm(FlaskForm):
    photo = FileField('Load Image', validators=[
        FileRequired(),
        FileAllowed(['png', 'pdf', 'jpg'], "wrong format!")
    ])

#Rutas visuales
@app.route("/", methods=["POST", "GET"])
def load_main():
    '''
    Cargamos el index.html primera parte visual
    '''
    main_form = LoadImageForm()
    return render_template("inicio.html", form = main_form) #Inicio


@app.route("/app", methods=["POST", "GET"])
def dashboard():
    '''
    Cargamos el app.html segunda parte visual
    '''
    if request.method == "POST":
        if request.files:
            print('Soy request files')
            data = request.files.getlist('file')
            print(data[0])
    return render_template("app.html") #App


@app.route("/data-barplot", methods=["POST", "GET"])
def load_barplot():
    '''
    Visualización del barplot
    '''
    #Simulacion de datos
    data = {
        "cultivos": "10",
        "construcciones": "3",
        "bosques": "2",
        "lotesPastoreo": "4",
        "recursosHidricos": "1",
        "carreteras": "0",
        "viviendas": "6",
        "aleoductos": "1",
        "rios": "0",
        "montañas": "3"
    }
    res = make_response(jsonify(data), 200)
    if request.method == "POST":
        if request.files:
            print('Soy request files')
        if request.data:
            print('Soy request files')
        if request.json:
            print('Soy request files')
    return res
if __name__ == '__main__':
    app.run(debug = True)