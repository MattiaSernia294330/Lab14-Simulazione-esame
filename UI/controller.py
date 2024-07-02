import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._soglia=None
    def handle_graph(self, e):
        self._view.txt_result.clean()
        self._model.creaGrafo()
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {self._model.getNodi()} Numero di archi: {self._model.getArchi()}"))
        minmax=self._model.minmax()
        self._view.txt_result.controls.append(ft.Text(f"informazioni sui pesi degli archi - valore minimo: {minmax[1]} e valore massimo: {minmax[0]}"))
        self._view.txt_name.disabled=False
        self._view.btn_countedges.disabled=False
        self._view.update_page()
        pass
    def read_soglia(self,e):
        self._soglia=e.control.value
    def handle_countedges(self, e):
        self._view.txt_result2.clean()
        minmax = self._model.minmax()
        try:
            soglia=float(self._soglia)
        except (ValueError):
            self._view.create_alert("inserisci una soglia valida")
            return
        if soglia>minmax[0] or soglia<minmax[1]:
            self._view.create_alert("la soglia inserita non è all'inetrno del grafo")
            return
        altobasso=self._model.conta(soglia)
        self._view.txt_result2.controls.append(
            ft.Text(f"numero archi con peso maggiore della soglia {altobasso[0]}"))
        self._view.txt_result2.controls.append(
            ft.Text(f"numero archi con peso minore della soglia {altobasso[1]}"))
        self._view.update_page()
        pass

    def handle_search(self, e):
        minmax = self._model.minmax()
        try:
            soglia = float(self._soglia)
        except (ValueError):
            self._view.create_alert("inserisci una soglia valida")
            return
        if soglia > minmax[0] or soglia < minmax[1]:
            self._view.create_alert("la soglia inserita non è all'inetrno del grafo")
            return
        self._model.conta(soglia)
        alfa=self._model.handle_ricorsione()
        self._view.txt_result3.controls.append(
            ft.Text(f"peso cammino massimo {alfa[1]}"))
        for element in alfa[0]:
            self._view.txt_result3.controls.append(
                ft.Text(f"peso cammino massimo {element}"))
        self._view.update_page()
        pass