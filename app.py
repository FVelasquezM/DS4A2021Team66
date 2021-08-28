from flask import Flask, request, render_template, jsonify, make_response
import json

app = Flask(__name__)

#Rutas visuales
@app.route("/")
def main():
    '''
    Cargamos el index.html que es donde se almacena
    los recursos visuales de la aplicación
    '''
    return render_template("incio.html") #Inicio

@app.route("/") #App

#Rutas verificar

@app.route("/") #Load image
@app.route("/") #checkbox


if __name__ == '__main__':
    app.run(debug = True)