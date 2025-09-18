import math
import streamlit as st
import airportsdata # library for airpoty data (specifically need IATA codes)

# talib said this is the earth's radius
earth_radius_km = 6378.0

# cruising speeds i found on a pic in km/h
PLANES = {
    "boeing 737":  {"cruise": (567*1.609, 606*1.609)},  
    "boeing 777":  {"cruise": 644*1.609},
    "boeing 787":  {"cruise": 652*1.609},
    "airbus a380": {"cruise": 561*1.609},
    "airbus a350": {"cruise": 561*1.609},
    "airbus a320": {"cruise": 598*1.609},
    "embraer e175": {"cruise": 515*1.609},
    "bombardier crj900": {"cruise": 516*1.609}
}

# latitude and longitude in degrees
def havershine_formula (latitude1, longitude1, latitude2, longitude2):
# converting from degrees to radians
    lat1rad = math.radians(latitude1)
    lat2rad = math.radians(latitude2)
    long1rad = math.radians(longitude1)
    long2rad = math.radians(longitude2)

    change_in_lat = lat2rad - lat1rad
    change_in_long = long2rad - long1rad

# havershine formula 
    a = math.sin(change_in_lat/2)**2 + (math.cos(lat1rad)*math.cos(lat2rad)) * math.sin(change_in_long/2)**2

# central angle between the two points on the surface of the earth
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
 
# distance
    distance = earth_radius_km*c
    return distance

# function to calc flight time in hours 
def flight_time(distance, speed):
    """Return flight time in hours given distance (km) and speed (km/h)."""
    return distance / speed


# load airport data
airports = airportsdata.load('IATA')

# user inputs 
dep = st.text_input("enter departure airport code (IATA, e.g. JFK)", "JFK").upper()
arr = st.text_input("enter arrival airport code (IATA, e.g. LHR)", "LHR").upper()

# check if code exists in airports data library or not
if dep not in airports or arr not in airports:
    st.write("one or both airport codes not found in database.")
else:
# get lat and lon for both aiports
    lat1, lon1 = airports[dep]['lat'], airports[dep]['lon']
    lat2, lon2 = airports[arr]['lat'], airports[arr]['lon']

# display planes and allow user to choose
    plane_name = st.selectbox("choose a plane", list(PLANES.keys()))

# get selected plane and cruise speed
    cruise = PLANES[plane_name]["cruise"]
# calculating avg speed
    if isinstance(cruise, tuple):
        avg_speed = sum(cruise) / 2
        plane_speed = avg_speed
        st.write(f"using average cruise speed: {avg_speed:.1f} km/h (range {cruise[0]:.0f}–{cruise[1]:.0f})")
    else:
        plane_speed = cruise

# calculate greatest circle distance + flight time
    distance = havershine_formula(lat1, lon1, lat2, lon2)
    time_hours = flight_time(distance, plane_speed)
    
    st.write(f"departure: {dep} - {airports[dep]['name']}, {airports[dep]['country']}")
    st.write(f"arrival:   {arr} - {airports[arr]['name']}, {airports[arr]['country']}")
    st.write(f"great-circle distance: {distance:.2f} km")
    st.write(f"estimated flight time: {time_hours:.2f} hours at {plane_speed:.0f} km/h")
