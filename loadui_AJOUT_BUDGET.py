from _ident_et_base import *
from _comptes import*
from _gestion_budget import *

from sys import argv
from pyside2_loadui import loadUi
from PySide2 import QtWidgets
from PySide2.QtWidgets import QDialog, QApplication, QWidget, QLineEdit
from PySide2 import QtCore
from PySide2.QtGui import QRegularExpressionValidator

class AJOUT_BUDGET(QDialog):
    def __init__(self,BUD_stock):
        import random
        super(AJOUT_BUDGET,self).__init__()
        loadUi(chemin("AJOUT_BUDGET.ui"),self)
        self.initUi(BUD_stock)
    
    def initUi(self,BUD_stock):
        self.BUD_stock = BUD_stock
        self.pushButton_1.clicked.connect(self.zonemontant)
        self.pushButton_2.clicked.connect(self.zonemontant)
        self.pushButton_3.clicked.connect(self.zonemontant)
        self.pushButton_4.clicked.connect(self.zonemontant)
        self.pushButton_5.clicked.connect(self.zonemontant)
        self.pushButton_6.clicked.connect(self.zonemontant)
        self.pushButton_7.clicked.connect(self.zonemontant)
        self.pushButton_8.clicked.connect(self.zonemontant)
        self.pushButton_9.clicked.connect(self.zonemontant)
        self.pushButton_10.clicked.connect(self.zonemontant)
        self.pushButton_11.clicked.connect(self.zonemontant)
        self.pushButton_suppr.clicked.connect(self.supprmontant)
        self.pushButton_creer.clicked.connect(self.valider)

        self.zone_montant.setReadOnly(True)

        self.comboBox_compte.addItems(list(self.BUD_stock.keys()))

        self.label_erreur.setVisible(False)
        self.label_confirmation.setVisible(False)
        
    def valider(self):
        '''
        Ajout du nouveau budget lorsque le bouton valider est cliqué.
        '''
        try:
            if self.zone_budget.text() in self.BUD_stock[self.comboBox_compte.currentText()]['budgets']:
                self.label_erreur.setVisible(True)
                self.label_confirmation.setVisible(False)
            else:
                self.BUD_stock = ajouter_BUD(self.comboBox_compte.currentText(),self.zone_budget.text(),self.zone_montant.text(),self.BUD_stock)
                self.label_erreur.setVisible(False)
                self.label_confirmation.setVisible(True)
        except:
            self.label_erreur.setVisible(True)
            self.label_confirmation.setVisible(False)
    
    def supprmontant(self):
        '''
        Supprime le dernier caractère de la zone de texte du montant
        lorsque le bouton suppr est cliqué.
        '''
        self.zone_montant.backspace()

    def zonemontant(self):
        '''
        Ajoute le caractère cliqué dans la zone de texte du montant.
        '''
        button = self.sender()
        self.zone_montant.insert(button.text())

    
        

if __name__=='__main__':
    app=QApplication(argv)
    AJOUT_BUDGET=AJOUT_BUDGET(operations_stock('38654157',21)[1])
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(AJOUT_BUDGET)
    widget.setFixedHeight(850)
    widget.setFixedWidth(1100)
    widget.show()
    app.exec_()