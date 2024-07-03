import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    # Popolare il menù a tendina Forma con tutte le possibili forme, prese dalla colonna “shape” del db, relative
    # agli avvistamenti nell’anno considerato.

    def fillDD(self):

        listaAvvistamenti = self._model.getAvvistamenti()

        for avvistamento in listaAvvistamenti:
            if avvistamento.datetime.year not in self._listYear:
                self._listYear.append(avvistamento.datetime.year)
            if avvistamento.shape not in self._listShape:
                self._listShape.append(avvistamento.shape)

        for y in self._listYear:
            if int(y) > 2014 or int(y) < 1910:
                self._view.createAlert("Errore nell'estrazione degli anni.")

        for y in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(y))

        for s in self._listShape:
            self._view.ddshape.options.append(ft.dropdown.Option(s))

        self._view.update_page()


    # c. Facendo click sul bottone CREA GRAFO, creare un grafo semplice, pesato e non orientato, i cui vertici siano
    # tutti gli stati presenti nella tabella “state”. Un arco collega due stati solo se sono confinanti, come indicato
    # nella tabella “neighbor”.
    # d. Il peso dell’arco viene calcolato come il numero di avvistamenti che hanno la stessa forma (colonna “shape”)
    # selezionata dal menù a tendina Forma, e che si sono verificati nello stesso anno selezionato (da estrarre dalla
    # colonna “datetime”), nei due stati considerati.
    # e. Stampare per ogni stato la somma dei pesi degli archi adiacenti.

    def handle_graph(self, e):

        s = self._view.ddshape.value
        y = self._view.ddyear.value

        self._model.buildGraph(s,y)
        self._view.txt_result.controls.append(ft.Text(
            f"Numero di vertici: {self._model.get_num_of_nodes()} Numero di archi: {self._model.get_num_of_edges()}"))

        listaPesiAdiacentiPerStato = self._model.getListaPesiAdiacentiPerStato()
        for stato in listaPesiAdiacentiPerStato:
            self._view.txt_result.controls.append(ft.Text(
                f"Nodo: {stato[0].id}, somma pesi su archi = {stato[1]}"))

        self._view.update_page()

        pass

    def handle_path(self, e):
        pass