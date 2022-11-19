from test import get_amasample
from organic import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy.sql import func
from flask import Flask, flash, redirect, render_template, request, url_for
import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    productName = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.Integer, nullable=False )
    img = db.Column(db.String(800), nullable=True)
    location = db.Column(db.String(1000), nullable=False)
    shipping = db.Column(db.String(80), unique=True, nullable=False)
    date = db.Column(db.Date,default = date.today())

    def __repr__(self):
        return f'<My {self.productName}>'


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

    db.create_all()
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

@app.route("/search/results/save/<productName>")
def ama_save(productName):
    res = get_amasample(productName) 
    try: 
        for item in res:
            shippingdata = 'None'
            locationdata = 'None' 
            if item['location'] is not None:
                locationdata = item['location']
            if item['shipping'] is not None:
                shippingdata = item['shipping']
            
            cart_item = Cart(
                productName=item['title'],
                link=item['link'],
                price= item['price'],
                img=item['img_url'],
                location=locationdata,
                shipping=shippingdata
                )

            db.session.add(cart_item)
            db.session.commit()
    except:
        print("can't save twice")
    return redirect(url_for('saved'))

@app.route("/search/results/ebay/save/<productName>/<price>")
def ebay_save(productName,price):
    res = get_on_ebay(productName)
    try: 
        for item in res:
            shippingdata = 'None'
            locationdata = 'None' 
            if item['location'] is not None:
                locationdata = item['location']
            if item['shipping'] is not None:
                shippingdata = item['shipping']
            
            cart_item = Cart(
                productName=item['title'],
                link=item['link'],
                price= item['price'],
                img=item['img_url'],
                location=locationdata,
                shipping=shippingdata
                )
            db.session.add(cart_item)
            db.session.commit()
    except:
        print("can't save twice")
    return redirect(url_for('saved'))

@app.route('/saved')
def saved():
    res = Cart.query.all()
    return render_template('saved.html',res=res)


if __name__ == "__main__":
    app.run(debug=True)