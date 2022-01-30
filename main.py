from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import requests
app = Flask(__name__)
Bootstrap(app)



@app.route("/", methods=['POST', 'GET'])
def home():
    return render_template("index.html")


@app.route("/userdata", methods=['POST', 'GET'])
def data():
    responce = requests.get('https://reqres.in/api/users?page=1')
    data = responce.json()
    print(data)

    return render_template("index.html", data=data['data'])




if __name__ == '__main__':
    app.run(debug=True)
