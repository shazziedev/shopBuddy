import requests
import json

def get_amasample(string):
    res_API = requests.get('http://amasample.herokuapp.com/api/products/')
    data = res_API.text
    res = json.loads(data)
    
    data = []
    
    for item in res:
        if string.lower() in item['name'].lower():
            price = item['price']
            kwrds = item['name'].lower().split(' ')
            slug = '-'.join(kwrds)
            data.append({
                'digit_price':price,
                'item': {
                    'title':item['name'] , 
                    'link': f'http://amasample.herokuapp.com/products/{slug}/{item["id"]}/', 
                    'price': f"${price}",
                    'img_url':item['thumb'],
                    
                },
                'condition': None,
                'top_rated': None,
                'reviews': None,
                'watchers_or_sold': None,
                'buy_now_extention': None,
                'delivery': {'shipping': None, 'location': item['location']},
                'bids': {'count': None, 'time_left': None},
            })

    data.sort(key=lambda x: x["digit_price"])
    return  data[1:] 
