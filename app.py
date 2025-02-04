# api/app.py
from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

app = Flask(__name__)

def get_tehran_time():
    tehran_tz = pytz.timezone('Asia/Tehran')
    return datetime.now(tehran_tz).strftime("%Y-%m-%d %H:%M:%S")

@app.route('/api/cars')
def get_cars():
    try:
        url = "https://mashinbank.com/%D9%82%DB%8C%D9%85%D8%AA-%D8%AE%D9%88%D8%AF%D8%B1%D9%88"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        cars = []
        car_items = soup.find_all('div', class_='vehicle-price-item')
        
        for item in car_items:
            try:
                name = item.find('h2', class_='vehicle-name')
                price = item.find('div', class_='vehicle-price')
                details = item.find('div', class_='vehicle-details')
                
                cars.append({
                    'title': name.text.strip() if name else '',
                    'price': price.text.strip() if price else 'نامشخص',
                    'year': details.find('span', class_='year').text.strip() if details else '',
                    'update_time': get_tehran_time()
                })
            except Exception as e:
                print(f"Error parsing car: {e}")
                continue
        
        return jsonify({
            'status': 'success',
            'data': cars,
            'timestamp': get_tehran_time()
        })
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'timestamp': get_tehran_time()
        }), 500

if __name__ == '__main__':
    app.run()
