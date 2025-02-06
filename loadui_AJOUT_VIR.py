from _ident_et_base import *
from _comptes import*
from _gestion_budget import *

from sys import argv
from pyside2_loadui import loadUi
from PySide2 import QtWidgets
from PySide2.QtWidgets import QDialog, QApplication, QWidget, QLineEdit
from PySide2 import QtCore
from PySide2.QtGui import QRegularExpressionValidator

class AJOUT_VIR(QDialog):
    def __init__(self,ope_stock,BUD_stock):
        import random
        super(AJOUT_VIR,self).__init__()
        loadUi(chemin("AJOUT_VIR.ui"),self)
        self.initUi(ope_stock,BUD_stock)
    
    def initUi(self,ope_stock,BUD_stock):
        self.ope_stock,self.BUD_stock = ope_stock, BUD_stock
        self.pushButton_1.clicked.connect(self.ecrire_montant)
        self.pushButton_2.clicked.connect(self.ecrire_montant)
        self.pushButton_3.clicked.connect(self.ecrire_montant)
        self.pushButton_4.clicked.connect(self.ecrire_montant)
        self.pushButton_5.clicked.connect(self.ecrire_montant)
        self.pushButton_6.clicked.connect(self.ecrire_montant)
        self.pushButton_7.clicked.connect(self.ecrire_montant)
        self.pushButton_8.clicked.connect(self.ecrire_montant)
        self.pushButton_9.clicked.connect(self.ecrire_montant)
        self.pushButton_10.clicked.connect(self.ecrire_montant)
        self.pushButton_11.clicked.connect(self.ecrire_montant)
        self.pushButton_suppr.clicked.connect(self.supprmontant)
        self.pushButton_valider.clicked.connect(self.valider)
        

        self.zone_montant.setReadOnly(True)

        self.comboBox_compte1.addItems(list(self.ope_stock.keys()))
        self.comboBox_compte2.addItems(list(self.ope_stock.keys()))
        self.comboBox_compte2.currentIndexChanged.connect(self.changer_compte)
        self.comboBox_budget.addItems(['']+list(self.BUD_stock[self.comboBox_compte2.currentText()]['budgets'].keys()))

        self.label_erreur.setVisible(False)
        self.label_confirmation.setVisible(False)
    
    def changer_compte(self):
        '''
        Actualise les budgets selon le compte sélectionné.
        '''
        self.comboBox_budget.clear()
        self.comboBox_budget.addItems(['']+list(self.BUD_stock[self.comboBox_compte2.currentText()]['budgets'].keys()))

    def valider(self):
        '''
        Ajoute le virement au dictionnaire d'opes lorsque le bouton valider est cliqué.
        '''
        listemois = {'Janvier':'01','Février':'02','Mars':'03','Avril':'04','Mai':'05','Juin':'06','Juillet':'07',\
        'Août':'08','Septembre':'09','Octobre':'10','Novembre':'11','Décembre':'12'}
        date=self.comboBox_jour.currentText()+"/"+listemois[self.comboBox_mois.currentText()]+"/"+self.comboBox_annee.currentText()
        try:
            if self.comboBox_compte1.currentText()!=self.comboBox_compte2.currentText():
                self.ope_stock,self.BUD_stock=ajouter_virement(self.ope_stock,self.BUD_stock,self.comboBox_compte1.currentText(),self.comboBox_compte2.currentText(),date,float(self.zone_montant.text()),self.comboBox_statut.currentText(),self.comboBox_budget.currentText())
                self.label_erreur.setVisible(False)
                self.label_confirmation.setVisible(True)
            else:
                self.label_erreur.setVisible(True)
                self.label_confirmation.setVisible(False)
        except:
            self.label_erreur.setVisible(True)
            self.label_confirmation.setVisible(False)
    
    def supprmontant(self):
        '''
        Supprime le dernier caractère de la zone de texte du montant
        lorsque le bouton suppr est cliqué.
        '''
        self.zone_montant.backspace()

    def ecrire_montant(self):
        '''
        Ajoute le caractère cliqué dans la zone de texte du montant.
        '''
        button = self.sender()
        self.zone_montant.insert(button.text())

    
        

if __name__=='__main__':
    app=QApplication(argv)
    AJOUT_BUDGET=AJOUT_VIR(operations_stock('38654157',21)[0],operations_stock('38654157',21)[1])
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(AJOUT_BUDGET)
    widget.setFixedHeight(850)
    widget.setFixedWidth(1100)
    widget.show()
    app.exec_()