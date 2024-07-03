CREAZIONE GRAFO

CONTROLLER

self._model.buildGraph(s, a)
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {self._model.get_num_of_nodes()} Numero di archi: {self._model.get_num_of_edges()}"))


        for p in self._model.get_sum_weight_per_node():
             self._view.txt_result.controls.append(ft.Text(f"Nodo {p[0]}, somma pesi su archi ={p[1]}"))

        self._view.update_page()



MODEL
IMPORT:
import networkx as nx

INIZIO:
self._grafo = nx.Graph()
self._nodes = []
self._edges = []

FUNZIONE CHE CREA IL GRAFO
 def buildGraph(self, c, a):
        self._grafo.clear()
        #CONDIZIONI
        self._nodes.append(NODO)

        self._grafo.add_nodes_from(self._nodes)
        self.idMap = {}
        for n in self._nodes:
            self.idMap[n.(ID)] = n

#CONDIZIONI TRA NODI SU SQL MA CREAZIONE ARCHI IN MODEL
        self._grafo.add_edge(n1, n2, weight=???)
#ALTRIMENTI ESTRAI IN SQL LE CONDIZIONI E GLI ARCHI E POI USI:
        self._grafo.add_weighted_edges_from(self.edges)


ALTRE FUNZIONI UTILI
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


ESPLORAZIONE GRAFO

INDIVIDUO NODO DI PARTENZA


def searchPath(self, ID):
    nodoSource = self.idMap[ID]  # individuato nodo di partenza

    parziale = []  # lista momentanea

    self.ricorsione(parziale, nodoSource, 0)  # inizio la ricorsione


RICORSIONE PER CAMMINO MASSIMO


def ricorsione(self, parziale, nodoLast, livello):
    archiViciniAmmissibili = self.getArchiViciniAmm(nodoLast, parziale)
    # SE IL NODO NON HA ALTRI ARCHI VICINI VERIFICO LA SOLUZIONE
    if len(archiViciniAmmissibili) == 0:
        if len(parziale) > len(self._solBest):
            self._solBest = list(parziale)
    # AGGIUNGO EVENTUALI ALTRI ARCHI VICINI E RICOMINCIO
    for a in archiViciniAmmissibili:
        parziale.append(a)
        self.ricorsione(parziale, a[1], livello + 1)
        parziale.pop()  #####


PRENDO ARCHI VICINI


def getArchiViciniAmm(self, nodoLast, parziale):
    archiVicini = self._grafo.edges(nodoLast, data=True)
    result = []
    for a1 in archiVicini:
        if self.isAscendent(a1, parziale) and self.isNovel(a1, parziale):
            result.append(a1)
    return result


FUNZIONE CHE CAPISCE SE IL PESO DELL'ARCO CONSIDERATO E' >= AI PRECEDENTI

def isAscendent(self, e, parziale):
    if len(parziale) == 0:
        return True
    return e[2]["weight"] >= parziale[-1][2]["weight"]  # True se è così, False altrimenti



FUNZIONE CHE CONTROLLA SE L'ARCO E' NUOVO NEL parziale[]
def isNovel(self, arco, parziale):
    if len(parziale) == 0:
        return True
    arco_inv = (arco[1], arco[0], arco[2])  # controllo anche l'arco invertito
    return (arco_inv not in parziale) and (arco not in parziale)  # True se entrambi non sono nel parziale[]

