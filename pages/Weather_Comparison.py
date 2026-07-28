import google.generativeai as genai
import requests
import streamlit as st

try:
    openweathermap_api_key = st.secrets["key"]
    gemini_api_key = st.secrets["googkey"]
    genai.configure(api_key=gemini_api_key)
except Exception as e:
    st.error("Error loading API keys from Streamlit secrets. Check your secrets.toml file.")
    st.stop()

def validate_input(input_value):
    try:
        return float(input_value)
    except ValueError:
        return None

st.title("Weather Comparison with Gemini 2.5 ☀️")

lat1_input = st.text_input("Enter the latitude for place 1:", key="lat1")
lon1_input = st.text_input("Enter the longitude for place 1:", key="lon1")
lat2_input = st.text_input("Enter the latitude for place 2:", key="lat2")
lon2_input = st.text_input("Enter the longitude for place 2:", key="lon2")

lat1 = validate_input(lat1_input)
lon1 = validate_input(lon1_input)
lat2 = validate_input(lat2_input)
lon2 = validate_input(lon2_input)

def fetch_weather_data(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={openweathermap_api_key}"
    response = requests.get(url)
    return response.json()

def get_gemini_response(weather_data_1, weather_data_2):
    try:
        if "main" not in weather_data_1 or "wind" not in weather_data_1:
             raise KeyError("Missing 'main' or 'wind' data for place 1.")
        if "main" not in weather_data_2 or "wind" not in weather_data_2:
             raise KeyError("Missing 'main' or 'wind' data for place 2.")
             
        temp1 = weather_data_1["main"]["temp"] - 273.15  
        temp2 = weather_data_2["main"]["temp"] - 273.15
        humidity1 = weather_data_1["main"]["humidity"]
        humidity2 = weather_data_2["main"]["humidity"]
        wind_speed1 = weather_data_1["wind"]["speed"]
        wind_speed2 = weather_data_2["wind"]["speed"]
        description1 = weather_data_1["weather"][0]["description"]
        description2 = weather_data_2["weather"][0]["description"]

        prompt = (
            f"Write an essay comparing the weather conditions between the following two places and determine which one has better weather. "
            f"Please attempt to infer and include the regions or countries. Base your answers strictly on the weather data provided. "
            f"Do not say 'place 1' or 'place 2'; refer to the locations by inferred regions/countries. Thank you:\n\n"
            f"Location 1 (Data): Temp: {temp1:.2f}°C, Humidity: {humidity1}%, Wind: {wind_speed1} m/s, Weather: {description1}\n\n"
            f"Location 2 (Data): Temp: {temp2:.2f}°C, Humidity: {humidity2}%, Wind: {wind_speed2} m/s, Weather: {description2}\n\n"
            f"Which location has better weather overall? Please include the name of the closest city and country."
        )

        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(prompt)  
        return response.text
    
    except KeyError as e:
        return f"Error: Failed to process weather data. Key missing: {e}. Check API response structure."
    except Exception as e:
        return f"Error with Google Gemini API: {str(e)}"

if lat1 is not None and lon1 is not None and lat2 is not None and lon2 is not None:
    if st.button("Compare Weather"):
        try:
            weather_data_1 = fetch_weather_data(lat1, lon1)
            weather_data_2 = fetch_weather_data(lat2, lon2)
    
            if weather_data_1.get("cod") == 200 and weather_data_2.get("cod") == 200:
                st.markdown("---")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"### Weather Data for Place 1: {lat1}, {lon1}")
                    st.write(f"Weather: {weather_data_1['weather'][0]['description']}")
                    st.write(f"Temperature: {weather_data_1['main']['temp'] - 273.15:.2f} °C")
                    st.write(f"Humidity: {weather_data_1['main']['humidity']}%")
                    st.write(f"Wind Speed: {weather_data_1['wind']['speed']} m/s")

                with col2:
                    st.markdown(f"### Weather Data for Place 2: {lat2}, {lon2}")
                    st.write(f"Weather: {weather_data_2['weather'][0]['description']}")
                    st.write(f"Temperature: {weather_data_2['main']['temp'] - 273.15:.2f} °C")
                    st.write(f"Humidity: {weather_data_2['main']['humidity']}%")
                    st.write(f"Wind Speed: {weather_data_2['wind']['speed']} m/s")
                
                st.markdown("---")
                with st.spinner('Asking Gemini to compare weather...'):
                    gemini_response = get_gemini_response(weather_data_1, weather_data_2)
                
                st.markdown("### Weather comparison between locations 🤖")
                st.write(gemini_response)
                
                try:
                    st.image("sunny.jpg")
                except FileNotFoundError:
                    st.warning("Image 'sunny.jpg' not found. Ensure it's in the same directory.")
            
            else:
                st.error(f"Error getting weather data. Check lat/lon values or API key. Place 1 Code: {weather_data_1.get('cod')}, Place 2 Code: {weather_data_2.get('cod')}.")
        
        except Exception as e:
            st.error(f"An unexpected error occurred during processing: {e}")

else:
    st.info("Enter valid latitude and longitude values to begin the comparison.")
