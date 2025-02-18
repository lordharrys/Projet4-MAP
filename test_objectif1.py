import Projet4 
import distance
import unittest
import networkx as nx

def test_shortest():
    pairs_to_connect = [('LOS', 'BOS')]
    model = Projet4.resolution(Projet4.G, pairs_to_connect, Projet4.edges, 0)
    return model.obj()

def test_direct():
    pairs_to_connect = [('BKK','ADD')]

    model = Projet4.resolution(Projet4.G, pairs_to_connect, Projet4.edges, 1)
    return model.obj()

def test_not_direct():
    pairs_to_connect = [('LGW','ADD')]
    model = Projet4.resolution(Projet4.G, pairs_to_connect, Projet4.edges, 0)
    return model.obj()

def test_complex():
    pairs_to_connect = [('LOS', 'BOS'), ('BKK','ADD'), ('LGW','ADD'), ('BKK','LOS'), ('LGW','BOS'), ('LGW','LOS'), ('BKK','BOS'), ('BKK','LGW'), ('LOS','ADD'), ('BOS','ADD')]
    model = Projet4.resolution(Projet4.G, pairs_to_connect, Projet4.edges, 0)    
    return model.obj()

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
    model = Projet4.resolution(Projet4.G, list, Projet4.edges, 0)
    sum = 0
    for i,j in list:
        sum += nx.shortest_path_length(Projet4.G, source=i, target=j,weight='weight')
    
    return model.obj(), sum/len(list)





class TestResolution(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(round(test_shortest(),4), round(nx.shortest_path_length(Projet4.G, source="LOS", target="BOS",weight='weight'),4))
        self.assertEqual(round(test_direct(),4), round(nx.shortest_path_length(Projet4.G, source="BKK", target="ADD",weight='weight'),4)+1)
        self.assertEqual(round(test_not_direct(),4), round(nx.shortest_path_length(Projet4.G, source="LGW", target="ADD",weight='weight'),4))
    
    
    def test_multiple_pairs(self):
        pairs_to_connect = [('LOS', 'BOS'), ('BKK','ADD'), ('LGW','ADD'), ('BKK','LOS'), ('LGW','BOS'), ('LGW','LOS'), ('BKK','BOS'), ('BKK','LGW'), ('LOS','ADD'), ('BOS','ADD')]
        sum = 0
        for i,j in pairs_to_connect:
            sum += nx.shortest_path_length(Projet4.G, source=i, target=j,weight='weight')
        
        self.assertEqual(round(test_complex(),4), round(sum/len(pairs_to_connect),4))

        result, sum1 = test_complex2()
        self.assertEqual(round(result,4), round(sum1,4))




if __name__ == '__main__':
    unittest.main(verbosity=2)

