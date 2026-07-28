import requests
import streamlit as st

def validate_input(input_value): #NEW 
    try:
        return float(input_value)
    except ValueError:
        return None

lat_input = st.text_input("Enter a latitude:") #NEW
lon_input = st.text_input("Enter a longitude:")

lat = validate_input(lat_input)
lon = validate_input(lon_input)

if lat is not None and lon is not None:
    api_key = "a0d010e8a3f85d10cb96017c547a0d6d"

    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    weather_data = response.json()

    if True:  
        st.markdown(f"### Weather Data for Coordinates: {lat}, {lon}") #NEW
        
        weather_fields = {
            "weather": "Weather Conditions",
            "main": "Main Info (Temperature, Feels Like, Pressure, Humidity)",
            "wind": "Wind Info (Speed, Gusts, Direction)",
            "clouds": "Cloud Coverage",
            "name": "City Name"
        }

        choice = st.selectbox("Select a weather field to display:", list(weather_fields.values())) #NEW
        selected_key = list(weather_fields.keys())[list(weather_fields.values()).index(choice)]

        if selected_key == "weather":
            for condition in weather_data["weather"]:
                st.write(f"**Condition:** {condition['description'].capitalize()}")
                st.image("Images/weather.jpg")

        elif selected_key == "main":
            temp = weather_data["main"]
            st.write(f"**Temperature:** {temp['temp'] - 273.15:.2f} °C")
            st.write(f"**Feels Like:** {temp['feels_like'] - 273.15:.2f} °C")
            st.write(f"**Pressure:** {temp['pressure']} hPa")
            st.write(f"**Humidity:** {temp['humidity']}%")
            
            data = {
                'Temperature (°C)': temp['temp'] - 273.15,  
                'Humidity (%)': temp['humidity']
            }
            st.bar_chart(data) #NEW
            st.image("Images/temp.png")

        elif selected_key == "wind":
            wind = weather_data["wind"]
            st.write(f"**Wind Speed:** {wind['speed']} m/s")
            st.write(f"**Wind Gusts:** {wind.get('gust', 'N/A')} m/s")
            st.write(f"**Wind Direction:** {wind['deg']}°")
            
            st.bar_chart({'Wind Speed (m/s)': wind['speed']})
            st.image("Images/wind.jpg")

        elif selected_key == "clouds":
            clouds = weather_data["clouds"]
            st.write(f"**Cloud Coverage:** {clouds['all']}%")
            st.image("Images/cloud.jpg")
            

        elif selected_key == "name":
            st.write(f"**City Name:** {weather_data['name']}")

    else:
        st.error("Could not retrieve weather data, please try again.")
else:
    st.error("Please enter valid latitude and longitude values. Longitude and Latitude values go from -90 to 90.")
