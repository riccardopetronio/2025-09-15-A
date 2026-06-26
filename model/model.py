import copy
from datetime import datetime

import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.pilotiDict = dict()
        self.solBest = []

    def getAllYears(self):
        return DAO.getAllYears()

    def createGraph(self, annoIn, annoFine):
        self.grafo.clear()
        self.solBest = []
        self.pilotiDict = dict()
        allP = DAO.getPiloti(annoIn, annoFine)
        self.grafo.add_nodes_from(allP)
        for pilot in allP:
            self.pilotiDict[pilot.driverId] = pilot

    def addArchi(self, annoIn, annoFine):
        connessioni = DAO.getConnessioni(annoIn, annoFine)
        for c in connessioni:
            if self.pilotiDict.get(c[0]) is not None and self.pilotiDict.get(c[1]) is not None:
                self.grafo.add_edge(self.pilotiDict[c[0]], self.pilotiDict[c[1]], weight = c[2])


    def archiMaggiori(self):
        # Estrae la lista includendo i dati dell'arco
        archi_con_dati = list(self.grafo.edges(data=True))

        # Ordina in base al valore dentro il dizionario degli attributi
        return sorted(archi_con_dati, key=lambda i: i[2]['weight'], reverse=True)


    def numComponentiConnesse(self):
        return nx.number_connected_components(self.grafo)

    # def componentiConnessaMaggiore(self):
    #     largest_cc = max(nx.connected_components(self.grafo), key=len)
    #     return sorted(largest_cc, key=lambda c: len(list(self.grafo.neighbors(c))), reverse=True)

    def componentiConnessaMaggiore(self):
        # Trova la componente connessa più grande
        largest_cc = max(nx.connected_components(self.grafo), key=len)

        # Ordina i nodi in base al numero di vicini (grado), dal più grande al più piccolo
        listaOrdinata = sorted(largest_cc, key=lambda c: self.grafo.degree(c), reverse=True)

        risultato = []
        for i in listaOrdinata:
            risultato.append((i, self.grafo.degree(i)))
        return risultato

    # def cercaInsieme(self, dimensione):
    #     parziale = []
    #     piloti = self.pilotiDict.values()
    #     self.ricorsione(dimensione, piloti, parziale)
    #     return self.solBest, self.intervalloEta(self.solBest)
    #
    # def ricorsione(self, dimensione, piloti, parziale):
    #     if len(parziale) == dimensione:
    #         if len(self.solBest) == 0 or self.intervalloEta(parziale) < self.intervalloEta(self.solBest):
    #             self.solBest = copy.deepcopy(parziale)
    #     else:
    #         for vTemp in piloti:
    #             if vTemp in parziale:
    #                 continue
    #             if self.nodiNonConnessi(parziale, vTemp):
    #                 parziale.append(vTemp)
    #                 self.ricorsione(dimensione, piloti, parziale)
    #                 parziale.pop()

    def cercaInsieme(self, dimensione):
        self.solBest = []
        parziale = []
        piloti = list(self.pilotiDict.values())  # lista, serve l'indicizzazione
        self.ricorsione(dimensione, piloti, parziale, 0)
        return self.solBest, self.intervalloEta(self.solBest)

    def ricorsione(self, dimensione, piloti, parziale, start):
        if len(parziale) == dimensione:
            if len(self.solBest) == 0 or self.intervalloEta(parziale) < self.intervalloEta(self.solBest):
                self.solBest = copy.deepcopy(parziale)
        else:
            for i in range(start, len(piloti)):
                vTemp = piloti[i]
                if self.nodiNonConnessi(parziale, vTemp):
                    parziale.append(vTemp)
                    self.ricorsione(dimensione, piloti, parziale, i + 1)
                    parziale.pop()


    def nodiNonConnessi(self, lista, nuovo):
        if len(lista) == 0:
            return True
        for i in lista:
            if nx.has_path(self.grafo, i, nuovo):
                return False
        return True


    def intervalloEta(self, lista: list):
        listaOrdinata = sorted(lista, key=lambda i: i.dob, reverse=True)
        primo = listaOrdinata[0]
        ultimo = listaOrdinata[-1]
        return primo.dob - ultimo.dob

    def getNumNodi(self):
        return len(self.grafo.nodes)
    def getNumArchi(self):
        return len(self.grafo.edges)

