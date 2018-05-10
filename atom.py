# -*- coding: cp1252 -*-

from collections import defaultdict
from bond import Bond


class Atom:
    def __init__(self, name, bondNumber):

        '''
        Erhaelt einen Namen und eine Anzahl, die angibt wie viele Bindungen es eingehen kann.
        Es wird eine dem Wert entsprechende Anzahl an Bond-Objekten erzeugt und an die Liste self._bonds angehangen.

        Parameter: str name - z.B. "C"
        Rueckgabewerte: -
        '''

        self._name = name
        self._bondNumber = bondNumber
        self._bonds = []
        self._locks = dict()
        self._bondModel = 0
        for bond in range(0,self._bondNumber):
            self._bonds.append(Bond(self, None))
            self._locks[bond] = 0


    def configureBond(self, index, method, parameter):
        Bond = self._bonds[index]
        method(Bond, parameter)


    def lock(self, position):
        self._locks[position] = 1


    def release(self, position):
        self._locks[position] = 0


    def isLocked(self, position):
        try:
            return self._locks[position]
        except: return 1


    def getBondNumber(self):
        return self._bondNumber


    #def updateBondNumber(self, bondNumber):
    #    '''
    #    Loescht soviele Bindungen, bis bondNumber erreicht ist.
    #    Setzt self._bondNumber auf bondNumber.
#
#        Parameter: int bondNumber
#        Rueckgabewerte: -
#        '''
#        if not self._bondNumber == bondNumber or self._bondNumber < 2:
#
#            num = (self._bondNumber - bondNumber)
#            for i in range(self._bondNumber -1, -1 , -1):
#                if not self.isLocked(i):
#                    del self._bonds[i]
#                    try:
#                        del self._locks[i]
#                    except:
#                        pass
#                    num -= 1
#                    if num < 1:
#                        break
#
#            self._bondNumber = bondNumber



    def updateBondNumber(self, typus):
        '''
        Loescht soviele Bindungen, bis bondNumber erreicht ist.
        Setzt self._bondNumber auf bondNumber.

        Parameter: int bondNumber
        Rueckgabewerte: -
        '''
        bondNumber = typus
        if self._bondNumber >= bondNumber:

            num = (self._bondNumber - bondNumber)
            for i in range(self._bondNumber -1, -1 , -1):
                if not self.isLocked(i):
                    del self._bonds[i]
                    try:
                        del self._locks[i]
                    except:
                        pass
                    num -= 1
                    if num < 1:
                        break

            self._bondNumber = bondNumber


    def updateBondModel(self, bond_model):
        self._bondModel = bond_model


    def getBondModel(self):
        return self._bondModel


    def getBonds(self):
        return self._bonds


    def getName(self):
        return self._name
