import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self._grafo=nx.DiGraph()
        self._dizionarioNodi={}
        self._numeroMax=0
        self._numeroMin=0
        self._grafoSoglia=nx.DiGraph()
        self._bestSol = []
        self._migliorNumero = 0
        pass
    def creaGrafo(self):
        self._grafo.clear()
        self._dizionarioNodi={}
        for nodo in DAO.getNodes():
            self._grafo.add_node(nodo)
            self._dizionarioNodi[nodo]=nodo
        for edge in DAO.getArchi():
            if self._grafo.has_edge(edge.c1, edge.c2):
                self._grafo[edge.c1][edge.c2]["weight"]+=edge.esp
            else:
                self._grafo.add_edge(edge.c1,edge.c2,weight=edge.esp)

    def getNodi(self):
        return len(self._grafo.nodes())
    def getArchi(self):
        return len(self._grafo.edges())

    def minmax(self):
        listanumeri=[]
        for nodo1 in self._grafo.nodes():
            for nodo2 in self._grafo.nodes():
                if nodo1!=nodo2 and self._grafo.has_edge(nodo1,nodo2):
                    listanumeri.append(self._grafo[nodo1][nodo2]["weight"])
        self._numeroMax=max(listanumeri)
        self._numeroMin=min(listanumeri)
        return self._numeroMax,self._numeroMin
    def conta(self,soglia):
        numeroalto=0
        numerobasso=0
        self._grafoSoglia.clear()
        for nodo1 in self._grafo.nodes():
            for nodo2 in self._grafo.nodes():
                if nodo1 != nodo2 and self._grafo.has_edge(nodo1, nodo2):
                    if self._grafo[nodo1][nodo2]["weight"]>soglia:
                        numeroalto+=1
                        self._grafoSoglia.add_edge(nodo1,nodo2,weight=self._grafo[nodo1][nodo2]["weight"])
                    elif self._grafo[nodo1][nodo2]["weight"]<soglia:
                        numerobasso+=1
        return numeroalto, numerobasso

    def _ricorsione(self, parziale, nodo,numeroattuale):
        successori = list(self._grafoSoglia.successors(nodo))
        for element in successori.copy():
            if f"{nodo}-->{element} : {self._grafoSoglia[nodo][element]['weight']}" in parziale:
                successori.remove(element)
        if len(successori) == 0:
            if numeroattuale > self._migliorNumero:
                self._bestSol = parziale
                self._migliorNumero = numeroattuale
            return
        else:
            for item in successori:
                nuovo_nodo = item
                parziale_nuovo = list(parziale)
                parziale_nuovo.append(f"{nodo}-->{nuovo_nodo} : {self._grafoSoglia[nodo][nuovo_nodo]['weight']}")
                numeroattuale_nuovo = numeroattuale + self._grafoSoglia[nodo][nuovo_nodo]['weight']
                self._ricorsione(parziale_nuovo, nuovo_nodo, numeroattuale_nuovo)

    def handle_ricorsione(self):
        self._bestSol = []
        self._migliorNumero = 0
        for nodo in self._grafoSoglia.nodes():
            self._ricorsione([],nodo,0)
        return self._bestSol, self._migliorNumero



