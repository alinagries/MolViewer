from PyQt4 import QtGui 
import sys 
import molViewGui

                           
#Struktur aus: https://nikolak.com/pyqt-qt-designer-getting-started/


class Main(QtGui.QMainWindow, molViewGui.MolViewGui):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupGui(self)  


def main():
    app = QtGui.QApplication(sys.argv)  
    form = Main()                
    form.show()
    app.exec_()


if __name__ == '__main__':             
    main()                            


