
import math

def distance(lat1, lat2, lon1, lon2):
   
    R = 6378137.0
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    distance = R * math.acos(math.sin(lat1_rad) * math.sin(lat2_rad) +
                             math.cos(lat1_rad) * math.cos(lat2_rad) * math.cos(lon2_rad - lon1_rad))
    return distance

lat1, lon1 = 51.5074, -0.1278  # Londres
lat2, lon2 = 40.7128, -74.0060  # New York

result = distance(lat1, lat2, lon1, lon2)
print(result)


    
