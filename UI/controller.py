
import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listShape = []

    # a. Permettere all’utente di scegliere da un menù a tendina un anno tra tutti i possibili anni in cui ci sono stati
    # avvistamenti (per verifica: il menù dovrà contenere tutti i valori tra il 1910 ed il 2014, estremi inclusi).
    # b. Popolare il menù a tendina Forma con tutte le possibili forme, prese dalla colonna “shape” del db, relative
    # agli avvistamenti nell’anno considerato.

    def fillDD(self):

        self._listYear = self._model.getYears()

        for year in self._listYear:
            self._view.ddyear.options.append(ft.dropdown.Option(year))

        self._view.ddyear.on_change = self.on_year_change

        self._view.update_page()

    def on_year_change(self, e):

        year = int(self._view.ddyear.value)

        self._listShape = self._model.getShape(year)

        for shape in self._listShape:
            self._view.ddshape.options.append(ft.dropdown.Option(shape))

        self._view.update_page()


    def handle_graph(self, e):

        self._view.txt_result.controls.clear()

        y = int(self._view.ddyear.value)

        s = self._view.ddshape.value

        self._model.loadStatesByYandS(y, s)

        self._model.buildgraph(y, s)

        self._view.txt_result.controls.append(ft.Text(
            f"Numero di nodi: {self._model.get_num_of_nodes()}\n"
            f"Numero di archi: {self._model.get_num_of_edges()}"))

        for state in self._model.get_nodes():
            self._view.txt_result.controls.append(ft.Text(
                f"Nodo {state._id}, somma pesi su archi adiacenti: {self._model.sommaPesiArchiAdiacenti(state)}"))

        self._view.update_page()

    # CAMMINO SEMPLICE CON PESO CRESCENTE CHE MASSIMIZZA DISTANZA TRA STATI
    def handle_path(self, e):

        self._view.txtOut2.controls.clear()

        self._model.calcolaPercorso()

        percorso = self._model.solBest

        self._view.txtOut2.controls.append(ft.Text(
        f"Peso cammino massimo: {int(self._model.pesoTotPercorso)};"
        f"Distanza cammino massimo: {float(self._model.distanzaBest)}"))
        for edge in percorso:
            self._view.txtOut2.controls.append(ft.Text(
                f"{edge[0]._id} --> {edge[1]._id}; weight: {int(self._model.graph[edge[0]][edge[1]]['weight'])};"
                f" distanza: {float(self._model.calcolaDistanzaTraNodi(edge[0], edge[1]))}"))

        self._view.update_page()
