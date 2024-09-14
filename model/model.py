import copy

from database.DAO import DAO
import networkx as nx
from geopy import distance



class Model:
    def __init__(self):
        self.listAvvistamenti = DAO.getAllSighting()
        self.confini = DAO.getAllConfine() # (stateID1, stateID2)


        self._grafo = nx.Graph()
        self.nodes = []
        self.edges = []
        self.idMap = {}

        self.solBest = []
        self.maxDistanza = 0

        self.solBest2 = []
        self.maxPeso2 = 0
        self.origine2 = None

        self.solBest3 = []
        self.maxPeso3 = 0

        self.solBest4 = []

        self.solBest5 = []

        self.solBest6 = []

        self.bestSet = set()

    def buildGrafo(self, year, shape):
        self._grafo.clear()
        self.nodes = DAO.getAllStates()
        for node in self.nodes:
            self.idMap[node._id] = node
        self._grafo.add_nodes_from(self.nodes)
        self.edges = DAO.gettAllEdge(year, shape)
        for node1ID, node2ID, peso in self.edges:
            self._grafo.add_edge(self.idMap[node1ID],self.idMap[node2ID], weight=peso)

    # Crea un grafo non orientato e non pesato in cui:
    # I nodi sono gli stati degli USA.
    # Un arco esiste tra due stati se un avvistamento di UFO è stato registrato in entrambi nello stesso giorno.
    # Il grafo deve essere costruito con gli avvistamenti filtrati dall'anno e dalla forma selezionati.
    def buildGrafo2(self, year, shape):
        self._grafo.clear()
        self.idMap = {}
        self.nodes = []
        self.edges = []
        self.nodes = DAO.getAllStates()
        for node in self.nodes:
            self.idMap[node._id] = node
        self._grafo.add_nodes_from(self.nodes)
        print(self.get_num_of_nodes())
        for node1ID, node2ID in DAO.getAllEdge2(year, shape):
            self.edges.append((self.idMap[node1ID], self.idMap[node2ID]))
        self._grafo.add_edges_from(self.edges)
        print(self.get_num_of_edges())
        i = 0
        for edge in self.get_edges():
            i += 1
            print(i, edge[0], edge[1])

    # Costruisci il grafo considerando solo gli avvistamenti nello stato e nel range di durata selezionati.
    # Crea un grafo orientato e pesato in cui:
    # I nodi sono gli avvistamenti di UFO (basati sulla tabella sighting).
    # Un arco esiste tra due avvistamenti se sono avvenuti nello stesso stato e il primo ha una durata inferiore rispetto al secondo, la direzione
    # sarà entrante nel nodo con durata maggiore
    # Il peso dell'arco è dato dalla differenza di durata tra i due avvistamenti.

    def buildGrafo3(self, stateName, year, durataMax):
        self._grafo.clear()
        self.idMap = {}
        self.nodes = []
        self.edges = []
        self.nodes = self.cercaNodi3(stateName, year, durataMax)
        for node in self.nodes:
            self.idMap[node.id] = node
        self._grafo.add_nodes_from(self.nodes)
        self.edges = self.cercaArchi3()
        for node1, node2, peso in self.edges:
            self._grafo.add_edge(node1, node2, weight=peso)
        print(self.get_num_of_nodes())
        print(self.get_num_of_edges())
        for edge in self.get_edges():
            print(edge[0].city, edge[0].datetime, "->", edge[1].city, edge[1].datetime, self._grafo[edge[0]][edge[1]]['weight'])

    def cercaArchi3(self):
        result = []
        for node1 in self.nodes:
            for node2 in self.nodes:
                if node1.id != node2.id:
                    if (node1,node2) not in result and (node2, node1) not in result:
                        if float(node1.duration) < float(node2.duration):
                            result.append((node1, node2, float(node2.duration)-float(node1.duration)))
        return result

    def cercaNodi3(self, stateName, year, durataMax):
        nodi = []
        stateID = self.traduttoreNomeIDStato(stateName)
        for a in self.listAvvistamenti:
            if float(a.duration) < int(durataMax) and a.state.upper() == stateID and int(a.datetime.year) == int(year):
                nodi.append(a)
        return nodi

    def traduttoreNomeIDStato(self, statoName):
        id = None
        for s in DAO.getAllStates():
            if s._Name == statoName:
                id = s._id
        return id

    # I nodi sono gli avvistamenti di UFO.
    # Un arco esiste tra due avvistamenti se sono avvenuti nello stesso stato e l'avvistamento iniziale è accaduto
    # prima del successivo (ordine temporale basato su datetime).
    # Il grafo sarà costruito solo con avvistamenti nell'intervallo temporale e nello stato scelto.

    def buildGrafo4(self, anno, s, m1, m2):
        self._grafo.clear()
        self.idMap = {}
        self.nodes = []
        self.edges = []
        self.nodes = self.cercaNodi4(anno, s, m1, m2)
        for node in self.nodes:
            self.idMap[node.id] = node
        self._grafo.add_nodes_from(self.nodes)
        print(self.get_num_of_nodes())
        self.edges = self.cercaArchi4()
        self._grafo.add_edges_from(self.edges)
        print(self.get_num_of_edges())

    def cercaNodi4(self, anno, stateName, m1, m2):
        nodi = []
        stateID = self.traduttoreNomeIDStato(stateName)
        for a in self.listAvvistamenti:
            if int(a.datetime.year) == int(anno):
                if a.state.upper() == stateID.upper() and int(m1) <= int(a.datetime.month) <= int(m2):
                    nodi.append(a)
        return nodi

    def cercaArchi4(self):
        archi = []
        for node1 in self.get_nodes():
            for node2 in self.get_nodes():
                if node1.id != node2.id:
                    if (node1, node2) not in archi and (node2, node1) not in archi:
                        if node1.datetime <= node2.datetime:
                            archi.append((node1, node2))
        return archi

    # Crea un grafo non orientato e pesato in cui:
    # I nodi sono gli stati degli USA.
    # Un arco esiste tra due stati se hanno avuto almeno un avvistamento con forma uguale,
    # inoltre il peso sarà il numero di avvistamenti con forma uguale

    def buildGrafo5(self, min, max):
        self._grafo.clear()
        self.nodes = []
        self.edges = []
        self.idMap = {}
        self.nodes = self.cercaNodi5(min, max) # funzione che prende solo gli stati in cui ci sono stati avvistamenti nel range min-max
        for node in self.nodes:
            self.idMap[node._id] = node
        self._grafo.add_nodes_from(self.nodes)
        print(self.get_num_of_nodes())
        self.edges = DAO.getAllEdges5(min, max)
        for node1, node2, peso in self.edges:
            self._grafo.add_edge(self.idMap[node1], self.idMap[node2], weight=peso)
        print(self.get_num_of_edges())

    def cercaNodi5(self, min, max):
        nodi = []
        setStatesID = set()
        for a in self.listAvvistamenti:
            if int(min) <= int(a.datetime.year) <= int(max):
                setStatesID.add(a.state.upper())
        for s in DAO.getAllStates():
            if s._id.upper() in setStatesID:
                nodi.append(s)
        return nodi


    def get_num_of_nodes(self):
        return self._grafo.number_of_nodes()

    def get_num_of_edges(self):
        return self._grafo.number_of_edges()

    def get_nodes(self):
        return self._grafo.nodes()

    def get_edges(self):
        return list(self._grafo.edges(data=True))

    def getPesoArchiAdiacenti(self):
        result = [] # (nodo, pesoTot)
        for node in self.get_nodes():
            pesoTot = 0
            for nNext in self._grafo.neighbors(node):
                pesoTot += self._grafo[node][nNext]['weight']
            result.append((node,pesoTot))
        return result

    # Dato il grafo costruito al punto precedente, si vuole identificare un percorso semplice che
    # massimizza la distanza tra stati con archi con peso sempre crescente.
    # a. Alla pressione del bottone “Calcola percorso” avviare l’algoritmo di ricerca
    # b. Stampare a video il percorso con peso di ogni arco e distanza geodesica tra i due stati
    # c. Hint: Per il calcolo della massima distanza tra stati usare i campi “lat” e “lng” del db

    def calcPath(self):
        self.solBest = []
        self.maxDistanza = 0
        for node in self.get_nodes():
            self.ricorsione(node, [])

    def ricorsione(self, nStart, parziale):

        amm = self.getAmm(nStart, parziale)

        if not amm:
            distanza = self.calcDistanzaTot(parziale)
            if distanza > self.maxDistanza:
                print("ok")
                self.maxDistanza = distanza
                self.solBest = list(parziale)
            return

        for node1, node2 in amm:
            parziale.append((node1,node2))
            self.ricorsione(node2, parziale)
            parziale.pop()

    def getAmm(self, nStart, parziale):
        result = []
        for node in self._grafo.neighbors(nStart):
            if not parziale:
                result.append((nStart, node))
            else:
                if (nStart, node) not in result and (node, nStart) not in result:
                    if self._grafo[nStart][node]['weight'] > self._grafo[parziale[-1][0]][nStart]['weight']:
                        result.append((nStart, node))
        return result

    def calcDistanzaTot(self, parziale):
        distanzaTot = 0
        for node1, node2 in parziale:
            distanzaTot += node1.distance_HV(node2)
        return distanzaTot

    # a. A partire dal grafo calcolato in precedenza, alla pressione del tasto "Ricerca Cammino", si avvii
    # una procedura di ricerca ricorsiva per determinare il cammino di vertici (stati) più lungo, composto
    # esclusivamente da archi con peso maggiore di input (ipotizza). La lunghezza del cammino sarà calcolata sommando i pesi
    # degli archi incontrati.
    # b. Stampare la sequenza di stati che costituisce il cammino di lunghezza massima così ottenuto.

    def calcPath2(self, soglia):
        self.solBest2 = []
        self.maxPeso2 = 0
        self.origine2 = None
        for node in self.get_nodes():
            self.ricorsione2(node, [], soglia)

    def ricorsione2(self, nStart, parziale, soglia):
        amm = self.getAmm2(nStart, parziale, soglia)
        if not amm:
            peso = self.calcolaPeso2(parziale)
            if peso > self.maxPeso2:
                self.maxPeso2 = peso
                self.solBest2 = list(parziale)
                self.origine2 = parziale[0][0]
            return
        for node1, node2 in amm:
            parziale.append((nStart,node2))
            self.ricorsione2(node2, parziale, soglia)
            parziale.pop()

    def getAmm2(self, nStart, parziale, soglia):
        result = []
        for node in self._grafo.neighbors(nStart):
            if self._grafo[nStart][node]['weight'] > soglia:
                if (node,nStart) not in parziale and (nStart, node) not in parziale:
                    result.append((nStart, node))
        return result

    def calcolaPeso2(self, parziale):
        peso = 0
        for node1, node2 in parziale:
            peso += self._grafo[node1][node2]['weight']
        return peso

    # percorso semplice e chiuso di peso massimo, composto esattamente da N archi.
    # Il primo e l'ultimo vertice della sequenza devono coincidere.
    # I vertici intermedi non devono essere ripetuti.
    # La somma dei pesi degli archi percorsi deve essere massima.

    def calcPath3(self, nArchi):
        self.solBest3 = []
        self.maxPeso3 = 0
        for node in self.get_nodes():
            self.ricorsione3(node, [], nArchi)

    # percorso semplice e chiuso di peso massimo, composto esattamente da N archi.

    def ricorsione3(self, nStart, parziale, nArchi):

        if len(parziale) == nArchi-1:
            origine = parziale[0][0]
            if origine in self._grafo.neighbors(nStart):
                parziale.append((nStart, origine))
                peso = self.calcolaPeso2(parziale)
                if peso > self.maxPeso3:
                    self.maxPeso3 = peso
                    self.solBest3 = list(parziale)
                    print(len(self.solBest3), self.maxPeso3)
                parziale.pop()
            return

        amm = self.getAmm3(nStart, parziale)
        if not amm:
            return
        for node1, node2 in amm:
            parziale.append((nStart,node2))
            self.ricorsione3(node2, parziale, nArchi)
            parziale.pop()

    def getAmm3(self, nStart, parziale):
        result = []
        for node in self._grafo.neighbors(nStart):
            if (node, nStart) not in parziale and (nStart, node) not in parziale:
                result.append((nStart, node))
        return result

    # dal vertice in input trova il max path (in numero di archi) con peso >= prec

    def calcPath4(self, nameNodo):
        self.solBest4 = []
        origine = self.riconosciNodoDalNome(nameNodo)
        self.ricorsione4(origine, [])

    def ricorsione4(self, nStart, parziale):
        amm = self.getAmm4(nStart, parziale)
        if not amm:
            if len(parziale) > len(self.solBest4):
                self.solBest4 = list(parziale)
            return
        for node1, node2 in amm:
            parziale.append((nStart,node2))
            self.ricorsione4(node2, parziale)
            parziale.pop()

    def riconosciNodoDalNome(self, nameNodo):
        for node in self.get_nodes():
            if node._Name == nameNodo:
               return node

    def getAmm4(self, nStart, parziale):
        result = []
        pesoPrecedente = 0
        if len(parziale) > 0:
            pesoPrecedente = self._grafo[parziale[-1][0]][nStart]['weight']
        for node in self._grafo.neighbors(nStart):
            if (node, nStart) not in parziale and (nStart, node) not in parziale:
                if self._grafo[nStart][node]['weight'] >= pesoPrecedente:
                    result.append((nStart,node))
        return result

    # come prima ma path semplice
    def calcPath5(self, nameNodo):
        self.solBest5 = []
        origine = self.riconosciNodoDalNome(nameNodo)
        self.ricorsione5(origine, [], set())

    def ricorsione5(self, nStart, parziale, nodiVisitati):
        amm = self.getAmm5(nStart, parziale, nodiVisitati)
        if not amm:
            if len(parziale) > len(self.solBest5):
                self.solBest5 = list(parziale)
            return
        nodiVisitati.add(nStart)
        for node1, node2 in amm:
            parziale.append((nStart,node2))
            self.ricorsione5(node2, parziale, nodiVisitati)
            parziale.pop()
        nodiVisitati.remove(nStart)

    def getAmm5(self, nStart, parziale, nodiVisitati):
        result = []
        pesoPrecedente = 0
        if len(parziale) > 0:
            pesoPrecedente = self._grafo[parziale[-1][0]][nStart]['weight']
        for node in self._grafo.neighbors(nStart):
            if node not in nodiVisitati:
                if (node, nStart) not in parziale and (nStart, node) not in parziale:
                    if self._grafo[nStart][node]['weight'] >= pesoPrecedente:
                        result.append((nStart,node))
        return result
    # path semplice, aciclico, da origine a destinazione evitando la stringa e toccando più località possibili
    def calcPath6(self, nodoOrigine, nameDestinazione, stringaDaEvitare):
        self.solBest6 = []
        parziale = []
        nodoDestinazione = self.riconosciNodoDalNome(nameDestinazione)
        parziale.append(nodoOrigine)
        self.ricorsione6(nodoOrigine, nodoDestinazione, stringaDaEvitare, parziale)

    def ricorsione6(self, nStart, nDest, evita, parziale):
        amm = self.getAmm6(nStart, evita, parziale)
        if nDest in amm:
            parziale.append(nDest)
            if len(parziale) > len(self.solBest6):
                self.solBest6 = list(parziale)
            return
        if not amm:
            return
        for nNext in amm:
            parziale.append(nNext)
            self.ricorsione6(nNext, nDest, evita, parziale)
            parziale.pop()

    # path semplice, aciclico, da origine a destinazione evitando la stringa e toccando più località possibili
    def getAmm6(self, nStart, evita, parziale):
        result = []
        for node in self._grafo.neighbors(nStart):
            if node not in parziale:
                if evita.lower() not in node._Name.lower():
                    result.append(node)
        return result

        # Permettere all'utente di inserire una popolazione totale.
        # Alla pressione del bottone, utilizzare un algoritmo ricorsivo per selezionare un insieme di stati
        # che soddisfi le seguenti condizioni:
        # Include uno stato scelto.
        # Include solo stati appartenenti alla stessa componente connessa dello stato scelto.
        # Massimizza il numero di nodi inclusi.
        # La somma delle durate degli non deve superare la popolazione Totale.
        # -> seleziono tra tutti quelli rimasti lo stato con pop minore

    def fallo(self, avvistamentoOGGETTO):
        print(avvistamentoOGGETTO.id, avvistamentoOGGETTO.city)

    def calcSet(self, statoName, pTot):
        nOrigine = self.riconosciNodoDalNome(statoName)
        self.bestSet = set()
        compConn = nx.node_connected_component(self._grafo, nOrigine)
        parziale = set([nOrigine])
        compConn.remove(nOrigine)
        self.ricorsione7(compConn, parziale, pTot)
    def ricorsione7(self, compConn, parziale, pTot):
        if self.popolazioneTot(parziale) > pTot:            # 1) verifica se parziale è sol ammissibile
            return
        if len(parziale) > len(self.bestSet):         # 2) verifica se parziale è meglio del best
            self.bestSet = copy.deepcopy(parziale)
            # qui nessuna return, per ora è sol ottima, può anche migliorare !!
        for c in compConn:          # 3) ciclo su nodi aggiungibili -- ricorsione
            if c not in parziale: # 1
                parziale.add(c)
                rimanenti = copy.deepcopy(compConn) # 2
                rimanenti.remove(c) # 3
                self.ricorsione7(rimanenti, parziale, pTot)
                parziale.pop()
        # 1,2,3 usati per limitare la ricorsione ai casi solo necessari
    def popolazioneTot(self, parziale):
        count = 0
        for node in parziale:
            count += node._Population
        return count




































