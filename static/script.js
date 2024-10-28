// Event listener for Enter key
document.getElementById('userInput').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    const userInput = document.getElementById('userInput').value.trim();
    if (!userInput) return;

    appendMessage(userInput, 'user');
    document.getElementById('userInput').value = '';

    // Parse user input for intent and parameters
    const { intent, city, date } = parseUserInput(userInput);

    let weatherMessage = '';

    try {
        // Determine whether to fetch current weather or forecast
        if (intent === 'current') {
            weatherMessage = await fetchWeatherData(city, 'current');
        } else if (intent === 'forecast') {
            weatherMessage = await fetchWeatherData(city, 'forecast', date);
        } else {
            weatherMessage = "I'm sorry, I didn't understand that.";
        }
    } catch (error) {
        weatherMessage = "Error: Could not reach the weather service.";
    }

    appendMessage(weatherMessage, 'bot');
}

async function fetchWeatherData(city, type, date = null) {
    const apiKey = 'YOUR_API_KEY'; // Replace with your OpenWeatherMap API key
    
    // Set up the API endpoint URL
    let url = '';
    if (type === 'current') {
        url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;
    } else if (type === 'forecast') {
        url = `https://api.openweathermap.org/data/2.5/forecast?q=${city}&appid=${apiKey}&units=metric`;
    }

    const response = await fetch(url);
    const data = await response.json();

    // Process the response based on the request type
    if (type === 'current') {
        return `Currently in ${data.name}: ${data.weather[0].description}, ${data.main.temp}°C.`;
    } else if (type === 'forecast') {
        const forecast = parseForecast(data, date);
        return forecast ? forecast : "Sorry, no forecast available for that date.";
    }
}

// Helper function to parse forecast data for a specific date
function parseForecast(data, date) {
    const targetDate = new Date(date).toDateString();
    const forecast = data.list.find(item => {
        const itemDate = new Date(item.dt * 1000).toDateString();
        return itemDate === targetDate;
    });
    
    if (forecast) {
        return `Forecast for ${targetDate}: ${forecast.weather[0].description}, temperature around ${forecast.main.temp}°C.`;
    }
    return null;
}

// Basic NLU function to determine intent and extract date/city from user input
function parseUserInput(input) {
    input = input.toLowerCase();
    let intent = '';
    let city = 'New York'; // Default city; adjust as needed
    let date = '';

    if (/forecast|tomorrow|next week/.test(input)) {
        intent = 'forecast';
        if (input.includes('tomorrow')) {
            const tomorrow = new Date();
            tomorrow.setDate(tomorrow.getDate() + 1);
            date = tomorrow.toISOString().split('T')[0];
        }
        // Additional logic for other date parsing can be added here
    } else if (/today|now|current/.test(input)) {
        intent = 'current';
    }

    return { intent, city, date };
}

function appendMessage(message, sender) {
    const chatBox = document.getElementById('chatBox');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.innerText = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
