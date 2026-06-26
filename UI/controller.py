import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self.annoFin = None
        self.annoIn = None


    def handleCreaGrafo(self,e):
        self._view._txt_result.controls.clear()

        if self.annoIn is None or self.annoFin is None:
            self._view._txt_result.controls.append(ft.Text(f"devi selezionare gli anni", color="red"))
            self._view.update_page()
            return
        if self.annoIn > self.annoFin:
            self._view._txt_result.controls.append(ft.Text(f"l'anno di inizio deve essere <= di quello di fine", color="red"))
            self._view.update_page()
            return

        self._model.createGraph(self.annoIn, self.annoFin)
        self._model.addArchi(self.annoIn, self.annoFin)

        numNodi = self._model.getNumNodi()
        numArchi = self._model.getNumArchi()

        self._view._txt_result.controls.append(
            ft.Text(f"ci sono {numNodi} nodi e {numArchi} archi", color="green"))

        self._view._btnstampa.disabled=False
        self._view._txtInK.disabled=False
        self._view._btnCerca.disabled=False
        self._view.update_page()

    def handleDettagli(self, e):
        archiMaggiori = self._model.archiMaggiori()
        self._view._txt_result.controls.append(ft.Text(f"i 3 archi maggiori:"))

        dim = 3
        if len(archiMaggiori) < 3:
            dim = len(archiMaggiori)
            self._view._txt_result.controls.append(ft.Text(f"ci sono solo {dim} archi", color="orange"))

        for i in range(dim):
            self._view._txt_result.controls.append(
                ft.Text(f"{archiMaggiori[i][0]} -> {archiMaggiori[i][1]}  ({archiMaggiori[i][2]['weight']})", color="green"))
        self._view.update_page()

        nComConnesse = self._model.numComponentiConnesse()
        self._view._txt_result.controls.append(ft.Text(f"ci sono {nComConnesse} componenti connesse", color="blue"))

        nodiComMax = self._model.componentiConnessaMaggiore()
        self._view._txt_result.controls.append(ft.Text(f"ci sono {len(nodiComMax)} nodi nella massima componente connessa"))
        for i in nodiComMax:
            self._view._txt_result.controls.append(ft.Text( f"{str(i[0])}  ({i[1]})" ))

        self._view.update_page()


    def handleCerca(self, e):
        self._view._txt_result.controls.clear()

        dimInsieme = self._view._txtInK.value
        dimInsiemeInt = 0
        if dimInsieme == "":
            self._view._txt_result.controls.append(ft.Text(f"devi inserire un numero in Num di piloti", color="red"))
            self._view.update_page()
            return
        try:
            dimInsiemeInt = int(dimInsieme)
            if dimInsiemeInt < 0:
                self._view._txt_result.controls.append(ft.Text(f"Num di piloti deve essere > 0", color="red"))
                self._view.update_page()
                return
        except ValueError:
            self._view._txt_result.controls.append(ft.Text(f"devi inserire un numero in Num di piloti", color="red"))
            self._view.update_page()
            return

        insieme, differenza = self._model.cercaInsieme(dimInsiemeInt)
        self._view._txt_result.controls.append(ft.Text(f"la differenza minima è {differenza}", color="green"))
        self._view._txt_result.controls.append(ft.Text(f"di seguito i nodi:", color="green"))
        for i in insieme:
            self._view._txt_result.controls.append(ft.Text(f"{str(i)}", color="green"))
        self._view.update_page()

    def fillDD(self):
        anni = self._model.getAllYears()
        for year in anni:
            self._view._ddAnno1.options.append(ft.dropdown.Option(text=year,
                                                                     data=year,
                                                                     on_click=self.annoInizio))
            self._view._ddAnno2.options.append(ft.dropdown.Option(text=year,
                                                                  data=year,
                                                                  on_click=self.annoFine))
        self._view.update_page()


    def annoInizio(self, e):
        self.annoIn = e.control.data
    def annoFine(self, e):
        self.annoFin = e.control.data

