import random

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        # self.choice = None

    def fillDDYear(self):
        setYears = set()
        for avvistamento in self._model.listAvvistamenti:
            setYears.add(avvistamento.datetime.year)
        for year in sorted(setYears, reverse=False):
            self._view.ddyear.options.append(ft.dropdown.Option(year))
        self._view.update_page()

    """def fillDDAvvistamenti(self, e):
        year = int(self._view.ddyear.value)
        for a in sorted(self._model.listAvvistamenti, key=lambda x: x.datetime, reverse = True):
            if a.datetime.year == year:
                self._view.ddAVVISTAMENTO.options.append(ft.dropdown.Option(data=a, on_click=self.readDD,text=f"{a.city}, {a.datetime}, {a.shape}"))
        self._view.update_page()
    def readDDAvvistamenti(self, e):
        if e.control.data == None:
            self.choice = None
        else:
            self.choice = e.control.data"""

    def fillDDShape(self, e):
        setForme = set()
        for avvistamento in self._model.listAvvistamenti:
            if int(avvistamento.datetime.year) == int(self._view.ddyear.value) and avvistamento.shape != '':
                setForme.add(avvistamento.shape)
        for shape in sorted(setForme, reverse=False):
            self._view.ddshape.options.append(ft.dropdown.Option(shape))
        self._view.update_page()

    def handle_graph(self, e):
        self._view.txt_result.controls.clear()
        year = int(self._view.ddyear.value)
        shape = str(self._view.ddshape.value)
        self._model.buildGrafo(year, shape)
        self._view.txt_result.controls.append(ft.Text(f"NODI: {self._model.get_num_of_nodes()}"))
        self._view.txt_result.controls.append(ft.Text(f"ARCHI: {self._model.get_num_of_edges()}"))
        for node, count in self._model.getPesoArchiAdiacenti():
            self._view.txt_result.controls.append(ft.Text(f"NODO: {node._id}, PESO: {count} "))
        self._view.update_page()

    # Esercizio 1: Grafo degli Stati con Avvistamenti
    # Dropdown 1: Permetti all'utente di scegliere un anno tra quelli disponibili nel database.
    # Dropdown 2: Permetti all'utente di scegliere una forma di UFO tra quelle presenti nella colonna shape (escludendo i valori nulli).
    # Crea un grafo non orientato e non pesato in cui:
    # I nodi sono gli stati degli USA.
    # Un arco esiste tra due stati se un avvistamento di UFO è stato registrato in entrambi nello stesso giorno.
    # Il grafo deve essere costruito con gli avvistamenti filtrati dall'anno e dalla forma selezionati.

    def handle_graph2(self, e):
        if self._view.ddyear.value is None or self._view.ddshape.value is None:
            self._view.create_alert("Seleziona i dropdown pirla!")
            return
        year = int(self._view.ddyear.value)
        shape = str(self._view.ddshape.value)
        self._model.buildGrafo2(year, shape)


    # Esercizio 2: Grafo degli Avvistamenti Consecutivi per Durata
    # Dropdown 1: Permetti all'utente di scegliere uno stato da un menù a tendina che mostra tutti gli stati disponibili nel database.
    # Dropdown 2: Permetti all'utente di scegliere un anno da un menù a tendina che mostra tutti gli anni in cui c'è stato almeno un avvistamento.
    # Input: Permetti all'utente di scegliere un massimo di durata
    # Costruisci il grafo considerando solo gli avvistamenti nello stato, nell'anno e nel range di durata selezionati.
    # Crea un grafo orientato e pesato in cui:
    # I nodi sono gli avvistamenti di UFO (basati sulla tabella sighting).
    # Un arco esiste tra due avvistamenti se sono avvenuti nello stesso stato e il primo ha una durata inferiore rispetto al secondo.
    # Il peso dell'arco è dato dalla differenza di durata tra i due avvistamenti.

    def handle_graph3(self, e):
        state = "New York"
        year = "2010"
        durataMax = 30
        self._model.buildGrafo3(state, year, durataMax)

    # Esercizio 4: Grafo degli Avvistamenti per Stato
    # Dropdown 1: Permetti all'utente di scegliere un intervallo temporale (esempio: da gennaio a marzo di un anno specifico).
    # Dropdown 2: Permetti all'utente di selezionare uno stato tra quelli nel database.
    # Costruisci un grafo orientato e non pesato in cui:
    # I nodi sono gli avvistamenti di UFO.
    # Un arco esiste tra due avvistamenti se sono avvenuti nello stesso stato e l'avvistamento iniziale è accaduto
    # prima del successivo (ordine temporale basato su datetime).
    # Il grafo sarà costruito solo con avvistamenti nell'intervallo temporale e nello stato scelto.
    # aggiunta di anno nei parametri dati sennò risultato troppo grande

    def handle_graph4(self, e):
        m1 = 1
        m2 = 6
        s = "Georgia"
        anno = 2000
        self._model.buildGrafo4(anno, s, m1, m2)

    # Esercizio 5: Grafo degli Stati con archi per avvistamenti uguali
    # Dropdown 1: Permetti all'utente di scegliere un range temporale da un menù a tendina (esempio: 2000-2005, 2006-2010, ecc.).
    # Crea un grafo non orientato e pesato in cui:
    # I nodi sono gli stati degli USA.
    # Un arco esiste tra due stati se hanno avuto almeno un avvistamento con forma uguale,
    # inoltre il peso sarà il numero di avvistamenti con forma uguale

    def handle_graph5(self, e):
        intervallo = "1945-1950"
        min, max = intervallo.split("-")
        self._model.buildGrafo5(min, max)



    # Dato il grafo costruito al punto precedente, si vuole identificare un percorso semplice che
    # massimizza la distanza tra stati con archi con peso sempre crescente.
    # a. Alla pressione del bottone “Calcola percorso” avviare l’algoritmo di ricerca
    # b. Stampare a video il percorso con peso di ogni arco e distanza geodesica tra i due stati
    # c. Hint: Per il calcolo della massima distanza tra stati usare i campi “lat” e “lng” del db
    def handle_path(self, e):
        self._view.txtOut2.controls.clear()
        self._model.calcPath()
        path = self._model.solBest
        distanza = self._model.maxDistanza
        self._view.txtOut2.controls.append(ft.Text(
            f"Percorso a distanza massima trovato.\nLa distanza percorsa è: {distanza}, mentre i nodi attraversati sono {len(path)}."))
        for node1, node2 in path:
            self._view.txtOut2.controls.append(ft.Text(
                f"{node1._Name} - {node2._Name} [{self._model._grafo[node1][node2]['weight']}]; distanza = {node1.distance_HV(node2)}"))
        self._view.update_page()

    # a. A partire dal grafo calcolato in precedenza, alla pressione del tasto "Ricerca Cammino", si avvii
    # una procedura di ricerca ricorsiva per determinare il cammino di vertici (stati) più lungo, composto
    # esclusivamente da archi con peso maggiore di input. La lunghezza del cammino sarà calcolata sommando i pesi
    # degli archi incontrati.
    # b. Stampare la sequenza di stati che costituisce il cammino di lunghezza massima così ottenuto.
    def handle_path2(self, e):
        self._view.txtOut2.controls.clear()
        input = 10
        self._model.calcPath2(input)
        path = self._model.solBest2
        origine = self._model.origine2
        self._view.txtOut2.controls.append(ft.Text(f"Percorso trovato, i nodi attraversati sono {len(path)}."))
        self._view.txtOut2.controls.append(ft.Text(f"1) {origine._Name}"))
        i = 1
        for node1, node2 in path:
            i += 1
            self._view.txtOut2.controls.append(ft.Text(f"{i}) {node2._Name}"))
        self._view.update_page()
    # Dato il grafo costruito in precedenza, si desidera identificare un percorso semplice e chiuso di peso massimo,
    # composto esattamente da N archi. Il valore di N deve essere inserito dall'utente tramite un campo nell'
    # interfaccia grafica, e deve essere almeno pari a 2. La sequenza di vertici deve rispettare le seguenti condizioni:
    # Il primo e l'ultimo vertice della sequenza devono coincidere.
    # I vertici intermedi non devono essere ripetuti.
    # La somma dei pesi degli archi percorsi deve essere massima.
    # Visualizzare:
    # La somma totale dei pesi degli archi nel percorso di peso massimo.
    # Il percorso trovato, sotto forma di sequenza di archi, ciascuno rappresentato come:
    def handle_path3(self, e):
        self._view.txtOut2.controls.clear()
        input = 2
        self._model.calcPath3(input)
        path = self._model.solBest3
        peso = self._model.maxPeso3
        self._view.txtOut2.controls.append(ft.Text(f"Percorso trovato a peso {peso}, i nodi attraversati sono {len(path)}."))
        i = 0
        for node1, node2 in path:
            i += 1
            self._view.txtOut2.controls.append(ft.Text(
                f"{i}) {node1._Name} -> {node2._Name} [{self._model._grafo[node1][node2]['weight']}]"))
        self._view.update_page()
    # Dato il grafo costruito in precedenza, si desidera identificare un percorso che, partendo da un vertice
    # selezionato (scelto da una tendina), individui il cammino più lungo in termini di numero di archi,
    # dove il peso di ciascun arco è maggiore o uguale a quello di tutti gli archi già percorsi.
    # La qualità del percorso sarà valutata in base al numero di archi attraversati, senza considerare i pesi.
    # Un arco può essere aggiunto al percorso solo se il suo peso è maggiore o uguale a tutti gli archi già percorsi.
    def handle_path4(self, e):
        input = "Georgia"
        self._model.calcPath4(input)
        path = self._model.solBest4
        self._view.txtOut2.controls.append(ft.Text(f"Percorso massimo trovato, è composto da {len(path)} archi."))
        for node1, node2 in path:
            self._view.txtOut2.controls.append(ft.Text(
                f"{node1._Name} -> {node2._Name} [{self._model._grafo[node1][node2]['weight']}]"
            ))
        self._view.update_page()

        # stesso caso di prima MA percorso semplice (non ripassa dallo stesso nodo)
    def handle_path5(self, e):
        input = "Georgia"
        self._model.calcPath5(input)
        path = self._model.solBest5
        self._view.txtOut2.controls.append(ft.Text(f"Percorso massimo trovato, è composto da {len(path)} archi."))
        for node1, node2 in path:
            self._view.txtOut2.controls.append(ft.Text(
                f"{node1._Name} -> {node2._Name} [{self._model._grafo[node1][node2]['weight']}]"
            ))
        self._view.update_page()

    # Permettere all'utente di selezionare una località di destinazione (t) e di inserire una stringa non vuota (s).
    # Alla pressione del bottone "Calcola Percorso", trovare, se esiste, un cammino aciclico semplice con le seguenti
    # caratteristiche:
    # - Inizia da una delle località calcolate al punto 1.d (scelta in modo casuale) e termina in t.
    # - Tocca il maggior numero di località.
    # - Non passa per località il cui nome contenga la sottostringa s.
    def handle_path6(self, e):
        input1 = "Georgia" # località
        input2 = "y" # sitringa che non deve essere contenuta nei nodi che attraversa
        origine = random.choice(list(self._model.get_nodes()))
        self._model.calcPath6(origine, input1, input2)
        path = self._model.solBest6
        if not path:
            self._view.txtOut2.controls.append(ft.Text(
                f"Il percorso che massimizza il numero di nodi attraversati, dove i nomi dei nodi non contengono la stringa {input2}, dal nodo {origine} al nodo {input1}, non esiste."))
            self._view.update_page()
            return
        self._view.txtOut2.controls.append(ft.Text(
            f"Il percorso che massimizza il numero di nodi attraversati, dove i nomi dei nodi non contengono la stringa {input2}, dal nodo {origine} al nodo {input1}, è stato trovato."
            f"\nIl percorso attraversa {len(path)} nodi."))
        i = 0
        for node in path:
            i+=1
            self._view.txtOut2.controls.append(ft.Text(f"{i}){node._Name}"))
        self._view.update_page()

        # (esercizio Itunes un po' modificato)
        # Permettere all'utente di inserire una popolazione totale.
        # Alla pressione del bottone, utilizzare un algoritmo ricorsivo per selezionare un insieme di stati
        # che soddisfi le seguenti condizioni:
        # Include uno stato scelto.
        # Include solo stati appartenenti alla stessa componente connessa dello stato scelto.
        # Massimizza il numero di nodi inclusi.
        # La somma delle durate degli non deve superare la popolazione Totale.

    def handle_set(self, e):
        pop = 100000000 #100 milioni
        stato = "New York" #stato scelto
        self._model.calcSet(stato, pop)
        set = self._model.bestSet
        popTot = self._model.popolazioneTot(set)
        print(len(set), popTot)