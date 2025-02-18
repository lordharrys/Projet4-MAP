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



class TestResolution(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(round(test_shortest(),4), round(nx.shortest_path_length(Projet4.G, source="LOS", target="BOS",weight='weight'),4))
        self.assertEqual(round(test_direct(),4), round(nx.shortest_path_length(Projet4.G, source="BKK", target="ADD",weight='weight'),4)+1)
        self.assertEqual(round(test_not_direct(),4), round(nx.shortest_path_length(Projet4.G, source="LGW", target="ADD",weight='weight'),4))




if __name__ == '__main__':
    unittest.main(verbosity=2)

