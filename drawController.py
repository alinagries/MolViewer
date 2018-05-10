# -*- coding: utf-8 -*-


from vispy import app, gloo
from vispy.util.transforms import perspective, translate, rotate, scale
from logicMolecule import *
from graphicMolecule import GraphicMolecule

import logicMolecule
import math



class DrawController(app.Canvas):

    '''

    Diese Klasse ist fuer die Visualisierung des Molekuels verantwortlich.
    Sie erbt vom Canvas von vispy und nutzt auch die Program funktion von vispy.

    '''

    def __init__(self, parent, master):

        '''

        In der __init__ Methode wird gloo konfiguriert und der pyqt Kontext festgelegt. Des Weiteren werden alle
        self.(...) Variablen und der Timer (siehe on_timer) initiiert.

        Parameter:  parent wird benoetigt zur Festsetzung des Kontextes
                    master wird zu Interaktion mit der GUI benötigt (z.B. Errors)
        Rückgabewerte: -

        '''

        print('[* Canvas: initializing *]')

        app.use_app(backend_name='pyqt4', call_reuse=True)
        app.Canvas.__init__(self, size=(1465, 850), title='GraphicMolecule Vizualizer',
                            keys='interactive', parent=parent)
        gloo.set_state(clear_color=(0.1,0.14, 0.23, 1.00), depth_test=True, blend=True,
                       blend_func=('src_alpha', 'one_minus_src_alpha'))
        gloo.wrappers.set_depth_range(near=0.9,far=1)

        #initializing all self._____ variables
        self._master = master

        self._molName = ''
        self._molecule = None
        self._programs = []

        self._decreaseDrawHorizon = False
        self._increaseDrawHorizon = False
        self._drawHorizon = 0

        self._rotSpeed = 0
        self._zoom = -7
        self._rotation = 0
        self._rotationVec = [0, 0, 0]

        self._atomSizes = 0
        self._atomColors = (0, 0, 0)
        self._bondSize = 0
        self._bondColor = (0, 0, 0)
        self._atomDT = ''
        self._bondDT = ''

        #als observer anmelden
        self._master.registerObserver(self)

        self.timer = app.Timer('auto', self.on_timer, start=True)

    def notify(self, dataType):
        if dataType=='Atom':
            data = self._master.getAtomSettings()
            self._atomColors = (data['CColor'], data['HColor'], data['OColor'])
            self._atomSizes = (data['CSize'], data['HSize'], data['OSize'])
            self._atomDT = data['Viz']
        elif dataType=='Bond':
            data = self._master.getBondSettings()
            self._bondColor = data['Color']
            self._bondSize = data['Size']
            self._bondDT = data['Viz']
        elif dataType=='General':
            data = self._master.getGeneralSettings()
            self._rotSpeed = data[0]
            self._rotationVec = data[1]
        if not self._molecule==None:
            self.uploadSettingsToMol()

    def uploadSettingsToMol(self):

        '''

        Diese Methode laedt die Optionen "color", "drawtype" und "size" von Atomen und Bindungen
        in das graphische Molekuel.

        Parameter: -
        Rückgabewerte: -

        '''

        self._molecule.setAtomDrawtype(self._atomDT)
        self._molecule.setBondDrawtype(self._bondDT)
        self._molecule.setBondColor(self._bondColor)
        self._molecule.setAtomColors(self._atomColors)
        self._molecule.setBondSize(self._bondSize)
        self._molecule.setAtomSizes(self._atomSizes)


    def newMolecule(self, molName, urgent=0):

        '''

        Mit dieser Methode können externe Klassen ein Molekuel erstellen. Der "urgent" Parameter fragt ab
        ob eine Uebergangsanimation dargestellt werden soll oder nicht. Der Uebergang wurde mithilfe der on_timer
        Funktion und der Variable "_decreaseDrawHorizion" realisiert.

        Parameter: Molekuelname (nach IUPAC Richtlinien), urgent-flag
        Rückgabewerte: -

        '''

        print('[* Canvas: making new molecule named "' + molName + '" *]')
        if urgent:
            self._molName = molName
            rawMol = LogicMolecule(self._molName)
            proof = rawMol.createMolecule()
            if isinstance(proof, str):
                self._master.showError(proof)
            else:
                new_molecule = GraphicMolecule(rawMol)
                new_molecule.processPositions()
                self._molecule = new_molecule
                self._getPrograms()
                self.uploadSettingsToMol()
                self._master.setMolecularFormula(self.getMolecularFormula())
        else:
            self._molName = molName
            self._decreaseDrawHorizon = True
            self._drawHorizon = -1.5

    def getMolecularFormula(self):

        '''

        Parameter: -
        Rückgabewerte: Die Summenformel des aktullen Molekuels

        '''

        rawMol = self._molecule.getRawMol()
        return rawMol.getMolecularFormula()

    def getDescription(self):

        '''

        Parameter: -
        Rückgabewerte: Die Beschreibung der Summenformel des aktullen Molekuels

        '''

        rawMol = self._molecule.getRawMol()
        return rawMol.getDescription()

    def on_draw(self, event):

        '''

        Die on_draw Methode wird mehrmals in der Sekunde ausgefuehrt. Sie ist ein von vispy gegebener Standart.
        Mit ihr haben wir neben dem Darstellen des Molekuels auch die Rotation realisiert.

        Parameter: (Das "draw-event" von vispy)
        Rückgabewerte: -

        '''

        gloo.clear(color=True, depth=True)
        #try:
        if not self._molecule==None:
                for program in self._programs:
                    program['view'] =  rotate(self._rotation, self._rotationVec).dot(translate((0,0,self._zoom)))
                    program['view'] =  rotate(self._rotation, self._rotationVec).dot(translate((0,0,self._zoom)))
                self._molecule.drawAll()
        #except Exception as ex:
        #    print 'Draw Exception', ex

    def on_resize(self, event):

        """

        Wird ausgefuert wenn das Canvas eine neue phsikalische Grosse bekommt. Fuer mehr Infos siehe activate_zoom.

        Quelle: http://vispy.readthedocs.io/en/stable/examples/tutorial/gloo/colored_cube.html

        Parameter: event mit der neuen physikalischen Groesse
        Rückgabewerte: -

        """
        self.activate_zoom()


    def activate_zoom(self):

        '''

        Diese Methode erstellt die projektion Matrix mithilfe der phsikalische Groesse des Canvas. Sie
        wird immer beim Start der Klasse, wenn das Canvas eine neue Groesse bekommt und wenn ein neues
        Molekuel erstellt wurde (es also neue Programme gibt) aufgerufen (siehe on_resize und
        _getPrograms).

        Quelle: http://vispy.readthedocs.io/en/stable/examples/tutorial/gloo/colored_cube.html

        Parameter: -
        Rückgabewerte: -

        '''

        gloo.set_viewport(0, 0, *self.physical_size)
        projection = perspective(45.0, self.size[0] / float(self.size[1]),
                                 2.0, 10.0)
        for program in self._programs:
            program['projection'] = projection
            program['projection'] = projection


    def on_timer(self, event):

        '''

        Mithilfe der on_timer Methode wird die Rotation, sowie der Uebergang zwischen zwei Molekuelen
        relisiert. Durch die Booleans _increaseDrawHorizion und _decreaseDrawHorizion wird der _drawhorizon so
        verschoben, dass wenn ein neues Molekuel visualisiert werden soll, der Nutzer das alte Molekuel
        verschwinden sieht und im Anschluss das neue aus dem nichts auftauchen sieht.


        Parameter: -
        Rückgabewerte: -

        '''

        self._rotation = self._rotation + self._rotSpeed

        if self._decreaseDrawHorizon:
            self._drawHorizon = round(self._drawHorizon + .05, 2)

            for program in self._programs:
                program['drawHorizon'] = self._drawHorizon
                program['drawHorizon'] = self._drawHorizon

            if self._drawHorizon == 1.5:
                #creating new Molecule
                rawMol = LogicMolecule(self._molName)
                proof = rawMol.createMolecule()
                if isinstance(proof, str):
                    self._master.showError(proof)
                else:
                    new_molecule = GraphicMolecule(rawMol)
                    new_molecule.processPositions()
                    self._molecule = new_molecule
                    self._getPrograms()
                    self.uploadSettingsToMol()
                    self._master.setMolecularFormula(self.getMolecularFormula())
                self._decreaseDrawHorizon = False
                self._increaseDrawHorizon = True

        if self._increaseDrawHorizon:
            self._drawHorizon = round(self._drawHorizon - .05, 2)

            for program in self._programs:
                program['drawHorizon'] = self._drawHorizon
                program['drawHorizon'] = self._drawHorizon

            if self._drawHorizon == -1.5:
                self._increaseDrawHorizon = False
        self.update()


    def on_mouse_wheel(self, event):
        print('[* Canvas: setting zoom to ' + str(self._zoom) + ' *]')
        self._setZoom(self._zoom + event.delta[1])

    def _getPrograms(self):
        self._programs = self._molecule.getPrograms()
        self.activate_zoom()

    def _setZoom(self, zoom):
        self._zoom = zoom
