from flask import Flask, render_template, request
from datetime import datetime, timezone
import requests

from config import OPENWEATHER_KEY

app = Flask(__name__, template_folder='templates')
OW_BASE = 'https://api.openweathermap.org/data/2.5/weather'

# ensures that the first letter will be capital and other small
def parse_name(s: str) -> str:
    words = s.split(' ')
    output = []
    for w in words:
        low_word = w.lower()
        tmp_word = list(low_word)
        tmp_word[0] = tmp_word[0].upper()
        output.append(''.join(tmp_word))

    return ' '.join(output)

# parses current date to format: "WEEKDAY, DD MM YYYY"
def show_date() -> str:
    output = datetime.today().strftime("%A, %d %B %Y")
    return output

# gets weather info based on the city name
def get_weather(city: str) -> dict:
    url = f'{OW_BASE}?q={city}&appid={OPENWEATHER_KEY}&units=metric'

    response = requests.get(url)

    if response.status_code == 200:
        weather_data = response.json()
        data = {}
        data['city'] = parse_name(city)
        data['temp_min'] = weather_data['main']['temp_min']
        data['temp_max'] = weather_data['main']['temp_max']
        data['country'] = weather_data['sys']['country']
        data['weather'] = weather_data['weather'][0]['description']

        lat = weather_data['coord']['lat']
        lng = weather_data['coord']['lon']

        data['day'] = show_date()
        return data
    else:
        return None

@app.route('/', methods=['GET'])
def index():
    city = request.args.get('city')
    initial = True
    success = False

    if city is None:
        return render_template('index.html', 
                                success=success, 
                                initial=initial)

    initial = False
    
    data = get_weather(city)

    if data is not None:
        success = True
        return render_template('index.html', 
                                data=data,
                                success=success,
                                initial=initial)
    else:
        return render_template('index.html', 
                                success=success,
                                initial=initial)


if __name__ == '__main__':
    app.run()