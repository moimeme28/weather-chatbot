from flask import Flask, jsonify, request, render_template
import requests
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

# Your OpenWeather API Key
API_KEY = os.getenv('OPENWEATHER_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City is required'}), 400

    try:
        response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        )
        weather = response.json()

        if weather.get('cod') != 200:
            return jsonify({'error': 'City not found'}), 404

        return jsonify({
            'city': weather['name'],
            'temperature': weather['main']['temp'],
            'description': weather['weather'][0]['description'],
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
    