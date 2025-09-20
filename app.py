import math
import streamlit as st
import airportsdata # library for airport data (specifically need IATA codes)

@st.cache_data
def load_airports_data():
    return airportsdata.load('IATA')

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
def havershine_formula(latitude1, longitude1, latitude2, longitude2):
# converting from degrees to radians
    lat1rad = math.radians(latitude1)
    lat2rad = math.radians(latitude2)
    long1rad = math.radians(longitude1)
    long2rad = math.radians(longitude2)

    change_in_lat = lat2rad - lat1rad
    change_in_long = long2rad - long1rad

# havershine formula 
    a = math.sin(change_in_lat / 2)**2 + (math.cos(lat1rad) * math.cos(lat2rad)) * math.sin(change_in_long / 2)**2

# central angle between the two points on the surface of the earth
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
 
# distance
    distance = earth_radius_km * c
    return distance

# function to calc flight time in hours 
def flight_time(distance, speed):
    """Return flight time in hours given distance (km) and speed (km/h)."""
    return distance / speed

airports = load_airports_data()

# Create a clean and searchable list of airport options
airport_options = []
for iata, data in airports.items():
    city = data.get('city')
    country = data.get('country')
    airport_name = data['name']
    
    if city:
        display_string = f"{iata} - {airport_name} ({city}, {country})"
    else:
        display_string = f"{iata} - {airport_name} ({country})"
    
    airport_options.append(display_string)

airport_options.sort()

# user inputs using st.selectbox for search functionality
dep_full_name = st.selectbox(
    "choose departure airport", 
    airport_options, 
    index=None, 
    placeholder="Search for an airport (e.g., LHR, London, Heathrow)"
)
arr_full_name = st.selectbox(
    "choose arrival airport", 
    airport_options, 
    index=None, 
    placeholder="Search for an airport (e.g., JFK, New York, Kennedy)"
)

# check if code exists in airports data library or not
if dep_full_name and arr_full_name:
    dep = dep_full_name.split(' - ')[0]
    arr = arr_full_name.split(' - ')[0]

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
else:
    st.write("Please select both a departure and arrival airport.")