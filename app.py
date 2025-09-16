
import math
import streamlit as st
import airportsdata

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

def flight_time(distance, speed):
    """Return flight time in hours given distance (km) and speed (km/h)."""
    return distance / speed

if __name__ == "__main__":
    print("flight path prediction")

    airports = airportsdata.load('IATA')

    dep = input("\nenter departure airport code (IATA, e.g. JFK): ").upper()
    arr = input("enter arrival airport code (IATA, e.g. LHR): ").upper()

    if dep not in airports or arr not in airports:
        print("one or both airport codes not found in database.")
        exit()

    lat1, lon1 = airports[dep]['lat'], airports[dep]['lon']
    lat2, lon2 = airports[arr]['lat'], airports[arr]['lon']

    print("\navailable planes:")
    for i, plane in enumerate(PLANES.keys(), 1):
        print(f"{i}. {plane}")
    choice = int(input("\nchoose a plane (number): "))

    plane_name = list(PLANES.keys())[choice-1]
    cruise = PLANES[plane_name]["cruise"]

    if isinstance(cruise, tuple):
        avg_speed = sum(cruise) / 2
        plane_speed = avg_speed
        print(f"\nusing average cruise speed: {avg_speed:.1f} km/h (range {cruise[0]:.0f}–{cruise[1]:.0f})")
    else:
        plane_speed = cruise

    distance = havershine_formula(lat1, lon1, lat2, lon2)
    time_hours = flight_time(distance, plane_speed)

    print(f"\ndeparture: {dep} - {airports[dep]['name']}, {airports[dep]['country']}")
    print(f"arrival:   {arr} - {airports[arr]['name']}, {airports[arr]['country']}")
    print(f"great-circle distance: {distance:.2f} km")
    print(f"estimated flight time: {time_hours:.2f} hours at {plane_speed:.0f} km/h")
