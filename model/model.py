from database.DAO import DAO
import networkx as nx
from geopy import distance

class Model:
    def __init__(self):
        self.pesoTotPercorso = 0
        self.solBest = []
        self.distanzaBest = 0
        self.nodes = []
        self.idMap = {}
        self.edges = []
        self.graph = nx.Graph()
        self.listSighting = []
        self.loadSighting()
        self.listStates = []
        self.loadStates()
        self.listStatesByYandS = []

    def loadSighting(self):
        self.listSighting = DAO.getAllSighting()

    def loadStates(self):
        self.listStates = DAO.getAllStates()

    def getYears(self):
        result = []
        for s in self.listSighting:
            if s.datetime.year not in result:
                result.append(s.datetime.year)
        return sorted(result)

    def getShape(self, year):
        result = []
        for s in self.listSighting:
            if s.datetime.year == year and s.shape not in result:
                result.append(s.shape)
        return sorted(result)

    # SEMPLICE, PESATO, NON ORIENTATO, VERTICI = STATI,
    # ARCO TRA 2 STATI CONFINANTI, PESO = NUMERO DI AVVISTAMENTI CON FORMA S E ANNO Y NEI 2 STATI
    def buildgraph(self, y, s):

        for state in self.listStates:
            if state not in self.nodes:
                self.nodes.append(state)

        self.graph.add_nodes_from(self.nodes)

        for n in self.nodes:
            self.idMap[n._id] = n

        self.edges = DAO.cercaArchi() # me li da solo come id

        for edge in self.edges:
            peso = self.contaAvvistamentiStato(edge[0]) + self.contaAvvistamentiStato(edge[1])
            self.graph.add_edge(self.idMap[edge[0]], self.idMap[edge[1]], weight=peso)

    def loadStatesByYandS(self, y, s):
        self.listStatesByYandS = DAO.getStatesByYandS(y, s)

    def contaAvvistamentiStato(self, state_id):
        contatore = 0
        for s in self.listStatesByYandS:
            if s._id == state_id:
                contatore += 1
        return contatore

    def sommaPesiArchiAdiacenti(self, nStart):
        somma = 0
        for nNext in self.graph.neighbors(nStart):
            somma += self.graph[nStart][nNext]['weight']
        return somma

    def get_nodes(self):
        return self.graph.nodes()

    def get_edges(self):
        return list(self.graph.edges(data=True))

    def get_num_of_nodes(self):
        return self.graph.number_of_nodes()

    def get_num_of_edges(self):
        return self.graph.number_of_edges()

    def get_sorted_edges(self):
        return sorted(self.graph.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)

    def getNumConfinanti(self, v):
        return len(list(self.graph.neighbors(v)))

    def getNumCompConnesse(self):
        return nx.number_connected_components(self.graph)

    def calcolaPercorso(self):
        self.pesoTotPercorso = 0
        self.solBest = []
        self.distanzaBest = 0
        for node in self.get_nodes():
            self.ricorsione(node, [], 0)
        self.calcolaPesoTotPercorso(self.solBest)

    # CAMMINO SEMPLICE CON PESO CRESCENTE CHE MASSIMIZZA DISTANZA TRA STATI
    def ricorsione(self, nStart, parziale, pesoPrec):

        archiAmm = self.cercaArchiAmm(nStart, parziale, pesoPrec)

        if archiAmm == []:
            distanzaParziale = self.calcolaDistanza(parziale)
            if distanzaParziale > self.distanzaBest:
                self.distanzaBest = distanzaParziale
                self.solBest = list(parziale)
            return

        for arco in archiAmm:
            nNext = arco[1]
            pesoAttuale = self.graph[nStart][nNext]['weight']
            parziale.append(arco)
            self.ricorsione(nNext, parziale, pesoAttuale)
            parziale.pop()



    def calcolaDistanza(self, listaArchi):
        distanza = 0
        for arco in listaArchi:
            nodo1 = arco[0]
            nodo2 = arco[1]
            distanza += distance.geodesic((nodo1.lat, nodo1.lng), (nodo2.lat, nodo2.lng)).km
        return distanza

    def cercaArchiAmm(self, nStart, parziale, pesoPrec):
        risultato = []
        for nVicino in self.graph.neighbors(nStart):
            if (nStart, nVicino) not in parziale and (nVicino, nStart) not in parziale:
                pesoArcoTemp = self.graph[nStart][nVicino]['weight']
                if pesoArcoTemp > pesoPrec:
                    risultato.append((nStart,nVicino))
        return risultato

    def calcolaDistanzaTraNodi(self, nodo1, nodo2):
        return distance.geodesic((nodo1.lat, nodo1.lng), (nodo2.lat, nodo2.lng)).km

    def calcolaPesoTotPercorso(self, percorso):
        peso = 0
        for arco in percorso:
            peso += self.graph[arco[0]][arco[1]]['weight']
        self.pesoTotPercorso = peso