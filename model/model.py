from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self.listaAvvistamenti = []
        self.loadAvvistamenti()
        self.listaStati = []
        self.loadStati()
        self._grafo = nx.Graph()
        self._nodes = []
        self._edges = []

    def loadAvvistamenti(self):
        self.listaAvvistamenti = DAO.getAllAvvistamento()

    def getAvvistamenti(self):
        return self.listaAvvistamenti

    def loadStati(self):
        self.listaStati = DAO.getAllState()

    # c. Facendo click sul bottone CREA GRAFO, creare un grafo semplice, pesato e non orientato, i cui vertici siano
    # tutti gli stati presenti nella tabella “state”. Un arco collega due stati solo se sono confinanti, come indicato
    # nella tabella “neighbor”.
    # d. Il peso dell’arco viene calcolato come il numero di avvistamenti che hanno la stessa forma (colonna “shape”)
    # selezionata dal menù a tendina Forma, e che si sono verificati nello stesso anno selezionato (da estrarre dalla
    # colonna “datetime”), nei due stati considerati.
    # e. Stampare per ogni stato la somma dei pesi degli archi adiacenti.

    def buildGraph(self, shape, year):
        self._grafo.clear()
        for stato in self.listaStati:
            self._nodes.append(stato)


        self._grafo.add_nodes_from(self._nodes)
        self.idMap = {}

        for n in self._nodes:
            self.idMap[n.id] = n

        listaArchi = DAO.cercaArchi(shape, year)
        for arco in listaArchi:
            self._grafo.add_edge(self.idMap[arco[0]], self.idMap[arco[1]], weight=arco[2])

    def getListaPesiAdiacentiPerStato(self):
        listaPesiAdiacenti = []
        for stato in self._grafo.nodes:
            somma = 0
            for edge in self._grafo.edges(stato, data=True):
                somma += edge[2]["weight"]
            listaPesiAdiacenti.append((stato, somma))
        return listaPesiAdiacenti
    def get_nodes(self):
        return self._grafo.nodes()

    def get_edges(self):
        return list(self._grafo.edges(data=True))


    def get_num_of_nodes(self):
        return self._grafo.number_of_nodes()


    def get_num_of_edges(self):
        return self._grafo.number_of_edges()


    def get_sorted_edges(self):
        return sorted(self._grafo.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)
