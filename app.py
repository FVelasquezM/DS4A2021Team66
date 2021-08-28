from flask import Flask, request, render_template, jsonify, make_response, after_this_request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
import json
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

#Config del entorno
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

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
    if request.method == "POST":
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(main_form.upload.data.filename))
        main_form.upload.data.save(file_path)
        return redirect(url_for('dashboard'))
    return render_template("inicio.html", form = main_form) #Inicio


@app.route("/app", methods=["POST"])
def dashboard():
    '''
    Cargamos el app.html segunda parte visual
    '''
    return render_template("app.html") #App
#Rutas verificar

#@app.route("/") #Load image

#@app.route("/") #checkbox


if __name__ == '__main__':
    app.run(debug = True)