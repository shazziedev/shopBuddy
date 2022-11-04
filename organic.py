
from hashlib import algorithms_available
from bs4 import BeautifulSoup
import requests, json, lxml, os
from serpapi import GoogleSearch
import re

headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}   

list_price = []

def get_organic_results(string):
    html = requests.get(f'https://www.ebay.com/sch/i.html?_nkw={string}', headers=headers).text
    soup = BeautifulSoup(html, 'lxml')

    data = []

    for item in soup.select('.s-item__wrapper.clearfix'):
        title = item.select_one('.s-item__title').text
        link = item.select_one('.s-item__link')['href']
        # img_url = item.select_one('.s-item__image-img')['src']
    
        try:
            img_url = item.select_one('.s-item__image-img')['src']
        except:
            img_url  = None 
        
        try:
            condition = item.select_one('.SECONDARY_INFO').text
        except:
            condition = None

        try:
            shipping = item.select_one('.s-item__logisticsCost').text
        except:
            shipping = None

        try:
            location = item.select_one('.s-item__itemLocation').text
        except:
            location = None

        try:
            watchers_sold = item.select_one('.NEGATIVE').text
        except:
            watchers_sold = None

        if item.select_one('.s-item__etrs-badge-seller') is not None:
            top_rated = True
        else:
            top_rated = False

        try:
            bid_count = item.select_one('.s-item__bidCount').text
        except:
            bid_count = None

        try:
            bid_time_left = item.select_one('.s-item__time-left').text
        except:
            bid_time_left = None

        try:
            reviews = item.select_one('.s-item__reviews-count span').text.split(' ')[0]
        except:
            reviews = None

        try:
            exctention_buy_now = item.select_one('.s-item__purchase-options-with-icon').text
        except:
            exctention_buy_now = None

        try:
            price = item.select_one('.s-item__price').text
            entry = re.findall(r'[\d]*[.][\d]+',price)
            digit_price = float(entry[0])
        except:
            price = None
            digit_price = None

        data.append({
            'digit_price':digit_price,
            'item': {
                'title': title, 
                'link': link, 
                'price': price,
                'img_url':img_url,
                
            },
            'condition': condition,
            'top_rated': top_rated,
            'reviews': reviews,
            'watchers_or_sold': watchers_sold,
            'buy_now_extention': exctention_buy_now,
            'delivery': {'shipping': shipping, 'location': location},
            'bids': {'count': bid_count, 'time_left': bid_time_left},
        })
  

    # sorting algorithm here
    
    return  data[1:] #{k: v for k, v in sorted(x.items(), key=lambda item: item[0])}