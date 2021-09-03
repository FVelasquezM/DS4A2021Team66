import os
from flask import Flask, render_template, request, redirect, url_for, session
from app_functions import save_send_img
from pathlib import Path

# flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)


@app.route('/', methods=['GET', 'POST'])
def inicio():
    """
    Route for the main page

    If uploades image:
        Receives the uploaded Tiff image and send it to api backend model
        When receives response as classification dataframe renders '/app' route
    """

    if request.method == 'POST':
        file = request.files['file']
        save_send_img(file)

        return redirect(url_for('dashboard'))

    return render_template("inicio.html")


# app route
@app.route("/app", methods=["POST", "GET"])
def dashboard():
    """
    Route for application page
    """
    x = 0
    return render_template("app.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
