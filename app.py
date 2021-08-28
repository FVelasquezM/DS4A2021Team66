from flask import Flask, request, render_template, jsonify, make_response, after_this_request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, FileAllowed
from wtforms.validators import ValidationError
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

#Creacion de forms
class LoadImageForm(FlaskForm):
    image = FileField('Load image', validators=[FileAllowed(['tiff'])])
    submit = SubmitField('Submit')

#Rutas visuales
@app.route("/")
def load_main():
    '''
    Cargamos el index.html primera parte visual
    '''
    main_form = LoadImageForm()

    if main_form.validate_on_submit():
        filename = secure_filename(main_form.file.data.filename)
        main_form.file.data.save('uploads/' + filename)
        return redirect(url_for('load_app'))
    return render_template("inicio.html", data = main_form) #Inicio


@app.route("/app")
def load_app():
    '''
    Cargamos el app.html segunda parte visual
    '''
    return render_template("app.html") #App

@app.route("/verify-image", methods=["GET", "POST"]) #App
def verify_image():
    '''
    Verificamos la imagen
    '''
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return render_template("app.html")
    return render_template("app.html")
#Rutas verificar

#@app.route("/") #Load image

#@app.route("/") #checkbox


if __name__ == '__main__':
    app.run(debug = True)