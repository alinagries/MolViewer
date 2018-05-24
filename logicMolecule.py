# -*- coding: cp1252 -*-

from collections import defaultdict
#from collections import dict
from atom import Atom
from bond import Bond

import re


class LogicMolecule:
    def __init__(self, molName):

        '''
        Erhaelt als Argument eine IUPAC-Bezeichnung eines Molek�ls - molName. Wenn der Benutzer diese in der Benutzeroberfl�che eingibt, wird ein LogicMolecule von DrawController erstellt.
        Die Molekuelsbezeichnung wird analysiert, verschiedene Atom- und Bondobjekte werden erstellt und an entsprechende Listen angehaengt,
        mit denen DrawController ein graphisches Molek�l erstellt.

        Parameter: str molName - IUPAC-Bezeichnung eines Molek�ls
        R�ckgabewerte: -
        '''

        self._name = molName.lower()

        self._suffixInformation = [("an", 1,(("C",4),("C",4))), ("en", 2,(("C",3),("C",3))), ("in", 3,(("C",2),("C",2))), ("ol", 1, (("C",4),("O",2),("H",1))), ("on",2,(("C",3),("O",1))), ("al",2,(("C",3),("O",1)))]  # wichtig reihenfolge, prioritaeten  das   2 in klammer fuer bindungenatom wie viele bindungen muss C eingehen(einfach, doppel etc)
        '''
        Enthaelt eine Liste mit Tupeln. Ist folgenderma�en aufgebaut: (Bezeichung, Bindungstyp,((1. Atom, Anzahl der M�glichen Bindungen),(2. Atom,  Anzahl der M�glichen Bindungen) usw.))
        '''

        self._suffixes = ["an", "en", "in", "ol", "on", "al"]
        self._atoms = []
        self._branchNumber = 0
        self._lenMainChain = 0
        self._functionNumber = 0
        self._bonds = []
        self._allAtoms = []
        self._description = ""
        self.molecularMass = {"C" : 12.011 , "H": 1.0079 , "O": 15.999}


    def getAtoms(self):
        '''
        Gibt eine Liste mit allen Atomen des Molekuels zur�ck.

        Parameter: -
        R�ckgabewerte: list alle Atomobjekte des Molekuels
        '''
        return self._allAtoms


    def getMolecularFormula(self):
        '''
        Gibt die Summenformel des Molekuels zur�ck. Mit einer List Comprehension wird ueber die Liste,
        die alle Atome des Molekuels enthaelt iteriert und eine neue, nur aus den Atombezeichnungen bestehende Liste erstellt.
        Mit einer weiteren List Comprehension wird ueber die names Liste iteriert, die durch set() keine doppelten Elemente mehr enthaelt.
        Dabei werden das Atomsymbol und die Anzahl des Symbols im Molekuel zusammengesetzt und die Liste alphabetisch sortiert.
        Dann werden die einzelnen Element der Liste zu einem String zusammengesetzt.

        Parameter: -
        R�ckgabewerte: str formula - Summenformel des Molekuels
        '''

        formula = ''
        mass = 0.0
        names = [atom.getName() for atom in self._allAtoms]
        c = [(name + str(names.count(name))) for name in set(names)]
        for n in sorted(c):
            formula = formula + " " + n
            mass = mass + float(n[1:]) * self.molecularMass[n[0]]
        return formula, mass


    def getDescription(self):
         '''
        Gibt eine Liste mit Erklaerungen zur Zeichnung einer Strukturformel des Molekuels zurueck.

        Parameter: -
        R�ckgabewerte: list self._description
        '''
         return self._description


    def createMolecule(self):
        '''
        Wird von DrawController aufgerufen. Erstellt ein Molekuelobjekt.
        Wenn der in der init uebergebene Molekuelname falsch ist, wird eine Fehlermeldung an den Controller zur�ckgegeben.

        Parameter: -
        R�ckgabewerte: instance sich selbst
        '''
        mainChainInformation = self._searchMainChain()
        if mainChainInformation != 0:
            analyseMainChain = self._analyseMainChain(mainChainInformation)
            if analyseMainChain == True:
                branch = self._searchBranches()
                analyseBranch = self._analyseBranch(branch)
                if analyseBranch == True:
                    self._addHydrogen(self._atoms)
                    self._description += ("Jedes normale 'C' hat vier Bindungen, die rechts, links, oben und unten vom 'C' stehen. Zeichne zuletzt an jedes 'C' diese Bindungen und daran jeweils ein 'H'. Wenn schon ein 'C' der Nebenkette oder ein 'O' einer Hydroxy-Gruppe daran haengt, dann zeichne auch nur noch drei weitere Bindungen. Wenn eine doppel oder dreifach Bindung vorliegt dann zeichne nur noch drei bzw. zwei Bindungen dazu.")
                else: return analyseBranch
            else:
                return analyseMainChain
        else:
            return "Tut uns Leid. Dieses Molekuel existiert bei uns nicht. Wir konnten keine Hauptkette finden."


    def _searchMainChain(self):
        '''
        Sucht in self._name eine Hauptkette mit Hilfe von regulaeren Ausdruecken.
        stems ist eine Liste von Tupeln. Jedes Tupel besteht aus einem moeglichen Nebenketten-Wortstamm und der dazugehoerigen Anzahl an Kohlenstoffatomen.
        Es wird fuer jeden stem mit jedem moeglichem Suffix ein regulaerer Ausdruck erstellt und mit der Methode findall in der Molek�elbezeichnung gesucht.
        Der regulaere Ausdruck ist folgenderma�en aufgebaut: Am Anfang muss ein stem stehen, in der Mitte kann etwas stehen, dass nicht 'yl' enthaelt, das ist naemlich ein Merkmal einer
        Nebenkette. Am Ende muss ein Suffix stehen. Da die Suffixe nach Prioritaet in der Suffixliste angeordnet sind, gilt nur die zuletzt gefundenene Hauptkette.
        Die gefundenen Suffixe werden in einer lokalen Liste gesammelt und zum Schluss gesetted, um Dopplungen zu vermeiden und danach wieder in eine Liste konvertiert,
        da man ueber set-Objekte nicht iterieren kann.

        Parameter: -
        R�ckgabewerte: list Liste mit der Hauptkette / int 0 - wenn nichts gefunden wurde
        '''
        stems = [("eth", 2), ("meth", 1), ("prop", 3), ("but", 4), ("pent", 5), ("hex", 6), ("hept", 7), ("oct", 8),
                   ("non", 9), ("dec", 10)]
        mainChainUpdate = []
        carbons = 0
        suffixes = []

        for stem in stems:
            for suffix in self._suffixes:
                regexM = '({0}[^(yl)]*{1})'.format(re.escape(stem[0]), re.escape(suffix))
                mainChain = re.findall(regexM, self._name)
                if mainChain != []:
                    mainChainUpdate = mainChain[0]
                    suffixes.append(suffix)
                    carbons = stem[1]

        if mainChainUpdate != []:
            self._lenMainChain = carbons
            return [mainChainUpdate, list(set(suffixes))]

        else:
            return 0


    def _analyseMainChain(self, chainInfo):
        '''
        Analysiert die Hauptkette. Sucht mit einem regulaeren Ausdruck nach Positionen, an denen besondere funktionelle Gruppen sein koennen.
        Gibt es keine Positionen in der Hauptkette, werden welche gesetzt.
        Ruft fuer jedes vorhandene Suffix amendMainChain  mit den dazugehoerigen Positionen auf.

        Parameter: list chainInfo - Aufbau: [str Hauptkette, list suffixe]
        R�ckgabewerte: Bool/String amendMainChain - nur zur Ueberpruefung von Fehlermeldungen
        '''
        suffixes = chainInfo[1]

        self._createMainChain()

        positions = re.findall('([^-]*[0-9]+[^-]*)', chainInfo[0])
        if positions == []:
                if "on" in suffixes:
                    positions = [['2']]
                elif "al" in suffixes:
                    positions = [[str(self._lenMainChain)]]
                else:
                    positions = [['1']]
        else:
            positions = [position.split(',') if len(position) > 1 else position for position in positions]
        for i in range(0,len(positions)):
            amendMainChain = self._amendMainChain(suffixes[i], positions[i])
            if not amendMainChain == 1:
                return amendMainChain
        return amendMainChain


    def _createMainChain(self):
        '''
        Erstellt die Atom-Objekte der Hauptkette und verknuepft sie durch Erstellung eines Bindungs-Objektes.

        Parameter: -
        R�ckgabewerte: -
        '''
        atomB = Atom("C", 4)
        self._atoms.append(atomB)
        if self._lenMainChain == 1:
            atomB.updateBondModel(2)
        else:
            for atom in range(0, self._lenMainChain -1):
                atomB = Atom("C", 4)
                self._atoms.append(atomB)
                atomA = self._atoms[atom]
                index = self._mainChainIndex(atomA, atomB)
                self._createBond(atomA, atomB, index, index, 1)
        self._description += ("Zeichne die Hauptkette, indem du "+ str(self._lenMainChain) +" 'C' hintereinander aufzeichnest.\n")


    def _amendMainChain(self, bondType, positions):
        '''
        Ruft fuer verschiedene funktionelle Gruppen/ Mehrfachbindungen die entsprechende Methode auf.

        Parameter: str bondType - Suffix,
                   list positions - Positionen des Suffixes in der Hauptkette
        R�ckgabewerte: Bool/String - erfolgreich/Fehlermeldung
        '''
        if not bondType == "an":
            suffix = self._suffixInformation[self._suffixes.index(bondType)]
            for pos in positions:
                pos = int(pos)
                atomA = self._atoms[pos - 1]
                if suffix[0] == "ol":
                    hydroxy = self._createHydroxy(atomA, pos)
                    if  hydroxy != True:
                        return hydroxy
                    self._description += ("Ergaenze die Hauptkette, indem du an das "+str(pos)+". Kohlenstoffatom eine Hydroxy-Gruppe zeichnest. Daf�r schreibst du ueber/unter das entsprechende 'C' einfach 'OH' und verbindest mit einem Strich das 'O' und das 'C'.\n ")

                elif suffix[0] == "al":
                    if pos == self._lenMainChain:
                        atomV = self._atoms[pos -2]
                        if pos % 2:
                            self._changeBond(atomV, atomA, None, 2, None)
                        else:
                            self._changeBond(atomV, atomA, None, 0, None)
                        self._createDoubleO(atomA, pos, suffix[0])
                    elif pos == 1:
                        double = self._createDoubleO(atomA, pos, suffix[0])
                        if double != True:
                            return double
                    else:
                        return "Tut uns Leid. Dieses Molekuel existiert bei uns nicht. Ueberpruefen Sie die Position der Aldehyd-Gruppe."
                    self._description += ("Ergaenze danach die Hauptkette, indem du an das "+str(pos)+". Kohlenstoffatom eine Aldehyd-Gruppe zeichnest. Daf�r schreibst du schraeg ueber das entsprechende 'C' einfach ein 'O' und schraeg darunter ein 'H'. Dann verbindest du mit zwei Strichen das 'O' und das 'C' und mit einem Strich das 'H' und das 'C'.\n ")

                elif suffix[0] == "on":
                    if pos == 1 or pos == self._lenMainChain:
                        return "Tut uns Leid. Dieses Molekuel existiert bei uns nicht. Ueberpruefen Sie die Position der Keto-Gruppe."
                    double = self._createDoubleO(atomA, pos, suffix[0])
                    if double != True:
                        return double
                    self._description += ("Ergaenze danach die Hauptkette, indem du an das "+str(pos)+". Kohlenstoffatom eine Keto-Gruppe zeichnest. Daf�r schreibst du ueber das entsprechende 'C' einfach ein 'O'. Dann verbindest du mit zwei Strichen das 'O' und das 'C'.\n ")

                else:
                    atomB = self._atoms[pos]
                    multipleBond = self._createMultipleBond(atomA, atomB, pos, suffix[1])
                    if  multipleBond != True:
                        return multipleBond
                    self._description += ("Ergaenze danach die Hauptkette, indem zwischen dem "+str(pos)+". und dem "+str(pos + 1)+". Kohlenstoffatom "+str(suffix[1])+" waagerechte Striche f�r die Bindungen zeichnest.\n" )

        return True


    def _createDoubleO(self, atomA, pos, suffix):
        '''
        Erstellt eine Doppelbindung zu einem O-Atom-Objekt.
        Reduziert die Anzahl der Bindugen, die atomA hat.
        Setzt fuer verschiedene Positionen verschiedene 'BondModel' , die in graphicMolecule verwendet werden.

        Parameter: instance atomA - Atom-Objekt, an das das O-Objekt mit einer Doppelbindung gebunden wird,
                   int pos - Position des O-Atoms
                   str suffix - funktionelle Gruppe
        R�ckgabewerte: Bool/String - erfolgreich/Fehlermeldung
        '''

        atomA.updateBondNumber(3)
        if suffix == "al":
            if pos == 1:
                atomA.updateBondModel(8)
            elif pos % 2:
                atomA.updateBondModel(4)
            else:
                atomA.updateBondModel(5)
        else:
            if pos % 2:
                atomA.updateBondModel(7)
            else:
                atomA.updateBondModel(6)
        indexA = self._universalIndex(atomA)
        if not indexA == "Error":
            atomO = Atom("O", 1)
            indexO = 0
            self._createBond(atomA, atomO, indexA , indexO , 2)
        else:
            return "Tut uns Leid. Dieses Molekuel existiert bei uns nicht. Ueberpruefen Sie die Anzahl der Bindungen am "+str(pos)+". Atom."
        return True


    def _createMultipleBond(self, atomA, atomB, pos, typus):
        '''
        Erstellt eine Mehrfachbindung zwischen atomA und atomB.
        Mit self._changeBond wird der typ der vorhandenen Bindung veraendert.
        Setzt fuer verschiedene Positionen verschiedene 'BondModel' , die in graphicMolecule verwendet werden.

        Parameter: instance atomA - 1. Atom-Objekt
                   instance atomB - 2. Atom-Objekt
                   int pos - Position der Bindung
                   int typus - Art der Mehrfachbindung
        R�ckgabewerte: Bool/String - erfolgreich/Fehlermeldung
        '''
        if self._bondAvailable(atomA,typus) and self._bondAvailable(atomB,typus):
            atomA.updateBondNumber(5 - typus)
            atomB.updateBondNumber(5 - typus)
        else:
            return "Tut uns Leid. Dieses Molekuel existiert bei uns nicht. Ueberpruefen Sie die Mehrfachbindungen."

        if atomA.getBondNumber() == 2 or atomB.getBondNumber() == 2:
            if pos % 2:
                atomA.updateBondModel(0)
                atomB.updateBondModel(0)
                self._changeBond(atomA, atomB, None, 1, typus)
                if pos != (self._lenMainChain -1):
                    atomN = self._atoms[pos + 1]
                    self._changeBond(atomN, atomB, None, 0, None)
            else:
                atomA.updateBondModel(10)
                atomB.updateBondModel(10)
                self._changeBond(atomA, atomB, None, 0, typus)
                if pos != (self._lenMainChain -1):
                    atomN = self._atoms[pos + 1]
                    self._changeBond(atomN, atomB, None, 1, None)
                    atomB.lock(0)

        elif atomA.getBondNumber() > 2:
            if pos == 1:
                atomA.updateBondModel(8)
                atomB.updateBondModel(6)
            elif pos % 2:
                atomA.updateBondModel(7)
                atomB.updateBondModel(6)
            else:
                atomA.updateBondModel(6)
                atomB.updateBondModel(7)
            self._changeBond(atomA, atomB, None, None, typus)

        else:
            return "Tut uns Leid. Dieses Molekuel existiert bei uns nicht. Ueberpruefen Sie die Mehrfachbindungen."
        return True


    def _createHydroxy(self, atomA, pos):
        '''
        Erstellt eine Hydroxy-Gruppe an atomA.
        Atom O wird mit einem Index an das C-Atom gehangen und mit dem anderen an ein neu erstelltes H-Atom.
        Fuer verschiedene Positionen der Hydroxy-Gruppe wird jeweils ein anderes Bindungsmodel und andere Indeizes gebraucht.

        Parameter: instance atomA - Atom-Objekt, an das die Hydroxy-Gruppe gebunden werden soll, int pos - Position der Hydroxy-Gruppe
        R�ckgabewerte: Bool/String - erfolgreich/Fehlermeldung
        '''

        indexA = self._universalIndex(atomA)
        if not indexA == "Error":
            if pos == 1 and indexA == 1:
                atomO = Atom("O", 2)
                indexO_1 = 1
                indexO_2 = 0
                atomO.updateBondModel(9)
            elif not pos % 2:
                atomO = Atom("O", 2)
                indexO_1 = 0
                indexO_2 = 1
                atomO.updateBondModel(10)
            else:
                atomO = Atom("O", 2)
                indexO_1 = 1
                indexO_2 = 0
            self._createBond(atomA, atomO, indexA , indexO_1, 1)
            atomH = Atom("H", 1)
            self._createBond(atomO, atomH, indexO_2, 0, 1)
        else:
            return "Tut uns Leid. Dieses Molekuel existiert bei uns nicht. Ueberpruefen Sie die Position des Hydroxy-Gruppe."
        return True


    def _searchBranches(self):
        '''
        Sucht in self._name nach Nebenketten mit Hilfe eines regulaeren Ausdruckes, der folgenderma�en aufgebaut ist:
        Am Anfang darf etwas stehen, dass kein Buchstabe ist, dann duerfen Buchstaben kommen,
        dann muss der Stamm der Nebenkette stehen, dann duerfen wieder Buchstaben kommen und zum Schluss muss 'yl' stehen.
        Mit proofBranches werden Dopplungen vermieden. Zum Beispiel findet der Ausdruck sowohl fuer methyl als auch fuer ethyl den gleichen String, weil das Wort ethyl in methyl steckt.


        Parameter: -
        R�ckgabewerte: list allBranches - alle Nebenketten als Tupel mit Stamm
        '''

        allBranches = []
        proofBranches = []
        stems = [("meth", 1), ("eth", 2), ("prop", 3), ("but", 4), ("pent", 5), ("hex", 6), ("hept", 7), ("oct", 8),("non", 9), ("dec", 10)]
        for stem in stems:
            regexB = '([^a-z]*[a-z]*{0}[a-z]*yl)'.format(re.escape(stem[0]))
            branch = re.findall(regexB, self._name)

            if branch != []:
                if not branch[0] in proofBranches:
                    proofBranches.append(branch[0])
                    branch = (branch[0], stem[1])
                    allBranches.append(branch)
        return allBranches


    def _analyseBranch(self, chainInfo):
        '''
        Sucht mit einem regulaeren Ausdruck nach Positionen, an denen die Nebenketten haengen.
        Gibt es keine Positionen, wird Positionen auf 1 gestetz.


        Parameter: list chainInfo - Liste von Nebenketten, bestehend aus Nebenkettenbezeichnung und Wortstamm
        R�ckgabewerte: Bool/String - erfolgreich/Fehlermeldung
        '''
        for chain in chainInfo:
            lenBranch = chain[1]
            positions=(re.findall('[0-9]+', chain[0]))
            if positions == []:
                positions = ['1']
            for position in positions:
                if not positions.count(position) > 2:
                    if not int(position) > self._lenMainChain:
                        branch = self._createBranch(position, lenBranch)
                        if branch != True:
                            return branch
                    else:
                        return "Tut uns Leid. Dieses Molekuel existiert bei uns nicht. Ueberpruefen Sie die Nebenkettenposition "+position+" ."
                else:
                    return "Tut uns Leid. Dieses Molekuel existiert bei uns nicht. Sie haengen zu viele Nebenketten an eine Position. Versuchen Sie eine groe�ere Hauptkette zu waehlen."
        return True


    def _createBranch(self, position, lenBranch):
        '''
        Erstellt alle Atom-Objekte der Nebenkette. Der Index variiert je nachdem, wo die Nebenkette liegt.
        An die Statusabfragen sind genauere Kommentare geschrieben.

        Parameter: str position - Position in der Hauptkette, an der die Nebenkette liegen soll.
        R�ckgabewerte: Bool/String  - nur zur Ueberpruefung von Fehlermeldungen
        '''
        self._branchNumber += 1
        branch = []
        position = int(position)
        atomA = self._atoms[position-1]
        firstSideCarbon = Atom("C", 4)
        branch.append(firstSideCarbon)
        if lenBranch > 1 or (position != 3 and position != 7 and position % 4 != 0):
            status = self._findStatus(atomA, position)
        else:
            status = self._statusLastAtom(atomA, position)
        if type(status) == str:
            return status
        indexA = self._universalIndex(atomA)
        indexC = self._branchIndex(firstSideCarbon, status)
        self._createBond(atomA, firstSideCarbon, indexA, indexC, 1)  # C wird an Hauptkette rangehangen

        for bPos in range(0, (lenBranch -1)):  #  -1 weil oben schon eins erstellt wurde
            atomB = Atom("C", 4)
            branch.append(atomB)
            atomC = branch[bPos]
            # if bPos == lenBranch -2 and (position % 4 == 0 or position == 3 or position == 7):
            #     status2 = self._statusLastAtom(atomA, position)
            #     indexB = self._longBranchIndex(atomB, atomC, status2)
                # if type(status2) == str:
                #     return status
            #else:
            indexB = self._longBranchIndex(atomB, atomC, status)
            indexC = self._universalIndex(atomC)
            self._createBond(atomC, atomB, indexC, indexB, 1)

        self._addHydrogen(branch)
        self._description += ("Zeichne jetzt ueber/unter das "+str(position)+". 'C' der Hauptkette "+str(lenBranch)+" weitere/s 'C' und verbinde das 'C', das direkt ueber dem der Hauptkette steht mit diesem." )
        return True

    def _findStatus(self, atomA, position):
        '''
        Teilt dem Atom den richtigen Status zu, der nacher das BondModel bestimmt.

        Parameter: instance atomA - Atom
        R�ckgabewerte: Bool/String  - nur zur Ueberpruefung von Fehlermeldungen
                        int - Status
        '''
        if not atomA.isLocked(2) and not position % 2: #normale Nebenkette und gerades C-Atom, an dem sie liegt.
            status = 1
        elif atomA.isLocked(2) and position % 2: #2.Nebenkette an ungeraden C-atom
            status = 4
        elif atomA.isLocked(2) and not atomA.isLocked(3): # 2. Nebenkette an geradem C-atom
            status = 2
        elif position % 2: #ungerade, anderes Modell und Index
            status = 3
        else:
            return "Tut uns Leid. Dieses Molekuel existiert bei uns nicht. Es gibt zu viele Nebenketten an Position "+str(position)+" ."
        return status

    def _statusLastAtom(self, atomA, position):
        '''
        Teilt dem letzten Atom einer Nebenkette den richtigen Status zu, der nacher das BondModel bestimmt.
        Vorrübergehende Funktion, bei Ausbau der Rotation nicht mehr wichtig. Nur fuer Positionen, die rotiert werden muessen, d.h., 4,8,3,7

        Parameter: instance atomA - Atom
        R�ckgabewerte: Bool/String  - nur zur Ueberpruefung von Fehlermeldungen
                        int - Status
        '''

        #unterscheiden in 2. an geradem und 2. an ungeradem c

        if not atomA.isLocked(2) and position % 2 == 0 and position % 4 == 0: #erste nk , position: 4,8 --> rotiert
            status = 5
        elif not atomA.isLocked(3) and position % 2 == 0 and position % 4 == 0: # 2. nk an 4 oder 8 --> rotiert
            status = 7
        elif not atomA.isLocked(2) and (position == 3 or position == 7) : #erste nk
            status = 6
        elif not atomA.isLocked(3) and (position == 3 or position == 7 ): #2. nk an 3 oder 7 --> rotiert
            status = 8
        else:
            return "Tut uns Leid. Dieses Molekuel existiert bei uns nicht. Es gibt zu viele Nebenketten an Position "+str(position)+" ."
        return status

    def _addHydrogen(self, atoms):
        '''
        Erstellt f�r jede nicht gelockte Bindung ein Atom-Objekt.

        Parameter: list atoms - Atome, an die Wasserstoff rangehangen werden soll
        R�ckgabewerte: -
        '''

        for atom in atoms:
            for pos in range(0,4):
                availableIndex = self._universalIndex(atom)
                if availableIndex != "Error":
                    atomH = Atom("H", 1)
                    self._createBond(atom, atomH, availableIndex, 0, 1)
                else:
                    break


    def _branchIndex(self, atom, status):
        '''
        Gibt einen Index aus, mit dem das erste Atom der Nebenkette an die Hauptkette gebunden werden kann.

        Parameter: instance atom
                   int status - der Index ist anhaenig von der Position der Nebenkette
        R�ckgabewerte: int index
        '''

        if status == 1:
            index = 2
            atom.lock(2)
            atom.updateBondModel(2)
            return index
        elif status == 2:
            index = 3
            atom.lock(3)
            atom.updateBondModel(2)
            return index
        elif status == 3:
            index = 2
            atom.lock(2)
            atom.updateBondModel(3)
            return index
        elif status == 5:
            index = 2
            atom.lock(2)
            atom.updateBondModel(11) #oben
            return index
        elif status == 6:
            index = 2
            atom.lock(2)
            atom.updateBondModel(12) # unten
            return index
        elif status == 7:
            index = 3
            atom.lock(3)
            atom.updateBondModel(13)
            return index
        elif status == 8:
            index = 3
            atom.lock(3)
            atom.updateBondModel(14) 
            return index
        else:
            index = 3
            atom.lock(3)
            atom.updateBondModel(3)
            return index


    def _longBranchIndex(self,atomB, atomC, status):
        '''
        Gibt einen Index aus, mit dem atomB der Nebenkette an atomC gebunden werden kann.

        Parameter: instance atomB
                   instance atomC
                   int status - der Index ist abhaenig von der Position der Nebenkette
        R�ckgabewerte: int indexB
        '''

        if status == 1 or status == 4:
            if atomC.isLocked(2) and not atomC.isLocked(3):
                atomB.updateBondModel(3)
                indexB = 3
                atomB.lock(3)
            elif atomC.isLocked(3) and not atomC.isLocked(2):
                atomB.updateBondModel(2)
                indexB = 2
                atomB.lock(2)
            else:
                pass
            return indexB
        # if status == 5 or status == 6:
        #     if atomC.isLocked(2) and not atomC.isLocked(3):
        #         atomB.updateBondModel(12)
        #         indexB = 0
        #         atomB.lock(0)
        #     elif atomC.isLocked(3) and not atomC.isLocked(2):
        #         atomB.updateBondModel(11)
        #         indexB = 2
        #         atomB.lock(2)
        #     else:
        #         pass
        #     return indexB
        else:
            if atomC.isLocked(2) and not atomC.isLocked(3):
                atomB.updateBondModel(2)
                indexB = 3
                atomB.lock(3)
            elif atomC.isLocked(3) and not atomC.isLocked(2):
                atomB.updateBondModel(3)
                indexB = 2
                atomB.lock(2)
            else:
                pass
            return indexB


    def _bondAvailable(self, atom, typus):
        '''
        Prueft, ob atom noch fuer den typus freie Bindungen hat.

        Parameter: instance atom
        R�ckgabewerte: Bool
        '''
        merke = [0,0,0,0]
        counter = 0
        for i in range(1,typus):
            if not atom.isLocked(2):
                merke[2] = 1
                atom.lock(2)
                counter += 1
            elif not atom.isLocked(3):
                merke[3] = 1
                atom.lock(3)
                counter += 1
            elif not atom.isLocked(0):
                merke[0] = 1
                atom.lock(0)
                counter += 1
            elif not atom.isLocked(1):
                merke[1] = 1
                atom.lock(1)
                counter += 1

        if counter == (typus -1):
            for a in range(len(merke)):
                if merke[a] == 1:
                    atom.release(a)
            return 1

    def _mainChainIndex(self, atomA, atomB):
        '''
        Gibt einen Index zur�ck, mit dem atomA der Hauptkette an atomB gebunden werden kann.

        Parameter: instance atomA
                   instance atomB
        R�ckgabewerte: index
        '''

        if not atomA.isLocked(0) and not atomB.isLocked(0):
            index = 0
            atomA.lock(0)
            atomB.lock(0)
            atomA.updateBondModel(2)
            atomB.updateBondModel(3)
        elif not atomA.isLocked(1)and not atomB.isLocked(1):
            index = 1
            atomA.lock(1)
            atomB.lock(1)
            atomA.updateBondModel(3)
            atomB.updateBondModel(2)
        else:
            return "Error"
        return index


    def _universalIndex(self, atom):
        '''
        Gibt den Index der Bindung zur�ck, die noch frei ist.

        Parameter: instance atom
        R�ckgabewerte: index
        '''

        if not atom.isLocked(2):
            index = 2
            atom.lock(2)
        elif not atom.isLocked(3):
            index = 3
            atom.lock(3)
        elif not atom.isLocked(0):
            index = 0
            atom.lock(0)
        elif not atom.isLocked(1):
            index = 1
            atom.lock(1)
        else:
            return "Error"
        return index


    def _createBond(self, atomA, atomB, indexA, indexB, typus):
        '''
        Erstellt eine Bindung, indem es mit configureBond die self._bonds Liste im Atom-Objekt updatet.
        Fuegt die Atome, die noch nicht in der self._allAtoms Liste sind hinzu.

        Parameter:  atomA instance
                    atomB instance
                    indexA int
                    indexB int
                    typus int
        R�ckgabewerte: -
        '''
        self._bonds.append((atomA, atomB, indexA, indexB, typus))

        atomA.configureBond(indexA, Bond.setAtomB, atomB)
        atomB.configureBond(indexB, Bond.setAtomB, atomA)
        atomB.configureBond(indexB, Bond.setType, typus)
        atomA.configureBond(indexA, Bond.setType, typus)

        if not atomA in self._allAtoms:
            self._allAtoms.append(atomA)
        if not atomB in self._allAtoms:
            self._allAtoms.append(atomB)


    def _changeBond(self, atomA, atomB, indexA, indexB, typus):
        '''
        Aktualisiert eine Bindung. Kuemmert sich um die Sperrung und Freigabe von veraenderten Indizes.
        Aktualisiert die self._bonds Liste.
        Aktualisiert mit configureBond auch die self._bonds Liste im Atom-Objekt.


        Parameter:  atomA instance
                    atomB instance
                    indexA int
                    indexB int
                    typus int
        R�ckgabewerte: -
        '''

        for bond in self._bonds:
            if atomA in bond and atomB in bond:
                bondIndex = self._bonds.index(bond)
                args = locals()
                argsList = [args['atomA'], args['atomB'], args['indexA'], args['indexB'], args['typus']] #bond wird nachkonstruiert

                for arg in range(2, len(argsList)):
                    if argsList[arg] == None:
                        argsList[arg] = bond[arg]
                    else:
                        if arg == 2:
                            indOld = bond[arg]
                            atomA.release(indOld)
                            atomA.lock(indexA)
                        elif arg == 3:
                            indOld = bond[arg]
                            atomB.release(indOld)
                            atomB.lock(indexB)

                self._bonds[bondIndex] = (atomA, atomB, argsList[2], argsList[3],  argsList[4])


                atomA.configureBond(argsList[2], Bond.setAtomB, atomB)
                atomB.configureBond(argsList[3], Bond.setAtomB, atomA)
                atomB.configureBond(argsList[3], Bond.setType, argsList[4])
                atomA.configureBond(argsList[2], Bond.setType, argsList[4])
