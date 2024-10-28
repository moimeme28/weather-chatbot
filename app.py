from flask import Flask, jsonify, request, render_template
import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

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
    intent, city, date = parse_user_input(user_message)

    if not city:
        return jsonify({'reply': 'Please specify a city. For example, "weather in London".'})

    # Determine the type of request: current weather or forecast
    try:
        if intent == 'current':
            reply = get_current_weather(city)
        elif intent == 'forecast':
            reply = get_forecast(city, date)
        else:
            reply = "I'm sorry, I can only provide current weather or forecast information."

        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'reply': 'Sorry, I encountered an error fetching the weather.'})

def get_current_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()
    
    if data.get('cod') != 200:
        return 'City not found. Please try another city.'

    return f"The current temperature in {data['name']} is {data['main']['temp']}°C with {data['weather'][0]['description']}."

def get_forecast(city, date):
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    data = response.json()

    if data.get('cod') != "200":
        return 'City not found. Please try another city.'

    # Find the forecast closest to the specified date
    for forecast in data['list']:
        forecast_date = datetime.fromtimestamp(forecast['dt']).date()
        if forecast_date == date:
            return f"Forecast for {date} in {city}: {forecast['weather'][0]['description']}, around {forecast['main']['temp']}°C."
    
    return "Sorry, no forecast available for that date."

def parse_user_input(user_message):
    intent = ''
    city = None
    date = None

    if 'forecast' in user_message or 'tomorrow' in user_message or 'next week' in user_message:
        intent = 'forecast'
        # Set tomorrow's date if 'tomorrow' is mentioned
        if 'tomorrow' in user_message:
            date = datetime.now().date() + timedelta(days=1)
    elif 'weather' in user_message or 'current' in user_message:
        intent = 'current'

    # Extract city (look for "in [city]")
    words = user_message.split()
    if 'in' in words:
        city_index = words.index('in') + 1
        if city_index < len(words):
            city = words[city_index]
    
    return intent, city, date

if __name__ == '__main__':
    app.run(debug=True)
