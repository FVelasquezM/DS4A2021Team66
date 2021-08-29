from flask import Flask, request, render_template, jsonify, make_response, after_this_request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
import json
from werkzeug.utils import secure_filename
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


@app.route("/app", methods=["POST"])
def dashboard():
    '''
    Cargamos el app.html segunda parte visual
    '''
    if request.method == "POST":
        if request.files:
            print('Soy request files')
            request.files.getlist('images[]')
        print('no images')
    return render_template("app.html") #App

if __name__ == '__main__':
    app.run(debug = True)