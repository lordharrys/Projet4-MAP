import Projet4 
import data_preprocessing
import distance
import unittest
import networkx as nx
import csv
import pandas as pd
from distance import distance

G_small = nx.DiGraph()
G, edges = data_preprocessing.data_processing("files/airports.csv", "files/routes.csv")

airports_random = [
    {"ID": "YYZ", "name": "Lester B. Pearson International Airport", "city": "Toronto", "country": "Canada", "latitude": 43.6772003174, "longitude": -79.6305999756},
    {"ID": "ALG", "name": "Houari Boumediene Airport", "city": "Algier", "country": "Algeria", "latitude": 36.691001892089844, "longitude": 3.215409994125366},
    {"ID": "DXB", "name": "Dubai International Airport", "city": "Dubai", "country": "United Arab Emirates", "latitude": 25.2527999878, "longitude": 55.3643989563},
    {"ID": "LHR", "name": "London Heathrow Airport", "city": "London", "country": "United Kingdom", "latitude": 51.4706, "longitude": -0.461941},
    {"ID": "BKK", "name": "Suvarnabhumi Airport", "city": "Bangkok", "country": "Thailand", "latitude": 13.681099891662598, "longitude": 100.74700164794922},
    {"ID": "MEX", "name": "Licenciado Benito Juarez International Airport", "city": "Mexico City", "country": "Mexico", "latitude": 19.4363, "longitude": -99.072098},
    {"ID": "SYD", "name": "Sydney Kingsford Smith International Airport", "city": "Sydney", "country": "Australia", "latitude": -33.94609832763672, "longitude": 151.177001953125},
    {"ID": "JNB", "name": "OR Tambo International Airport", "city": "Johannesburg", "country": "South Africa", "latitude": -26.1392, "longitude": 28.246},
    {"ID": "SFO", "name": "San Francisco International Airport", "city": "San Francisco", "country": "United States", "latitude": 37.61899948120117, "longitude": -122.375},
    {"ID": "ICN", "name": "Incheon International Airport", "city": "Seoul", "country": "South Korea", "latitude": 37.46910095214844, "longitude": 126.45099639892578}
]

for airport in airports_random:
    G_small.add_node(airport["ID"], name=airport["name"], city=airport["city"], country=airport["country"], latitude=airport["latitude"], longitude=airport["longitude"])

# List of airport IDs from airports_random
airport_ids = {"YYZ", "ALG", "DXB", "LHR", "BKK", "MEX", "SYD", "JNB", "SFO", "ICN"}

df = pd.read_csv("files/pre_existing_routes.csv")


# Convert the filtered DataFrame to a list of dictionaries
filtered_routes = {}

for _,route in df.iterrows():
    start, end = route["ID_start"], route["ID_end"]
    if start in G_small.nodes and end in G_small.nodes:
        lat1 = G_small.nodes[start]["latitude"]
        lon1 = G_small.nodes[start]["longitude"]
        lat2 = G_small.nodes[end]["latitude"]
        lon2 = G_small.nodes[end]["longitude"]
        dist = distance(lat1, lon1, lat2, lon2)
        G_small.add_edge(start, end, weight=dist)
        filtered_routes[(start, end)] = dist  


def test_shortest():
    pairs_to_connect = [('LOS', 'BOS')]
    model = Projet4.resolution(G, pairs_to_connect, edges, 0)
    return model.obj()

def test_shortest_cbig():
    pairs_to_connect = [('ALG', 'DXB')]
    filtered_routes[('ALG', 'DXB')] = 50000000000
    filtered_routes[('DXB', 'ALG')] = 50000000000
    model = Projet4.resolution(G_small, pairs_to_connect, filtered_routes, 100000000000)
    return model.obj()

def test_direct():
    pairs_to_connect = [('BKK','ADD')]

    model = Projet4.resolution(G, pairs_to_connect, edges, 1)
    
    return model.obj()

def test_not_direct():
    pairs_to_connect = [('LGW','ADD')]
    model = Projet4.resolution(G, pairs_to_connect, edges, 0)
    return model.obj()

def test_complex():
    pairs_to_connect = [('LOS', 'BOS'), ('BKK','ADD'), ('LGW','ADD'), ('BKK','LOS'), ('LGW','BOS'), ('LGW','LOS'), ('BKK','BOS'), ('BKK','LGW'), ('LOS','ADD'), ('BOS','ADD')]
    model = Projet4.resolution(G, pairs_to_connect, edges, 0)    
    return model.obj()

# def test_complex_c5():
#     pairs_to_connect = [('LOS', 'BOS'), ('BKK','ADD'), ('LGW','ADD'), ('BKK','LOS'), ('LGW','BOS'), ('LGW','LOS'), ('BKK','BOS'), ('BKK','LGW'), ('LOS','ADD'), ('BOS','ADD')]
#     model = Projet4.resolution(G, pairs_to_connect, edges, 5)    
#     return model.obj()

def test_complex2():
    # Liste aléatoire de 40 aéroports générée par une IA
    list = [
    ('ADD', 'LOS'), ('HKG', 'SVO'), ('SZX', 'SDU'), ('IAH', 'BOM'),
    ('DMK', 'SGN'), ('SVO', 'SCL'), ('KMG', 'JFK'), ('SYD', 'BOS'),
    ('YYZ', 'GRU'), ('KUL', 'SIN'), ('LOS', 'CKG'), ('LHR', 'EWR'),
    ('PVG', 'LAS'), ('ICN', 'MIA'), ('HND', 'AKL'), ('HGH', 'MAD'),
    ('CGK', 'LOS'), ('PHX', 'SDU'), ('CAN', 'MEL'), ('DEL', 'MNL'),
    ('CGK', 'SIN'), ('DEL', 'JNB'), ('HND', 'BOG'), ('SFO', 'KUL'),
    ('CBR', 'DEN'), ('HRG', 'DFW'), ('CDG', 'SGN'), ('BOG', 'IAH'),
    ('HGH', 'CLT'), ('LAX', 'YYZ'), ('FRA', 'HND'), ('SYD', 'ICN'),
    ('CBR', 'LOS'), ('MCO', 'SHA'), ('AMS', 'MEX'), ('JNB', 'HGH'),
    ('BSB', 'TPE'), ('SHA', 'PVG'), ('BSB', 'IAH'), ('ADL', 'HND')
    ]
    model = Projet4.resolution(G, list, edges, 0)
    sum = 0
    for i,j in list:
        sum += nx.shortest_path_length(G, source=i, target=j,weight='weight')
    
    return model.obj(), sum/len(list)

def test_bcp():
    list = [('DEN', 'CDG'), ('SHA', 'DEN'), ('MNL', 'PEK'), ('EZE', 'SYD'), ('LHR', 'AKL'),
    ('EZE', 'SZX'), ('IAH', 'MEL'), ('BCN', 'CGK'), ('XIY', 'SHA'), ('AKL', 'SYD'),
    ('AKL', 'CAN'), ('MEX', 'HGH'), ('MCO', 'BOG'), ('EWR', 'JED'), ('CKG', 'ADD'),
    ('MEX', 'BKK'), ('HKG', 'BKK'), ('KMG', 'ADD'), ('CGK', 'SYD'), ('IST', 'BOG'),
    ('CBR', 'MIA'), ('SDU', 'PVG'), ('SFO', 'PEK'), ('SIN', 'JFK'), ('HRG', 'CMN'),
    ('EWR', 'YYZ'), ('LAX', 'BSB'), ('BCN', 'BOM'), ('ORD', 'CAI'), ('MEX', 'DEL'),
    ('CMN', 'PEK'), ('FRA', 'DXB'), ('NBO', 'LIM'), ('LOS', 'DFW'), ('IST', 'ICN'),
    ('DFW', 'BSB'), ('HKG', 'BOM'), ('EWR', 'CLT'), ('BCN', 'ALG'), ('ATL', 'YYZ'),
    ('SGN', 'ORD'), ('CPT', 'BCN'), ('SCL', 'MEX'), ('MEX', 'LGW'), ('CMN', 'CAI'),
    ('HKG', 'IAH'), ('DFW', 'DXB'), ('AMS', 'XIY'), ('LGW', 'BOS'), ('KMG', 'PEK'),
    ('LOS', 'DEL'), ('LHR', 'ATL'), ('SGN', 'MIA'), ('ADD', 'ALG'), ('CGK', 'DFW'),
    ('ADL', 'LAX'), ('IST', 'PVG'), ('LHR', 'CDG'), ('EWR', 'MIA'), ('KMG', 'FRA'),
    ('SFO', 'DMK'), ('ICN', 'HRG'), ('BKK', 'KMG'), ('MEL', 'SEA'), ('CMN', 'SDU'),
    ('CAI', 'PEK'), ('LAX', 'CMN'), ('LGW', 'DOH'), ('AKL', 'SDU'), ('DEL', 'LGW'),
    ('LGW', 'ICN'), ('IAH', 'PHX'), ('MEX', 'ADD'), ('MAD', 'LAX'), ('CLO', 'LOS'),
    ('IAH', 'SHA'), ('DXB', 'MNL'), ('CGK', 'CPT'), ('SZX', 'XIY'), ('FRA', 'ORD'),
    ('LGW', 'IAH'), ('LIM', 'LGW'), ('MCO', 'JED'), ('SGN', 'HND'), ('BOG', 'MEX'),
    ('FRA', 'JFK'), ('CDG', 'CAI'), ('BSB', 'SCL'), ('SEA', 'HGH'), ('CPT', 'SDU'),
    ('ATL', 'LGW'), ('NBO', 'LHR'), ('BKK', 'MCO'), ('IAH', 'CDG'), ('TPE', 'MIA'),
    ('CAN', 'MEX'), ('EZE', 'HGH'), ('BOG', 'YYZ'), ('KMG', 'DFW'), ('DEL', 'LAX')
    ]
    model = Projet4.resolution(G, list, edges, 0)
    sum = 0
    for i,j in list:
        sum += nx.shortest_path_length(G, source=i, target=j,weight='weight')
    
    return model.obj(), sum/len(list)



class TestResolution(unittest.TestCase):
    def test_simple(self):
        #self.assertEqual(round(test_shortest(),4), round(nx.shortest_path_length(G, source="LOS", target="BOS",weight='weight'),4))
        print(f"\nError of the test with C = 0 and 1 pair : {abs(test_shortest() - nx.shortest_path_length(G, source='LOS', target='BOS',weight='weight'))}")
        #self.assertEqual(round(test_direct(),4), round(nx.shortest_path_length(G, source="BKK", target="ADD",weight='weight'),4)+1)
        print(f"Error of the test with C = 1 and 1 pair : {abs(test_direct() - nx.shortest_path_length(G, source='BKK', target='ADD',weight='weight')-1)}")
        #self.assertEqual(round(test_not_direct(),4), round(nx.shortest_path_length(G, source="LGW", target="ADD",weight='weight'),4))
        print(f"Error of the test with C = 0 and 1 pair : {abs(test_not_direct() - nx.shortest_path_length(G, source='LGW', target='ADD',weight='weight'))}")
        #self.assertEqual(round(test_shortest_c1000000000(),4), round(50000000000),4))
        print(f"Error of the test with C = 100000000000 and 1 pair : {abs(test_shortest_cbig() -50000000000- 100000000000)}")
    
    
    def test_multiple_pairs(self):
        pairs_to_connect = [('LOS', 'BOS'), ('BKK','ADD'), ('LGW','ADD'), ('BKK','LOS'), ('LGW','BOS'), ('LGW','LOS'), ('BKK','BOS'), ('BKK','LGW'), ('LOS','ADD'), ('BOS','ADD')]
        sum = 0
        for i,j in pairs_to_connect:
            sum += nx.shortest_path_length(G, source=i, target=j,weight='weight')
        
        #self.assertEqual(round(test_complex(),4), round(sum/len(pairs_to_connect),4))
        print(f"\nError of the test with C = 0 and 1 pair : {test_complex() - sum/len(pairs_to_connect)}")

        result, sum1 = test_complex2()
        #self.assertEqual(round(result,4), round(sum1,4))
        print(f"Error of the test with C = 0 and 40 pairs : {result - sum1}")

        result2, sum2 = test_bcp()
        print(f"Error of the test with C = 0 and 100 pairs : {result2 - sum2}")




if __name__ == '__main__':
    unittest.main(verbosity=2)

