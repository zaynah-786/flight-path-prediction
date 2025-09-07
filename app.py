
import math

# talib said this is the earth's radius
earth_radius_km = 6378.0

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
