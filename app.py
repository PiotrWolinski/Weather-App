from flask import Flask, render_template, request
from datetime import datetime
import requests

from config import KEY

app = Flask(__name__, template_folder='templates')
base = 'https://api.openweathermap.org/data/2.5/weather'

def parse_name(s: str) -> str:
    words = s.split(' ')
    output = []
    for w in words:
        low_word = w.lower()
        print(low_word)
        tmp_word = low_word.split()
        tmp_word[0] = tmp_word[0].upper()
        output.append(''.join(tmp_word))

    return ' '.join(output)

def show_date() -> str:
    output = datetime.today().strftime("%A, %d %B %Y")
    return output
        

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

    url = f'{base}?q={city}&appid={KEY}&units=metric'

    response = requests.get(url)

    if response.status_code == 200:
        success = True
        weather_data = response.json()
        data = {}
        data['city'] = parse_name(city)
        data['temp_min'] = weather_data['main']['temp_min']
        data['temp_max'] = weather_data['main']['temp_max']
        data['country'] = weather_data['sys']['country']
        data['weather'] = weather_data['weather'][0]['description']
        data['day'] = show_date()

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