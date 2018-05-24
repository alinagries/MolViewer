# -*- coding: cp1252 -*-

from graphics import *
import numpy as np




class GraphicMolecule:

    '''

    Die Klasse GraphicMolecule ist zur Erstellung eines graphischen Molekuels noetig. In ihr werden auch
    alle Aenderungen an den Einstellungen des dreidimensionalen Molekuels festgesetzt.

    '''

    def __init__(self, rawMolecule):

        """

        In der __init__ Methode dieser Klasse werden die Modell Translations und Rotations definiert.
        Des weiteren werden alle self.(...) Variablen initiiert.

        Parameter:  rawMolecule ist das logische Molekuel, dass durch die Klasse logicMolecule erstellt wurde und
                    nach dessen Vorgaben diese Klasse das graphische Molekuel erstellt
        R�ckgabewerte: -

        """

        print('[* Molecule: initializing *]')
        self._modelTranslations = [((-0.8165, 0.4714, 1.0/3.0),(0.8165, -0.4714, -1.0/3.0)),#fuer alkine an ungerader stelle
                                   ((-0.5, 0.865, 0.0), (-0.5, -0.864, 0.0), (1, 0.0, 0.0)),
                                   ((0.0, 0.9428, -1.0/3.0), (0.8165, -0.4714, -1.0/3.0), (-0.8165, -0.4714, -1.0/3.0), (0.0, 0.0, 1.0)),
                                   ((0.0, -0.9428, 1.0/3.0), (-0.8165, 0.4714, 1.0/3.0), (0.8165, 0.4714, 1.0/3.0), (0.0, 0.0, -1.0)),
                                   ((-0.84, -0.54, 0.0),(-0.04, 1, 0.0), (0.89, -0.46, 0.0)),#propanal ungerade
                                   ((0.04, -1, 0.0),(0.84, 0.54, 0.0), (-0.89, 0.46, 0.0)), #propanal gerade
                                   ((0.04, -1, 0.0), (-0.89, 0.46, 0.0),(0.84, 0.54, 0.0)),#ketone gerade
                                   ((-0.04, 1, 0.0), (0.89, -0.46, 0.0),(-0.84, -0.54, 0.0)),#ketone ungerade
                                   ((0.04, 1, 0.0), (0.89, -0.46, 0.0),(-0.84, -0.54, 0.0)),#alkanale an 1. stelle
                                   ((0.0, -0.9428, 1.0/3.0), (0.0, 0.9428, -1.0/3.0)),#ol an 1. stelle mit index 3
                                   ((0.0, -0.9428, 1.0/3.0), (0.0, 0.9428, -1.0/3.0)),
                                   ((-0.27, 0.81, 0.52), (0.57, 0.28, -0.78), (-0.8165, -0.4714, -1.0/3.0), (0.52, -0.61, 0.59)),#rotierte nebenketten
                                   ((0.27, -0.81, -0.52), (-0.57, -0.28, 0.78), (0.8165, 0.4714, 1.0/3.0), (-0.52, 0.61, -0.59)),#rotierte nebenketten
                                   ((-0.66, 0.66, -1.0/3.0), (0.91, 0.24, -1.0/3.0), (-0.24, -0.91, -1.0/3.0), (0.0, 0.0, 1.0)),
                                   ((0.66, -0.66, 1.0/3.0), (-0.91, -0.24, 1.0/3.0), (0.24, 0.91, 1.0/3.0), (0.0, 0.0, -1.0))#rotierte nebenketten
                                   ]

        self._modelRotations = [((-70.53,(2.1632,3.7461, 0.0)),(109.47,(2.1632,3.7461, 0.0))),
                                ((-90 ,(1.72, 1, 0)), (90 ,(1.72, -1, 0)), (90 ,(0,1,0))),
                                ((-109.47 ,(1.0, 0.0, 0.0)), (109.47,(2.1632,3.7461, 0.0)), (-109.47,(-2.1632,3.7461, 0.0)), (0 ,(0.0, 1.0, 0.0))),
                                ((70.53 ,(1.0, 0.0, 0.0)), (70.53,(-2.1632,-3.7461, 0.0)), (-70.53,(2.1632,-3.7461, 0.0)), (-180 ,(0.0, 1.0, 0.0))),
                                ((-90 ,(-1.95,3.07, 0)), (270 ,(4.72,0.21,0)), (270 ,(-0.83,-2.17, 0))),
                                ((-90,(-4.72,-0.21,0)),(270 ,(1.95,-3.07, 0)),  (-90 ,(0.83,2.17, 0))),
                                ((-90 ,(-4.72,-0.21,0)),  (-90 ,(0.83,2.17, 0)),(270 ,(1.95,-3.07, 0))),
                                ((-270 ,(-4.72,-0.21,0)),  (-90 ,(0.83,2.17, 0)),(90 ,(1.95,-3.07, 0))),
                                ((-270 ,(-4.72,-0.21,0)),  (270 ,(-0.83,-2.17, 0)),(-90 ,(-1.95,3.07, 0))),
                                ((70.53, (1.0, 0.0, 0.0)),((-109.47,(1.0, 0.0, 0.0)))),
                                ((-109.47, (1.0, 0.0, 0.0)),((-109.47 ,(1.0, 0.0, 0.0)))),
                                ((310,(0.81, 0.27, 0.0)), (140,(-0.28,0.57, 0.0)), (-250,(0.4714, -0.8165, 0.0)), (-300,(0.61, 0.52, 0.0))),
                                ((130,(0.81, 0.27, 0.0)), (-40,(-0.28,0.57, 0.0)), (120,(0.4714, -0.8165, 0.0)), (-480,(0.61, 0.52, 0.0))),
                                ((-109.47 ,(0.66, 0.66, 0.0)), (-109.47,(0.24, -0.91, 0.0)), (-109.47,(-0.91,0.24,  0.0)), (-180 ,(0.0, 1.0, 0.0))),
                                ((70.53 ,(0.66, 0.66, 0.0)), (70.53,(0.24, -0.91, 0.0)), (70.53,(-0.91,0.24,  0.0)), (-180 ,(0.0, 1.0, 0.0)))
                                ]


        self._rawMolecule = rawMolecule
        self._positionsProcessed = False
        self._graphics = []

        self._CAtomArchetype = C_Atom()
        self._HAtomArchetype = H_Atom()
        self._OAtomArchetype = O_Atom()

        self._zylinderArchetype = ArcheTypeZylinder()

        self._twoGraphic = TwoGraphic()
        self._threeGraphic = ThreeGraphic()

        self._borders = []

        self._atomToAtom = .1 #Bestcase: Hier steht die Bindungsgroesse/Atomgroesse.

    def getPrograms(self):
        return [self._CAtomArchetype.getProgram(), self._HAtomArchetype.getProgram(),
                self._OAtomArchetype.getProgram(), self._zylinderArchetype.getProgram(),
                self._twoGraphic.getProgram(), self._threeGraphic.getProgram()]

    def getRawMol(self):
        return self._rawMolecule

    def setAtomSizes(self, sizes):
        print('[* Molecule: setting atom sizes to ' + str(sizes) + ' (C, H, O) *]')
        for graphic in self._graphics:
            if graphic.kind == self._CAtomArchetype.kind:
                graphic.setScaling(scale((sizes[0], sizes[0], sizes[0])))
            elif graphic.kind == self._HAtomArchetype.kind:
                graphic.setScaling(scale((sizes[1], sizes[1], sizes[1])))
            elif graphic.kind == self._OAtomArchetype.kind:
                graphic.setScaling(scale((sizes[2], sizes[2], sizes[2])))

    def setBondSize(self, size):
        print('[* Molecule: setting bond size to ' + str(size) + ' *]')
        for graphic in self._graphics:
            if graphic.kind == self._zylinderArchetype.kind:
                graphic.setScaling(scale((size*0.25, size*0.25, size)))

    def setAtomColors(self, colors):
        print('[* Molecule: setting atom colors to ' + str(colors) + ' (C, H, O) *]')
        self._CAtomArchetype.setColor(colors[0])
        self._HAtomArchetype.setColor(colors[1])
        self._OAtomArchetype.setColor(colors[2])

    def setBondColor(self, color):
        print('[* Molecule: setting bond color to ' + str(color) + ' *]')
        self._zylinderArchetype.setColor(color)

    def setAtomDrawtype(self, t):
        print('[* Molecule: setting atom draw types to ' + t + ' *]')
        for graphic in self._graphics:
            if not graphic.kind == 'number' and not graphic.kind == self._zylinderArchetype.kind:
                graphic.setDrawType(t)

    def setBondDrawtype(self, t):
        print('[* Molecule: setting bond draw type to ' + t + ' *]')
        for graphic in self._graphics:
            if graphic.kind == self._zylinderArchetype.kind:
                graphic.setDrawType(t)

    def processPositions(self):

        '''

        Diese Methode ist neben _processbondPosition und _processAtomPosition einer der Drehpunkte dieser
        Klasse und kann von externen Klassen oder von dieser Klasse aufgerufen werden, wenn die Positionen und
        Rotationen der einzelnen Atome und Bindungen anhand des rawMolecules und der tranlation und rotation
        modelle berechnet werden sollen. Die Methode stoesst eine wechelseitige Rekursion zwischen
        _processbondPosition und _processAtomPosition an. Da das erste Molekuel immer
        ein C Atom ist kann man das erste Atom sofort definieren, welches dann den Ursprung der Rekursion
        darstellt. Zum ende werden noch die Positionen der "graphic" Objekte so verschoben, dass das Zentrum des
        Molekuels bei (0, 0, 0) ist.

        Parameter: -
        R�ckgabewerte: -

        '''

        print('[* Molecule: processing positions *]')

        firstAtomGraphic = StandartGraphic(self._CAtomArchetype.getProgram(), self._CAtomArchetype.getIndices(), self._CAtomArchetype.kind)
        firstAtomGraphic.setTranslation(np.array([0.0, 0.0, 0.0]))
        self._graphics.append(firstAtomGraphic)


        self._borders = [[0, 0], [0, 0], [0, 0]]
        self._processBondPosition(self._rawMolecule.getAtoms()[0], np.array([0.0, 0.0, 0.0]), None)
        self._positionsProcessed = True


        ncenter = list()
        for border in self._borders:
            ncenter.append(-(border[0]+((abs(border[0])+abs(border[1]))/2)))
        self.shiftVertices(ncenter)

    def _processBondPosition(self, aktAtom, position, originAtom):

        '''

        Diese Methode ist ein Teil der wechelseitigen Rekursion. Hier wird fuer alle Bindungen eines Atoms die
        Rotation sowie die Skalierung und die Position, also die Model-Matrix bestimmt. Fuer jedes Atom, ausser
        dem Ursprungsatom (siehe infiniter Regress), wird die _processAtomPosition aufgerufen. Des Weiteren werden hier die Zahlen im
        Falle einer Doppel- oder Dreifachbindung erstellt.

        Parameter:  Das Atom, dessen Bindungen berechnet werden sollen
                    Die Position des Atoms aktAtom
                    Das Ursprungsatom
        R�ckgabewerte: -

        '''

##        if aktAtom.getName()=='C':
##            print aktAtom, self._rawMolecule.getAtoms().index(aktAtom)
##            for bond in aktAtom.getBonds():
##                print bond, bond.atomA, bond.atomB

        trans_model = self._modelTranslations[aktAtom.getBondModel()]
        rot_model = self._modelRotations[aktAtom.getBondModel()]
        for bond in aktAtom.getBonds():
            if not bond.atomB == originAtom:
                print str(bond.type)
                index = aktAtom.getBonds().index(bond)

                bondPos = np.array(position) + np.array(trans_model[index]) * self._atomToAtom
                numberPos = np.array(position) + (np.array(trans_model[index])*1.5) * self._atomToAtom

                #print('[* Molecule: Creating bond at ' + str(bondPos) + ' *]')
                bond_rotation = rot_model[index]
                bondGraphic = StandartGraphic(self._zylinderArchetype.getProgram(), self._zylinderArchetype.getIndices(), self._zylinderArchetype.kind)
                bondGraphic.setTranslation(bondPos)
                bondGraphic.setRotation(rotate(bond_rotation[0], bond_rotation[1]))
                self._graphics.append(bondGraphic)

                if bond.type == 2:
                    twoGraphic = StandartGraphic(self._twoGraphic.getProgram(), self._twoGraphic.getIndices(), 'number')
                    twoGraphic.setTranslation(numberPos)
                    twoGraphic.setRotation(rotate(bond_rotation[0], bond_rotation[1]))
                    twoGraphic.setScaling(scale((self._atomToAtom, self._atomToAtom, self._atomToAtom)))
                    twoGraphic.setDrawType('triangles')
                    self._graphics.append(twoGraphic)

                if bond.type == 3:
                    threeGraphic = StandartGraphic(self._threeGraphic.getProgram(), self._threeGraphic.getIndices(), 'number')
                    threeGraphic.setTranslation(numberPos)
                    threeGraphic.setRotation(rotate(bond_rotation[0], bond_rotation[1]))
                    threeGraphic.setScaling(scale((self._atomToAtom, self._atomToAtom, self._atomToAtom)))
                    threeGraphic.setDrawType('triangles')
                    self._graphics.append(threeGraphic)

                self._processAtomPosition(bond, trans_model[index], position)



    def _processAtomPosition(self, originBond, vector, lastAtomPos):

        '''

        Diese Methode ist der andere Teil der wechelseitigen Rekursion. Hier wird fuer ein Atom die Position festgelegt.
        Fuer dieses Atom wird dann, wenn es nicht nur eine Bindung hat (Dann hat es nur die alte Bindung ist also ein
        "dead end"). Auserdem werden die zur Ermittlung des Zentrums des Molekuels noetigen Daten gespeichert.

        Parameter:  bindung die "origin-Bindung
                    vector (noetig zur Ermittlung der Position)
                    lastAtomPos Position des letzen Atoms
        R�ckgabewerte: -

        '''

        aktAtom = originBond.atomB
        atomPosition = lastAtomPos + np.array(vector) * 3.0 * self._atomToAtom

        for i in range(0,2):
            if (atomPosition[i] < self._borders[i][0]):
                self._borders[i][0] = atomPosition[i]
            if (atomPosition[i] > self._borders[i][1]):
                self._borders[i][1] = atomPosition[i]

        if aktAtom.getName()=='H':
            archType = self._HAtomArchetype
        elif aktAtom.getName()=='C':
            archType = self._CAtomArchetype
        elif aktAtom.getName()=='O':
            archType = self._OAtomArchetype

        atomGraphic = StandartGraphic(archType.getProgram(), archType.getIndices(), archType.kind)
        atomGraphic.setTranslation(atomPosition)
        self._graphics.append(atomGraphic)

        print '[** (' + str(atomPosition[0]) + ',' + str(atomPosition[1]) + ',' + str(atomPosition[2]) + ') **]'

        if len(aktAtom.getBonds()) > 1:
            self._processBondPosition(aktAtom, atomPosition, originBond.atomA)


    def shiftVertices(self, shiftVec):
        print('[* Molecule: shifting vertices with vector ' + str(shiftVec) + ' *]')
        for graphic in self._graphics:
            pos = graphic.getTranslation()
            newPos = (pos[0] + shiftVec[0], pos[1] + shiftVec[1], pos[2] + shiftVec[2])
            graphic.setTranslation(newPos)


    def drawAll(self):

        '''

        Diese Methode wird jede Sekunde mehrmals von der Klasse "drawController" aufgerufen um die Positionen zu
        berechnen.

        Parameter: -
        R�ckgabewerte:  'process positions first' (wenn die Positionen noch nicht berechnet wurden, kann auch
                        nichts dargestellt werden)

        '''

        if self._positionsProcessed:
            for graphic in self._graphics:
                graphic.draw()
        else:
            return 'process positions first'
