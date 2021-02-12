from flask import Flask, render_template, request
from livereload import Server
from datetime import datetime
import requests

from config import KEY

app = Flask(__name__, template_folder='templates')
base = 'https://api.openweathermap.org/data/2.5/weather'
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday']

@app.route('/', methods=['GET'])
def index():
    city = request.args.get('city')

    if city is None:
        return render_template('index.html')

    url = f'{base}?q={city}&appid={KEY}&units=metric'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp_min = data['main']['temp']
        day = WEEKDAYS[datetime.today().weekday()]
        country = data['sys']['country']

        return render_template('index.html', 
                                city=city, 
                                temp=temp, 
                                day=day, 
                                country=country)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.serve(port=5000)