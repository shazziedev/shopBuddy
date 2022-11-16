from test import get_amasample
from organic import *

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)

@app.route("/")
def index():
    """
    _summary_
        simple ecommerce webscrapper built in flask
        scaps ebay and amasample.
        order products to find the cheepest product.
        
    Returns:
        html: empty form on the homepage and root url
    """
    return render_template('index.html')


@app.route("/search/results/",methods=('GET','POST'))
def post():
    """
    _summary_
        search on ebay or amasample. 
        handles user input and search online.
    Returns:
        html: results of web scrapped results
    """
    if request.method == 'POST':
        
        data = request.form['_data'] #obtain search data
        
        if data:
            res = []
            ama = []
            if request.form.getlist('ebay'): #check if ebay checkbox is checked
                # run ebay search algorithms_available
                res = get_on_ebay(data) 
            
            if request.form.getlist('amasample'):#check if ebay checkbox is checked
                # run amasample search algorithms_available
                ama = get_amasample(data)
       
            
            print('RES ------------------->',res)
            return render_template('results.html',res=res,ress=ama) #pass response to template
        
    return render_template('results.html') #if method is get, return blank form


if __name__ == "__main__":
    app.run(debug=True)