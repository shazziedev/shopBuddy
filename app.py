from flask import Flask, render_template, request, url_for, flash, redirect
from organic import *
from test import get_amasample

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/search/results/",methods=('GET','POST'))
def post():
    if request.method == 'POST':
        data = request.form['_data']
        if data:
            if request.form.getlist('ebay'):
                res = get_on_ebay(data)
            elif request.form.getlist('amasample'):
                res = get_amasample(data)
            return render_template('results.html',res=res)
        
    return render_template('results.html')


if __name__ == "__main__":
    app.run(debug=True)