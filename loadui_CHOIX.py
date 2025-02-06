from _ident_et_base import *
from _comptes import*
from _gestion_budget import *

from sys import argv
from pyside2_loadui import loadUi
from PySide2 import QtWidgets
from PySide2.QtWidgets import QDialog, QApplication, QWidget, QLineEdit
from PySide2 import QtCore
from PySide2.QtGui import QRegularExpressionValidator

class CHOIX(QDialog):
    def __init__(self,ope_stock,BUD_stock,nom):
        import random
        super(CHOIX,self).__init__()
        loadUi(chemin("CHOIX.ui"),self)
        self.initUi(ope_stock,BUD_stock,nom)
    
    def initUi(self,ope_stock,BUD_stock,nom):
        self.ope_stock,self.BUD_stock = ope_stock,BUD_stock

        # AFFICHER LE NOM
        self.label_titre.setText('Bienvenue '+nom+'.')

        self.comboBox_compte.addItems(list(self.ope_stock.keys()))
        self.compte=self.comboBox_compte.currentText()

        # ASSOCIER COMPTE ET SOLDE
        self.comboBox_compte.currentIndexChanged.connect(self.changer_compte)

        self.affiche_solde()
    
    def changer_compte(self):
        '''
        Permet d'afficher une prévisualisation du solde d'un compte selon le compte sélectionné.
        '''
        self.compte=self.comboBox_compte.currentText()
        self.affiche_solde()

    def affiche_solde(self):
        '''
        Permet d'afficher une prévisualisation du solde d'un compte.
        '''
        if self.comboBox_compte.count()>0:
            self.label_solde.setText('Il vous reste\n'+str(solde(self.compte,self.ope_stock))+' €')


if __name__=='__main__':
    app=QApplication(argv)
    choix=CHOIX(operations_stock('144166',21)[0],operations_stock('144166',21)[1],'Silvain')
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(choix)
    widget.setFixedHeight(850)
    widget.setFixedWidth(1100)
    widget.show()
    app.exec_()