import os
from flask import Flask,render_template, request, redirect, url_for,session
from app_functions import save_send_img
from pathlib import Path

# flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)


## route for main page
@app.route('/', methods=['GET', 'POST'])
def inicio():
    # receives image uploaded, saves it locally, sends to back and saves the returned csv
    ## redirects then to app page
    if request.method == 'POST':
        file = request.files['file']
        save_send_img(file)
    
        return redirect(url_for('dashboard'))


    return render_template("inicio.html")


# app route
@app.route("/app", methods=["POST", "GET"])
def dashboard():
    x=0
    return render_template("app.html") #App


if __name__ == '__main__':    
    app.run(debug=True, host='0.0.0.0')



    