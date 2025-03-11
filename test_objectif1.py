import Projet4 
import data_processing
import distance
import unittest
import networkx as nx
import csv
import pandas as pd
from distance import distance
import time


G, edges = data_processing.data_processing("files/airports.csv", "files/pre_existing_routes.csv")

G_small, filtered_routes = data_processing.data_processing("files/test_airports.csv", "files/pre_existing_routes.csv")

def test_network():
    G_test = nx.DiGraph()
    edges = {}
    G_test.add_node("ABC")
    G_test.add_node("DEF")
    G_test.add_node("GHI")
    G_test.add_node("JKL")
    G_test.add_node("MNO")
    G_test.add_node("PQR")
    G_test.add_node("STU")
    G_test.add_node("VWX")
    G_test.add_edge("ABC", "DEF", weight=50000)
    edges[("ABC", "DEF")] = 50000
    G_test.add_edge("VWX","ABC",weight=150000)
    edges[("VWX","ABC")] = 150000
    G_test.add_edge("GHI","ABC", weight=50000)
    edges[("GHI","ABC")] = 50000
    G_test.add_edge("DEF","STU", weight=200000)
    edges[("DEF","STU")] = 200000
    G_test.add_edge("JKL","DEF" ,weight=40000)
    edges[("JKL","DEF")] = 40000
    G_test.add_edge("DEF","MNO", weight=400000)
    edges[("DEF","MNO")] = 400000
    G_test.add_edge("DEF","GHI", weight=20000)
    edges[("DEF","GHI")] = 20000
    G_test.add_edge("VWX","GHI", weight=100000)
    edges[("VWX","GHI")] = 100000
    G_test.add_edge("MNO","JKL", weight=30000)
    edges[("MNO","JKL")] = 30000
    G_test.add_edge("JKL", "PQR",weight=50000)
    edges[("JKL", "PQR")] = 50000
    G_test.add_edge("PQR","MNO", weight=100000)
    edges[("PQR","MNO")] = 100000
    G_test.add_edge("STU","PQR", weight=50000)
    edges[("STU","PQR")] = 50000
    G_test.add_edge("STU","VWX", weight=50000)
    edges[("STU","VWX")] = 50000
    G_test.add_edge("VWX","GHI", weight=100000)
    edges[("VWX","GHI")] = 100000

    return G_test, edges

G_test, edges_test = test_network()

def test_shortest():
    pairs_to_connect = [('LOS', 'BOS')]
    model = Projet4.resolution(G, pairs_to_connect, edges, 0)
    return model.obj()
cmax = 10**18
def test_shortest_cbig():
    pairs_to_connect = [('ALG', 'DXB')]
    edges[('ALG', 'DXB')] = 50000000000
    edges[('DXB', 'ALG')] = 50000000000
    model = Projet4.resolution(G, pairs_to_connect, edges,cmax)
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

def test_complex_c5():
    pairs_to_connect = [('YYZ','BKK'),('LHR','BKK')]
    model = Projet4.resolution(G_small,pairs_to_connect,filtered_routes,5000000)
    return model.obj()

def test_complex2(C=0):
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
    model = Projet4.resolution(G, list, edges, C)
    sum = 0
    for i,j in list:
        sum += nx.shortest_path_length(G, source=i, target=j,weight='weight')
    
    return model.obj(), sum/len(list)

def test_bcp(C=0):
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
    model = Projet4.resolution(G, list, edges, C)
    sum = 0
    for i,j in list:
        sum += nx.shortest_path_length(G, source=i, target=j,weight='weight')
    
    return model.obj(), sum/len(list)


def test_optimality():
    model = Projet4.resolution(G_test, [("DEF", "MNO")], edges_test, 50000)
    return model.obj()

class TestResolution(unittest.TestCase):
    def test_correcteness(self):
        start = time.time()
        self.assertAlmostEqual(test_shortest(), nx.shortest_path_length(G, source="LOS", target="BOS",weight='weight'))
        print(f"\nTest with C = 0 and 1 pair in {round(time.time()-start, 4)} seconds")       

        start = time.time()
        self.assertAlmostEqual(round(test_direct(),4), round(nx.shortest_path_length(G, source="BKK", target="ADD",weight='weight'),4)+1)
        print(f"Test with C = 1 and 1 pair in {round(time.time()-start, 4)} seconds")

        start = time.time()
        self.assertAlmostEqual(test_not_direct(), nx.shortest_path_length(G, source="LGW", target="ADD",weight='weight'))
        print(f"Test with C = 0 and 1 pair in {round(time.time()-start, 4)} seconds")

        start = time.time()
        self.assertAlmostEqual(test_shortest_cbig(), 50000000000+10**18)
        print(f"Test with C = cmax and 1 pair in {round(time.time()-start, 4)} seconds")

        start = time.time()
        self.assertAlmostEqual(test_complex_c5(), 5000000*2+9855600.810234353+14115511.52441033/2)
        print(f"Test with C = 5000000 and 2 pairs on a small graph in {round(time.time()-start, 4)} seconds")

        start = time.time()       
        self.assertEqual(test_optimality(), 450000)
        print(f"Test with C = 50000 and 1 pair in {round(time.time()-start, 4)} seconds")

        start = time.time()
        result, sum1 = test_complex2()
        self.assertAlmostEqual(result, sum1)
        print(f"Test with C = 0 and 40 pairs in {round(time.time()-start, 4)} seconds")


        start = time.time()
        result2, sum2 = test_bcp()
        self.assertAlmostEqual(result2, sum2)
        print(f"Test with C = 0 and 100 pairs in {round(time.time()-start, 4)} seconds")
        

    def test_time(self):

        start = time.time()
        g , h = test_complex2(C=100000)
        print(f"\nTest with C = 100 000 and 40 pairs in {round(time.time()-start, 4)} seconds")

        start = time.time()
        r,v = test_bcp(C=50000)
        print(f"Test with C = 10 000 and 100 pairs in {round(time.time()-start, 4)} seconds")
    
        






if __name__ == '__main__':
    unittest.main(verbosity=2)

