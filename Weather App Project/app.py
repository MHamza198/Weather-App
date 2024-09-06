from flask import Flask, request, render_template
import requests

app = Flask(__name__)

def get_weather(api_key, location):
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        'key': api_key,
        'q': location,
        'aqi': 'no'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        location_name = data['location']['name']
        temp_c = data['current']['temp_c']
        weather = data['current']['condition']['text']
        humidity = data['current']['humidity']
        wind_kph = data['current']['wind_kph']

        return (f"Weather in {location_name}:<br>"
                f"Temperature: {temp_c}°C<br>"
                f"Weather: {weather}<br>"
                f"Humidity: {humidity}%<br>"
                f"Wind Speed: {wind_kph} kph")
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_info = ""
    if request.method == 'POST':
        location = request.form['location']
        api_key = '00f67e43c8b9456ea3b60906240609'
        weather_info = get_weather(api_key, location)
    
    return render_template('index.html', weather_info=weather_info)

if __name__ == '__main__':
    app.run(debug=True)
