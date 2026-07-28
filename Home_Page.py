import streamlit as st

# Title of App
st.title("Personal Portfolio & Weather API Project")
st.image("coverphoto.jpg")

# Assignment Data 
# TODO: Fill out your team number, section, and team members

st.header("Arshan Kadri and Daniel Wu")

# Introduction
# TODO: Write a quick description for all of your pages in this lab below, in the form:
#       1. **Page Name**: Description
#       2. **Page Name**: Description
#       3. **Page Name**: Description
#       4. **Page Name**: Description

st.write("""
Welcome to our Streamlit Web Development app! You can navigate between the pages using the sidebar to the left. The following pages are:

1. Home Page: As Seen\n
2. Arshan's Page: Information on Arshan\n
3. Daniel's Page: Information on Daniel\n
4. Weather Index: Give a longitude, latitude, and pick a weather criteria. The result will be the current state of that criteria at that location.\n
5. Weather Comparison: Give 2 longitudes and latitudes for two different locations. Google Gemini will compare the two and say which one is the better option based on the weather.\n

""")

