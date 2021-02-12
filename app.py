from flask import Flask, render_template, request
from datetime import datetime
import requests

app = Flask(__name__, template_folder='templates')
key = '581cee2f55870ef5bba4a1fb82038c6f'
base = 'https://api.openweathermap.org/data/2.5/weather'
WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday',
            'Thursday', 'Friday', 'Saturday', 'Sunday']

@app.route('/', methods=['GET'])
def index():
    city = request.args.get('city')

    if city is None:
        return render_template('index.html')

    url = f'{base}?q={city}&appid={key}&units=metric'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        day = WEEKDAYS[datetime.today().weekday()]
        country = data['sys']['country']
        print(country)

        return render_template('index.html', 
                                city=city, 
                                temp=temp, 
                                day=day, 
                                country=country)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()