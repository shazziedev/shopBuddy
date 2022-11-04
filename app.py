from flask import Flask, render_template, request, url_for, flash, redirect
from organic import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search/results/",methods=('GET','POST'))
def post():
    if request.method == 'POST':
        data = request.form['_data']
        if data:
            res = get_organic_results(data)
            print(res)
            return render_template('results.html',res=res)
    return render_template('results.html')


if __name__ == "__main__":
    app.run(debug=True)