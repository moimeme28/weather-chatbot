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

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message').lower()

    if 'weather' in user_message:
        # Extract city from user message
        words = user_message.split()
        if 'in' in words:
            city_index = words.index('in') + 1
            if city_index < len(words):
                city = words[city_index]
            else:
                return jsonify({'reply': 'Please specify a city.'})
        else:
            return jsonify({'reply': 'Please specify a city using "in". For example, "weather in London".'})

        # Fetch weather data
        try:
            response = requests.get(
                f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
            )
            weather = response.json()

            if weather.get('cod') != 200:
                return jsonify({'reply': 'City not found. Please try another city.'})

            reply = f"The current temperature in {weather['name']} is {weather['main']['temp']}°C with {weather['weather'][0]['description']}."
            return jsonify({'reply': reply})
        except Exception as e:
            return jsonify({'reply': 'Sorry, I encountered an error fetching the weather.'})

    else:
        return jsonify({'reply': "I'm sorry, I can only provide weather information. Try asking about the weather in a specific city."})

if __name__ == '__main__':
    app.run(debug=True)