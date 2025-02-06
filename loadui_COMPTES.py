from _ident_et_base import *
from _comptes import*
from _gestion_budget import *

from sys import argv
from pyside2_loadui import loadUi
from PySide2 import QtWidgets
from PySide2.QtWidgets import QDialog, QApplication, QWidget, QLineEdit
from PySide2 import QtCore

class COMPTES(QDialog):
    def __init__(self,ope_stock,BUD_stock):
        import random
        super(COMPTES,self).__init__()
        loadUi(chemin("GEST_COMPTES.ui"),self)
        self.initUi(ope_stock,BUD_stock)

    def initUi(self,ope_stock,BUD_stock):
        self.ope_stock,self.BUD_stock=ope_stock,BUD_stock
        self.comboBox_comptes.addItems(list(self.ope_stock.keys()))
        self.comboBox_comptes.currentIndexChanged.connect(self.changer_compte)

        if self.comboBox_comptes.count()>0:
            self.compte=self.comboBox_comptes.currentText()
            self.i=len(self.ope_stock[self.compte])-1
            self.ir=1
            self.solde=solde(self.compte,self.ope_stock)
            self.label_solde.setText("Solde du compte : "+str(self.solde)+"€")
            if len(self.ope_stock[self.compte]) >= 1:
                self.nombre_page.setText('1/'+str(((len(self.ope_stock[self.compte])-1)//10)+1))
            else:
                self.nombre_page.setText('1/1')
        else:
            self.i=-1
            self.pushButton_precedent.setEnabled(False)
            self.pushButton_suivant.setEnabled(False)
            self.pushButton_ajout_ope.setEnabled(False)
            self.pushButton_ajout_vir.setEnabled(False)
            self.label_solde.setText("Solde du compte : Pas de compte,  veuillez en créer un.")
            self.nombre_page.setText('1/1')

        self.numero_page=1
        self.pushButton_precedent.clicked.connect(self.bouton_prec)
        self.pushButton_suivant.clicked.connect(self.bouton_suiv)
        
        self.load_ope()
        
    def vider_ope(self)->None:
        '''
        Vide entièrement le tableau des opérations.
        '''
        for i in range(1,self.gridLayout.rowCount()):#Lignes
            for j in range(self.gridLayout.columnCount()):#Colonnes
                item = self.gridLayout.itemAtPosition(i, j)
                widget = item.widget()
                widget.setText("")

    def refresh_nombre_page(self):
        '''
        Dans le tableau des opérations d'un compte d'un utilisateur,
        cette methode permet d'afficher le numero de page actuel et
        Le nombre total de pages.
        '''
        if len(self.ope_stock[self.compte]) >= 1:
            self.nombre_page.setText(str(self.numero_page)+'/'+str(((len(self.ope_stock[self.compte])-1)//10)+1))
        else:
            self.nombre_page.setText(str(self.numero_page)+'/1')

    def changer_compte(self)->None:
        '''
        Actualise les informations 
        '''
        self.vider_ope()
        self.compte=self.comboBox_comptes.currentText()

        #Actualisation du numéro de la page
        self.numero_page=1
        self.refresh_nombre_page()

        self.i=len(self.ope_stock[self.compte])-1
        self.ir=1
        self.solde=solde(self.compte,self.ope_stock)
        self.label_solde.setText("Solde du compte : "+str(self.solde)+"€")
        self.load_ope()
    
    
    def bouton_prec(self):
        '''
        Affiche la page d'opération précédente.
        '''
        i=self.i+10+self.ir-1
        if i<len(self.ope_stock[self.compte]):

            #Actualisation du numéro de la page
            self.numero_page -= 1
            self.refresh_nombre_page()

            self.ir=1
            self.i=i
            self.load_ope()

    def bouton_suiv(self):
        '''
        Affiche la page d'opération suivante.
        '''
        if self.i> -1:

            #Actualisation du numéro de la page
            self.numero_page += 1
            self.refresh_nombre_page()

            self.vider_ope()
            self.ir=1
            self.load_ope()

    def load_ope(self):
        '''
        Rafraîchit le tableau des opérations selon l'action souhaitée.
        '''
        irow,icol=self.gridLayout.rowCount(),self.gridLayout.columnCount()
        ic=0
        j=0
        while self.i> -1 and self.ir<irow and ic<icol :
            t=self.ope_stock[self.compte][self.i][1:3]+self.ope_stock[self.compte][self.i][4:]
            while j<6:
                item = self.gridLayout.itemAtPosition(self.ir,j)
                widget=item.widget()
                widget.setText(t[j])
                j+=1
            j,self.i,self.ir=0,self.i-1,self.ir+1
        

if __name__=='__main__':
    app=QApplication(argv)
    comptes=COMPTES(operations_stock('38654157',21)[0],operations_stock('38654157',21)[1],)
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(comptes)
    widget.setFixedHeight(850)
    widget.setFixedWidth(1100)
    widget.show()
    app.exec_()