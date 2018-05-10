# -*- coding: utf-8 -*-
from PIL import ImageGrab
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from drawController import DrawController
import sys
from datetime import datetime

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class MolViewGui(object):
    def setupGui(self, Dialog):
        Dialog.setObjectName(_fromUtf8("MolViewer"))
        Dialog.resize(1914, 963)
        Dialog.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(2, 4, 35)")


        self.observers = []

        self.molekuel_frame = QtGui.QFrame(Dialog)
        self.molekuel_frame.setGeometry(QtCore.QRect(330, 40, 1465, 850))
        self.molekuel_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.molekuel_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.molekuel_frame.setObjectName(_fromUtf8("molekuel_frame"))


        self.molekuel_widget = QtGui.QWidget(self.molekuel_frame)
        self.molekuel_widget.setGeometry(QtCore.QRect(10, 10, 1465, 850))
        self.molekuel_widget.setObjectName(_fromUtf8("molekuel_widget"))
        self.molCanvas = DrawController(self.molekuel_widget, self)
        #self.molekuel_widget.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(255, 255, 255)")



        self.einstellungen_frame = QtGui.QFrame(Dialog)
        self.einstellungen_frame.setGeometry(QtCore.QRect(20, 40, 271, 741))
        self.einstellungen_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.einstellungen_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.einstellungen_frame.setObjectName(_fromUtf8("einstellungen_frame"))
        self.einstellungen_frame.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(2, 4, 35)")


        self.sumLabel = QtGui.QLabel(self.einstellungen_frame)
        self.sumLabel.setGeometry(QtCore.QRect(165,80, 110, 16))
        self.sumLabel.setObjectName(_fromUtf8("sumLabel"))

        self.sumLabel2 = QtGui.QLabel(self.einstellungen_frame)
        self.sumLabel2.setGeometry(QtCore.QRect(10,80, 120, 16))
        self.sumLabel2.setObjectName(_fromUtf8("sumLabel2"))

        self.massLabel = QtGui.QLabel(self.einstellungen_frame)
        self.massLabel.setGeometry(QtCore.QRect(165,110, 110, 16))
        self.massLabel.setObjectName(_fromUtf8("massLabel"))

        self.massLabel2 = QtGui.QLabel(self.einstellungen_frame)
        self.massLabel2.setGeometry(QtCore.QRect(10,110, 145, 16))
        self.massLabel2.setObjectName(_fromUtf8("massLabel2"))

        self.label_4 = QtGui.QLabel(self.einstellungen_frame)
        self.label_4.setGeometry(QtCore.QRect(165, 370, 61, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))

        self.pushButton = QtGui.QPushButton(self.einstellungen_frame)
        self.pushButton.setGeometry(QtCore.QRect(200, 30, 70, 25))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.clicked.connect(self.new_molecule)
        self.pushButton.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(45, 65, 90)")



        self.desButton = QtGui.QPushButton(self.einstellungen_frame)
        self.desButton.setGeometry(QtCore.QRect(10, 140, 200, 25))
        self.desButton.setObjectName(_fromUtf8("desButton"))
        self.desButton.clicked.connect(self.showDescription)
        self.desButton.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(45, 65, 90)")


        self.atomOptions = QtGui.QPushButton(self.einstellungen_frame)
        self.atomOptions.setGeometry(QtCore.QRect(10, 230, 80, 28))
        self.atomOptions.setObjectName(_fromUtf8("atomOptions"))
        self.atomOptions.clicked.connect(self.openAtomOptions)
        self.atomOptions.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(45, 65, 90)")


        self.bondOptions = QtGui.QPushButton(self.einstellungen_frame)
        self.bondOptions.setGeometry(QtCore.QRect(110, 230, 130, 28))
        self.bondOptions.setObjectName(_fromUtf8("bondOptions"))
        self.bondOptions.clicked.connect(self.openBondOptions)
        self.bondOptions.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(45, 65, 90)")


        self.infoButton = QtGui.QPushButton(Dialog)
        self.infoButton.setGeometry(QtCore.QRect(10, 10, 30, 30))
        self.infoButton.setObjectName(_fromUtf8("infoButton"))
        icon = QIcon('info.gif')
        self.infoButton.setIcon(icon)
        self.infoButton.setIconSize(QSize(22,22))
        self.infoButton.clicked.connect(self.show_info)
        self.infoButton.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(45, 65, 90)")


        self.shotButton = QtGui.QPushButton(Dialog)
        self.shotButton.setGeometry(QtCore.QRect(60, 10, 30, 30))
        self.shotButton.setObjectName(_fromUtf8("shotButton"))
        icon = QIcon('screen.gif')
        self.shotButton.setIcon(icon)
        self.shotButton.setIconSize(QSize(22, 22))
        self.shotButton.clicked.connect(self.shoot)
        self.shotButton.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(45, 65, 90)")


        self.checkBox_3 = QtGui.QCheckBox(self.einstellungen_frame)
        self.checkBox_3.setGeometry(QtCore.QRect(10, 290, 120, 23))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.checkBox_3.stateChanged.connect(lambda: self.notifyObservers('General'))

        self.slider_xR = QtGui.QSlider(QtCore.Qt.Horizontal,self.einstellungen_frame)
        self.slider_xR.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slider_xR.setGeometry(10, 320, 111, 31)
        self.slider_xR.valueChanged[int].connect(lambda: self.notifyObservers('General'))


        self.slider_yR = QtGui.QSlider(QtCore.Qt.Horizontal,self.einstellungen_frame)
        self.slider_yR.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slider_yR.setGeometry(10, 370, 111, 31)
        self.slider_yR.valueChanged[int].connect(lambda: self.notifyObservers('General'))


        self.slider_zR = QtGui.QSlider(QtCore.Qt.Horizontal,self.einstellungen_frame)
        self.slider_zR.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slider_zR.setGeometry(10, 420, 111, 31)
        self.slider_zR.valueChanged[int].connect(lambda: self.notifyObservers('General'))

        self.checkBox_3.setChecked(True)


        self.checkBox_6 = QtGui.QCheckBox(self.einstellungen_frame)
        self.checkBox_6.setGeometry(QtCore.QRect(10, 470, 131, 23))
        self.checkBox_6.setObjectName(_fromUtf8("checkBox_6"))
        self.checkBox_6.setChecked(True)

        self.label_3 = QtGui.QLabel(self.einstellungen_frame)
        self.label_3.setGeometry(QtCore.QRect(160, 320, 61, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.label_5 = QtGui.QLabel(self.einstellungen_frame)
        self.label_5.setGeometry(QtCore.QRect(160, 420, 61, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))

        self.lineEdit = QtGui.QLineEdit(self.einstellungen_frame)
        self.lineEdit.setGeometry(QtCore.QRect(10, 30, 171, 20))
        self.lineEdit.setStyleSheet(_fromUtf8("IUPAC NAME"))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))

        self.label_7 = QtGui.QLabel(self.einstellungen_frame)
        self.label_7.setGeometry(QtCore.QRect(10, 185, 191, 31))
        self.label_7.setTextFormat(QtCore.Qt.AutoText)
        self.label_7.setObjectName(_fromUtf8("label_7"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.slider_xR.setValue(20)
        self.slider_yR.setValue(10)

        self.bondSettings = dict()
        self.bondSettings['Size'] = .14
        self.bondSettings['Color'] = (.5, .5, .5)
        self.bondSettings['Viz'] = 'triangles'

        self.atomSettings = dict()
        self.atomSettings['CColor'] = (0.0, 0.0, 0.0)
        self.atomSettings['CSize'] = .11
        self.atomSettings['HColor'] = (1.0, 1.0, 1.0)
        self.atomSettings['HSize'] = .08
        self.atomSettings['OColor'] = (1.0, 0.0, 0.0)
        self.atomSettings['OSize'] = .11
        self.atomSettings['Viz'] = 'triangles'

    #def getter(widget):
        #x = self.molekuel_widget.winfo_rootx() + widget.winfo_x()
        #y = self.molekuel_widget.winfo_rooty() + widget.winfo_y()
        #x1 = x + widget.winfo_width()
        #y1 = y + widget.winfo_height()
        #ImageGrab.grab().crop((x, y, x1, y1)).save("file path here")

    def shoot(self):
        #x = self.molekuel_widget.winfo_rootx() + self.molekuel_widget.winfo_x()
        #y = self.molekuel_widget.winfo_rooty() + self.molekuel_widget.winfo_y()
        #x1 = x + self.molekuel_widget.winfo_width()
        #y1 = y + self.molekuel_widget.winfo_height()
        pic = ImageGrab.grab((350, 125, 1590, 860))
        filename = QtGui.QFileDialog.getSaveFileName(self, 'Molekuel Speichern', '/path/to/default/directory', selectedFilter='*.jpg')
        pic.save(str(filename), 'jpeg')


    def registerObserver(self, observer):
        self.observers.append(observer)

    def unregisterObserver(self, observer):
        self.observers.remove(observer)

    def notifyObservers(self, dataType):
        for observer in self.observers:
            observer.notify(dataType)

    def getAtomSettings(self):
        return self.atomSettings

    def getBondSettings(self):
        return self.bondSettings

    def getGeneralSettings(self):
        return (self.checkBox_3.isChecked(), (self.slider_xR.value(), self.slider_yR.value(), self.slider_zR.value()))

    def setBondSettings(self, x):
        self.bondSettins = x
        self.notifyObservers('Bond')

    def setAtomSettings(self, x):
        self.atomSettings = x
        self.notifyObservers('Atom')

    def openAtomOptions(self):
        self.setEnabled(False)
        self.w = Ui_AtomOptions(self)
        self.w.setupUi(self.w)
        self.w.show()

    def openBondOptions(self):
        self.setEnabled(False)
        self.w = Ui_BondOptions(self)
        self.w.setupUi(self.w)
        self.w.show()



    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "MolViewer", None))
        self.label_4.setText(_translate("Dialog", "Y Rot.", None))
        self.sumLabel2.setText(_translate("Dialog", "Summenformel:", None))
        self.massLabel2.setText(_translate("Dialog", "Molekülmasse(Da):", None))
        self.pushButton.setText(_translate("Dialog", "Erstelle", None))
        self.infoButton.setText(_translate("Dialog", "", None))
        self.shotButton.setText(_translate("Dialog", "", None))
        self.desButton.setText(_translate("Dialog", "Zur Strukturformel", None))
        self.atomOptions.setText(_translate("Dialog", "Atome", None))
        self.bondOptions.setText(_translate("Dialog", "Bindungen", None))
        self.checkBox_3.setText(_translate("Dialog", "Rotation", None))
        self.checkBox_6.setText(_translate("Dialog", "Übergang", None))
        self.label_3.setText(_translate("Dialog", "X Rot.", None))
        self.label_5.setText(_translate("Dialog", "Z Rot.", None))
        self.lineEdit.setToolTip(_translate("Dialog", "<html><head/><body><p>Geben sie hier den IUPAC Namen ein.</p></body></html>", None))
        self.lineEdit.setWhatsThis(_translate("Dialog", "<html><head/><body><p>IUPAC NAME</p></body></html>", None))
        self.lineEdit.setPlaceholderText(_translate("Dialog", "IUPAC-Namen eingeben", None))
        self.label_7.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600;\">Optionen</span></p></body></html>", None))


    def keyPressEvent(self, e):
        print e.key(),'!!!'
        if e.key() == 16777220:
            self.new_molecule()
        if e.key() == 82:
            self.checkBox_3.setChecked(not self.checkBox_3.isChecked())
        if e.key() == 85:
            self.checkBox_6.setChecked(not self.checkBox_6.isChecked())
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()


    def new_molecule(self):
        self.notifyObservers('Atom')
        self.notifyObservers('Bond')
        self.notifyObservers('General')
        mol_name = str(self.lineEdit.text())
        self.molCanvas.newMolecule(mol_name, not self.checkBox_6.isChecked())

    def setMolecularFormula(self, x):
        self.sumLabel.setText(_translate("Dialog",x[0] , None))
        self.massLabel.setText(_translate("Dialog", str(x[1]), None))


    def show_info(self):#Struktur uebernommen aus: https://www.tutorialspoint.com/pyqt/pyqt_qmessagebox.htm
       msg = QMessageBox()
       msg.setIcon(QMessageBox.Information)
       msg.setText("Guten Tag. Folgende Vorgaben sind bei der Eingabe eines IUPAC-Namens zu beachten:")
       msg.setInformativeText("1. Der Molekuel-Name folgt der systematischen Nomenklatur.\n2. Die Hauptkette kann aus hoechstens zehn Kohlenstoffatomen bestehen.\n3. Bei mehr als einer Nebenkette, Hydroxygruppe, Mehrfachbindung, Aldehyd-Gruppe oder Keto-Gruppe muessen die Positionen angegeben werden.\n4. Die Positionen werden direkt vor die jeweilige funktionelle Gruppe oder Mehrfachbindung geschrieben.\n5. Die Positionen werden links und rechts mit einem Bindestrich eingegrenzt und einzelne durch Kommata getrennt.  ")
       msg.setWindowTitle("Informationen")
       msg.setStandardButtons(QMessageBox.Ok)
       retval = msg.exec_()

    def showError(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Ein Fehler ist aufgetreten.")
        msg.setInformativeText(text)
        msg.setWindowTitle("Fehlermeldung")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()

    def showDescription(self):
        des = self.molCanvas.getDescription()
        msg = QMessageBox()
        msg.setText("So kannst auch du eine Strukturformel zeichnen:")
        msg.setInformativeText(des)
        msg.setWindowTitle("Strukturformel")
        msg.setStandardButtons(QMessageBox.Ok)
        retval = msg.exec_()


class Ui_AtomOptions(QtGui.QMainWindow, object):
    def __init__(self, parent):
        super(self.__class__, self).__init__()
        self.parent = parent

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(601, 313)
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 60, 61, 16))
        self.label.setObjectName(_fromUtf8("label"))


        self.slider0 = QtGui.QSlider(QtCore.Qt.Horizontal, Form)
        self.slider0.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slider0.setGeometry(400, 60, 111, 31)


        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(400, 30, 91, 20))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_8 = QtGui.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(240, 30, 101, 20))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.radioButton = QtGui.QRadioButton(Form)
        self.radioButton.setGeometry(QtCore.QRect(310, 270, 121, 20))
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.radioButton_2 = QtGui.QRadioButton(Form)
        self.radioButton_2.setGeometry(QtCore.QRect(20, 270, 121, 20))
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.radioButton_3 = QtGui.QRadioButton(Form)
        self.radioButton_3.setGeometry(QtCore.QRect(160, 270, 121, 20))
        self.radioButton_3.setObjectName(_fromUtf8("radioButton_3"))

        self.slider1 = QtGui.QSlider(QtCore.Qt.Horizontal, Form)
        self.slider1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slider1.setGeometry(240, 60, 111, 31)

        self.slider2 = QtGui.QSlider(QtCore.Qt.Horizontal, Form)
        self.slider2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slider2.setGeometry(100, 60, 111, 31)


        self.pushButtonColor = QtGui.QPushButton(Form)
        self.pushButtonColor.setGeometry(QtCore.QRect(480, 250, 180, 25))
        self.pushButtonColor.setObjectName(_fromUtf8("pushButton"))
        self.pushButtonColor.clicked.connect(self.color_picker)



        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 150, 81, 23))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEdit_3 = QtGui.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(100, 180, 51, 23))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.label_9 = QtGui.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(100, 30, 91, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.lineEdit_2 = QtGui.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 150, 51, 23))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.lineEdit_4 = QtGui.QLineEdit(Form)
        self.lineEdit_4.setGeometry(QtCore.QRect(100, 120, 51, 23))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.lineEdit_5 = QtGui.QLineEdit(Form)
        self.lineEdit_5.setGeometry(QtCore.QRect(240, 180, 51, 23))
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.lineEdit_6 = QtGui.QLineEdit(Form)
        self.lineEdit_6.setGeometry(QtCore.QRect(240, 120, 51, 23))
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))
        self.lineEdit_7 = QtGui.QLineEdit(Form)
        self.lineEdit_7.setGeometry(QtCore.QRect(240, 150, 51, 23))
        self.lineEdit_7.setObjectName(_fromUtf8("lineEdit_7"))
        self.lineEdit_8 = QtGui.QLineEdit(Form)
        self.lineEdit_8.setGeometry(QtCore.QRect(400, 180, 51, 23))
        self.lineEdit_8.setObjectName(_fromUtf8("lineEdit_8"))
        self.lineEdit_9 = QtGui.QLineEdit(Form)
        self.lineEdit_9.setGeometry(QtCore.QRect(400, 120, 51, 23))
        self.lineEdit_9.setObjectName(_fromUtf8("lineEdit_9"))
        self.lineEdit_10 = QtGui.QLineEdit(Form)
        self.lineEdit_10.setGeometry(QtCore.QRect(400, 150, 51, 23))
        self.lineEdit_10.setObjectName(_fromUtf8("lineEdit_10"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(490, 270, 100, 25))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.clicked.connect(self._applyChanges)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.atomSettings = self.parent.getAtomSettings()
        self._loadSettingsToGUI()

    def color_picker(self):
        ind = QtGui.QColorDialog.getColor().name()
        self.colorRGB = QtGui.QColorDialog.customColor(ind)
        print self.colorRGB

    def _loadSettingsToGUI(self):
        print self.atomSettings['CSize']
        self.slider0.setValue(self.atomSettings['CSize'] / 0.01)
        self.slider1.setValue(self.atomSettings['HSize'] / 0.01)
        self.slider2.setValue(self.atomSettings['OSize'] / 0.01)

        self.lineEdit_4.setText(str(self.atomSettings['OColor'][0] * 255.0))
        self.lineEdit_2.setText(str(self.atomSettings['OColor'][1] * 255.0))
        self.lineEdit_3.setText(str(self.atomSettings['OColor'][2] * 255.0))
        self.lineEdit_6.setText(str(self.atomSettings['HColor'][0] * 255.0))
        self.lineEdit_7.setText(str(self.atomSettings['HColor'][1] * 255.0))
        self.lineEdit_5.setText(str(self.atomSettings['HColor'][2] * 255.0))
        self.lineEdit_9.setText(str(self.atomSettings['CColor'][0] * 255.0))
        self.lineEdit_10.setText(str(self.atomSettings['CColor'][1] * 255.0))
        self.lineEdit_8.setText(str(self.atomSettings['CColor'][2] * 255.0))

        if self.atomSettings['Viz']=='lines':
             self.radioButton.setChecked(True)
        elif self.atomSettings['Viz']=='points':
             self.radioButton_2.setChecked(True)
        elif self.atomSettings['Viz']=='triangles':
             self.radioButton_3.setChecked(True)

    def _applyChanges(self):
        self.parent.setAtomSettings(self.getSettingsFromGUI())

    def closeEvent(self, event):
        self.parent.setEnabled(True)

    def getSettingsFromGUI(self):
        self.atomSettings['CSize'] = self.slider0.value() * 0.01
        self.atomSettings['HSize'] = self.slider1.value() * 0.01
        self.atomSettings['OSize'] = self.slider2.value() * 0.01

        self.atomSettings['OColor'] = (float(self.lineEdit_4.text())/255.0, float(self.lineEdit_2.text())/255.0, float(self.lineEdit_3.text())/255.0)
        self.atomSettings['HColor'] = (float(self.lineEdit_6.text())/255.0, float(self.lineEdit_7.text())/255.0, float(self.lineEdit_5.text())/255.0)
        self.atomSettings['CColor'] = (float(self.lineEdit_9.text())/255.0, float(self.lineEdit_10.text())/255.0, float(self.lineEdit_8.text())/255.0)

        if self.radioButton.isChecked():
            self.atomSettings['Viz'] = 'lines'
        elif self.radioButton_2.isChecked():
            self.atomSettings['Viz'] = 'points'
        elif self.radioButton_3.isChecked():
            self.atomSettings['Viz'] = 'triangles'
        return self.atomSettings

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label.setText(_translate("Form", "Größe", None))
        self.label_9.setText(_translate("Form", "Sauerstoff", None))
        self.label_6.setText(_translate("Form", "Kohlenstoff", None))
        self.label_8.setText(_translate("Form", "Wasserstoff", None))
        self.radioButton.setText(_translate("Form", "Linien", None))
        self.radioButton_2.setText(_translate("Form", "Punkte", None))
        self.radioButton_3.setText(_translate("Form", "Solide", None))
        self.label_2.setText(_translate("Form", "Farbe", None))
        self.pushButton.setText(_translate("Form", "Übernehmen", None))

class Ui_BondOptions(QtGui.QMainWindow, object):
    def __init__(self, parent):
        super(self.__class__, self).__init__()
        self.parent = parent

    def setupUi(self, Bindungsoptionen):
        Bindungsoptionen.setObjectName(_fromUtf8("Bindungsoptionen"))
        Bindungsoptionen.resize(400, 277)

        self.slider0 = QtGui.QSlider(QtCore.Qt.Horizontal, Bindungsoptionen)
        self.slider0.setFocusPolicy(QtCore.Qt.NoFocus)
        self.slider0.setGeometry(160, 20, 111, 31)

        self.label_2 = QtGui.QLabel(Bindungsoptionen)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 91, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_9 = QtGui.QLabel(Bindungsoptionen)
        self.label_9.setGeometry(QtCore.QRect(20, 90, 111, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.radioButton_2 = QtGui.QRadioButton(Bindungsoptionen)
        self.radioButton_2.setGeometry(QtCore.QRect(30, 170, 121, 20))
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        self.radioButton_3 = QtGui.QRadioButton(Bindungsoptionen)
        self.radioButton_3.setGeometry(QtCore.QRect(30, 200, 121, 20))
        self.radioButton_3.setObjectName(_fromUtf8("radioButton_3"))
        self.radioButton = QtGui.QRadioButton(Bindungsoptionen)
        self.radioButton.setGeometry(QtCore.QRect(30, 230, 121, 20))
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.pushButton = QtGui.QPushButton(Bindungsoptionen)
        self.pushButton.setGeometry(QtCore.QRect(290, 230, 100, 25))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.clicked.connect(self._applyChanges)

        self.lineEdit_4 = QtGui.QLineEdit(Bindungsoptionen)
        self.lineEdit_4.setGeometry(QtCore.QRect(160, 90, 51, 20))
        self.lineEdit_4.setText(_fromUtf8(""))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.lineEdit_5 = QtGui.QLineEdit(Bindungsoptionen)
        self.lineEdit_5.setGeometry(QtCore.QRect(300, 90, 51, 20))
        self.lineEdit_5.setText(_fromUtf8(""))
        self.lineEdit_5.setObjectName(_fromUtf8("lineEdit_5"))
        self.lineEdit_6 = QtGui.QLineEdit(Bindungsoptionen)
        self.lineEdit_6.setGeometry(QtCore.QRect(230, 90, 51, 20))
        self.lineEdit_6.setText(_fromUtf8(""))
        self.lineEdit_6.setObjectName(_fromUtf8("lineEdit_6"))

        self.label = QtGui.QLabel(Bindungsoptionen)
        self.label.setGeometry(QtCore.QRect(160, 70, 46, 13))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_3 = QtGui.QLabel(Bindungsoptionen)
        self.label_3.setGeometry(QtCore.QRect(230, 70, 46, 13))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(Bindungsoptionen)
        self.label_4.setGeometry(QtCore.QRect(300, 70, 46, 13))
        self.label_4.setObjectName(_fromUtf8("label_4"))

        self.retranslateUi(Bindungsoptionen)
        QtCore.QMetaObject.connectSlotsByName(Bindungsoptionen)
        self.bondSettings = self.parent.getBondSettings()
        self._loadSettingsToGUI()

    def _loadSettingsToGUI(self):
        self.slider0.setValue(self.bondSettings['Size'] / 0.01)
        self.lineEdit_4.setText(str(self.bondSettings['Color'][0] * 255.0))
        self.lineEdit_5.setText(str(self.bondSettings['Color'][1] * 255.0))
        self.lineEdit_6.setText(str(self.bondSettings['Color'][2] * 255.0))
        if self.bondSettings['Viz']=='lines':
             self.radioButton.setChecked(True)
        elif self.bondSettings['Viz']=='points':
             self.radioButton_2.setChecked(True)
        elif self.bondSettings['Viz']=='triangles':
             self.radioButton_3.setChecked(True)

    def _applyChanges(self):
        self.parent.setBondSettings(self.getSettingsFromGUI())

    def closeEvent(self, event):
        self.parent.setEnabled(True)

    def getSettingsFromGUI(self):
        self.bondSettings['Size'] = self.slider0.value() * 0.01 #geht leider nicht anders
        self.bondSettings['Color'] = (float(self.lineEdit_4.text())/255.0, float(self.lineEdit_5.text())/255.0, float(self.lineEdit_6.text())/255.0)
        if self.radioButton.isChecked():
            self.bondSettings['Viz'] = 'lines'
        elif self.radioButton_2.isChecked():
            self.bondSettings['Viz'] = 'points'
        elif self.radioButton_3.isChecked():
            self.bondSettings['Viz'] = 'triangles'
        return self.bondSettings

    def retranslateUi(self, Bindungsoptionen):
        Bindungsoptionen.setWindowTitle(_translate("Bindungsoptionen", "Bindungsvisualisierung", None))
        self.label_2.setText(_translate("Bindungsoptionen", "Größe", None))
        self.label_9.setText(_translate("Bindungsoptionen", "Farbe", None))
        self.radioButton_2.setText(_translate("Bindungsoptionen", "Punkte", None))
        self.radioButton_3.setText(_translate("Bindungsoptionen", "Solide", None))
        self.radioButton.setText(_translate("Bindungsoptionen", "Linien", None))
        self.pushButton.setText(_translate("Bindungsoptionen", "Übernehmen", None))
        self.label.setText(_translate("Bindungsoptionen", "Red", None))
        self.label_3.setText(_translate("Bindungsoptionen", "Green", None))
        self.label_4.setText(_translate("Bindungsoptionen", "Blue", None))


from PyQt4 import phonon
