from _ident_et_base import *
from _comptes import*
from _gestion_budget import *

from sys import argv
from pyside2_loadui import loadUi
from PySide2 import QtWidgets
from PySide2.QtWidgets import QDialog, QApplication, QWidget, QLineEdit
from PySide2 import QtCore
from PySide2.QtGui import QRegularExpressionValidator

class AJOUT_COMPTE(QDialog):
    def __init__(self,ope_stock,BUD_stock):
        import random
        super(AJOUT_COMPTE,self).__init__()
        loadUi(chemin("AJOUT_COMPTE.ui"),self)
        self.initUi(ope_stock,BUD_stock)
    
    def initUi(self,ope_stock,BUD_stock):
        self.ope_stock, self.BUD_stock = ope_stock,BUD_stock
        self.pushButton_creer.clicked.connect(self.valider)
        self.label_erreur.setVisible(False)
        self.label_confirmation.setVisible(False)
        
    def valider(self):
        #Ajout du nouveau compte lorsque le bouton valider est cliqué.
        try:
            if (self.zone_compte.text() not in self.ope_stock) and self.zone_compte.text()!='budgets':
                self.ope_stock,self.BUD_stock=ajouter_compte(self.ope_stock,self.BUD_stock,self.zone_compte.text())
                self.label_erreur.setVisible(False)
                self.label_confirmation.setVisible(True)
            else:
                self.label_erreur.setVisible(True)
                self.label_confirmation.setVisible(False)
        except:
            self.label_erreur.setVisible(True)
            self.label_confirmation.setVisible(False)

    
        

if __name__=='__main__':
    app=QApplication(argv)
    ajout_compte=AJOUT_COMPTE(operations_stock('38654157',21)[0],operations_stock('38654157',21)[1])
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(ajout_compte)
    widget.setFixedHeight(850)
    widget.setFixedWidth(1100)
    widget.show()
    app.exec_()