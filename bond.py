# -*- coding: cp1252 -*-

class Bond:
    def __init__(self, a, b):

        '''
        Ein Bond-Objekt besitzt zwei Attribute, die veraendert werden koennen. Eins für einen Typ und eins für ein zweites Atom, das an der Bindung haengt.

        Parameter: instance a - atomA
                   instance b - atomB
        Rueckgabewerte: -
        '''
        self.type = None
        self.atomA = a
        self.atomB = b
        self.bSet = False


    def setType(self, typ):
        self.type = typ


    def setAtomB(self, b):
        self.atomB = b
        self.bSet = True
