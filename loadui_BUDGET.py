from _ident_et_base import *
from _comptes import*
from _gestion_budget import *

from sys import argv
from pyside2_loadui import loadUi
from PySide2 import QtWidgets
from PySide2.QtWidgets import QDialog, QApplication, QWidget, QLineEdit
from PySide2 import QtCore
from RoundProgressBar import roundProgressBar

class BUDGET(QDialog):
    def __init__(self,ope_stock,BUD_stock):
        import random
        super(BUDGET,self).__init__()
        loadUi(chemin("GEST_BUDGET.ui"),self)
        self.initUi(ope_stock,BUD_stock)

    def initUi(self,ope_stock,BUD_stock):
        self.ope_stock,self.BUD_stock = ope_stock,BUD_stock
        self.comboBox_compte.addItems(list(self.BUD_stock.keys()))

        self.compte = self.comboBox_compte.currentText()
        self.mois = self.comboBox_mois.currentText()
        self.annee = self.comboBox_annee.currentText()

        self.comboBox_budget.addItems(liste_BUD(self.BUD_stock,self.compte))
        self.budget = self.comboBox_budget.currentText()

        #GRIDCONT ~ Contenu de la grille/tableau.
        self.GRIDCONT=operations_budget(self.BUD_stock,self.compte,self.budget,self.mois,self.annee)
        self.i = len(self.GRIDCONT)-1
        self.ir = 1
        self.numero_page = 1
        
        self.solde=solde(self.compte,self.ope_stock)
        self.budget_fixe=soldeBUD(self.BUD_stock,self.compte,self.budget)
        self.restant=difference(self.BUD_stock,self.compte,self.budget,self.mois,self.annee)
        self.depenses=depenses(self.BUD_stock,self.compte,self.budget,self.mois,self.annee)

        
        if self.comboBox_compte.count()>0:
            if self.comboBox_compte.count()>0 and self.comboBox_budget.count()>0:
                self.refresh_diagramme()
            self.afficher_texte()
            if len(self.GRIDCONT)>=1:
                self.nombre_page.setText('1/'+str(((len(self.GRIDCONT)-1)//8)+1))
            else:
                self.nombre_page.setText('1/1')
        else:
            self.pushButton_ajouter.setEnabled(False)
            self.arriere_plan_diag.setVisible(False)
            self.vider_texte()
            self.nombre_page.setText('1/1')
        
        if self.comboBox_budget.count()>0:
            self.refresh_diagramme()
            self.afficher_texte()
        else:
            self.label_aucun_compte.setText('Aucun budget')
            self.arriere_plan_diag.setVisible(False)
            self.vider_texte_no_budget()

        self.comboBox_compte.currentIndexChanged.connect(self.changer_compte)
        self.comboBox_mois.currentIndexChanged.connect(self.changer_tableau)
        self.comboBox_annee.currentIndexChanged.connect(self.changer_tableau)
        self.comboBox_budget.currentIndexChanged.connect(self.changer_tableau)
        self.pushButton_precedent.clicked.connect(self.bouton_prec)
        self.pushButton_suivant.clicked.connect(self.bouton_suiv)
        
        self.load_ope()
        
    def refresh_diagramme(self):
        '''
        Affiche un diagramme correspondant qux paramètres selectionnés.
        '''
        self.arriere_plan_diag.setVisible(True)
        while self.gridLayout_progress.count() > 0:
            item = self.gridLayout_progress.takeAt(self.gridLayout_progress.count() - 1)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.label_aucun_compte.setVisible(False)
        self.progress_bar = roundProgressBar()
        self.progress_bar.rpb_setBarStyle('Line')
        self.progress_bar.rpb_setLineColor((255, 255, 255))
        self.progress_bar.rpb_setTextColor((255,255,255))
        self.progress_bar.rpb_setLineWidth(20)
        self.progress_bar.rpb_setLineCap('RoundCap')
        self.progress_bar.rpb_setRange(self.budget_fixe, 0.00001)
        self.progress_bar.rpb_setValue(-self.depenses)
        self.gridLayout_progress.addWidget(self.progress_bar)

    def cacher_diagramme(self):
        '''
        Rend le diagramme invisible.
        '''
        self.label_aucun_compte.setText('Aucun budget')
        self.label_aucun_compte.setVisible(True)
        try:
            self.arriere_plan_diag.setVisible(False)
            self.progress_bar.setVisible(False)
        except:
            None

    def afficher_texte(self):
        '''
        Actualise l'affichage des informations du compte sur la page.
        '''
        self.comboBox_mois.setEnabled(True)
        self.comboBox_annee.setEnabled(True)
        self.label_solde.setText("Solde du compte : "+str(self.solde)+" €")
        self.label_budget.setText("Budget fixé : "+str(self.budget_fixe)+" €")
        self.label_restant.setText("Budget restant: "+str(self.restant)+" €")
        self.label_depenses.setText("Dépenses : "+str(self.depenses)+" €")
    
    def vider_texte(self):
        '''
        Toutes les valeurs sont en "non calculable" si un utilisateur ne possède pas de comptes.
        '''
        self.comboBox_compte.clear()
        self.comboBox_mois.setEnabled(False)
        self.comboBox_annee.setEnabled(False)
        self.comboBox_budget.clear()
        self.label_solde.setText("Solde du compte : Non calculable") 
        self.label_budget.setText("Budget fixé : Non calculable")
        self.label_restant.setText("Budget restant : Non calculable")
        self.label_depenses.setText("Dépenses : Non calculable")

    def vider_texte_no_budget(self):
        '''
        Toutes les valeurs sont en "non calculable" si un compte
        d'utilisateur ne possède pas de budget.
        '''
        self.comboBox_mois.setEnabled(False)
        self.comboBox_annee.setEnabled(False)
        self.label_solde.setText("Solde du compte : Non calculable") 
        self.label_budget.setText("Budget fixé : Non calculable")
        self.label_restant.setText("Budget restant : Non calculable")
        self.label_depenses.setText("Dépenses : Non calculable")

    def changer_compte(self):
        '''
        Actualise les informatuion de la fenêtre selon le compte choisi.
        '''
        self.compte = self.comboBox_compte.currentText()
        self.mois = self.comboBox_mois.currentText()
        self.annee = self.comboBox_annee.currentText()
        self.budget = self.comboBox_budget.currentText()

        self.comboBox_budget.clear()
        self.vider_ope()

        self.GRIDCONT=operations_budget(self.BUD_stock,self.compte,self.budget,self.mois,self.annee)
        self.comboBox_budget.addItems([i for i in self.BUD_stock[self.compte]['budgets']])
        self.i = len(self.GRIDCONT)-1
        self.ir = 1
        
        self.solde=solde(self.compte,self.ope_stock)
        self.budget_fixe=soldeBUD(self.BUD_stock,self.compte,self.budget)
        self.restant=difference(self.BUD_stock,self.compte,self.budget,self.mois,self.annee)
        self.depenses=depenses(self.BUD_stock,self.compte,self.budget,self.mois,self.annee)

        if self.comboBox_budget.count()>0:
            self.afficher_texte()
            self.refresh_diagramme()
        else:
            self.vider_texte_no_budget()
            self.cacher_diagramme()

        #Actualisation du numéro de la page
        self.numero_page = 1
        self.refresh_nombre_page()

        self.load_ope()
        
    
    def changer_tableau(self):
        '''
        Change le contenu du tableau selon les paramètres choisis.
        '''
        self.vider_ope()
        #self.compte = self.comboBox_compte.currentText()
        self.budget = self.comboBox_budget.currentText()
        self.mois = self.comboBox_mois.currentText()
        self.annee = self.comboBox_annee.currentText()

        self.solde=solde(self.compte,self.ope_stock)
        self.budget_fixe=soldeBUD(self.BUD_stock,self.compte,self.budget)
        self.restant=difference(self.BUD_stock,self.compte,self.budget,self.mois,self.annee)
        self.depenses=depenses(self.BUD_stock,self.compte,self.budget,self.mois,self.annee)

        self.GRIDCONT = operations_budget(self.BUD_stock,self.compte,self.budget,self.mois,self.annee)
        self.i = len(self.GRIDCONT)-1
        self.ir = 1

        #Actualisation du numéro de la page
        self.numero_page = 1
        self.refresh_nombre_page()

        self.refresh_diagramme()
        self.afficher_texte()
        self.load_ope()
        
    def vider_ope(self):
        '''
        Vide le tableau des opérations.
        '''
        for i in range(1,self.gridLayout.rowCount()):
            for j in range(self.gridLayout.columnCount()):
                item = self.gridLayout.itemAtPosition(i, j)
                widget = item.widget()
                widget.setText("")

    def refresh_nombre_page(self):
        '''
        Dans le tableau des opérations d'un compte d'un utilisateur,
        cette methode permet d'afficher le numero de page actuel et
        Le nombre total de pages.
        '''
        if len(self.GRIDCONT)>=1:
            self.nombre_page.setText(str(self.numero_page)+'/'+str(((len(self.GRIDCONT)-1)//8)+1))
        else:
            self.nombre_page.setText(str(self.numero_page)+'/1')

    def bouton_prec(self):
        '''
        Passage à la page d'opération précédente.
        '''
        i=self.i+8+self.ir-1
        if i<len(self.GRIDCONT):

            #Actualisation du numéro de la page
            self.numero_page -= 1
            self.refresh_nombre_page()

            self.ir=1
            self.i=i
            self.load_ope()

    def bouton_suiv(self):
        '''
        Passage à la page d'opération suivante.
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
        Actualise le tableau des opérations.
        '''
        irow,icol=self.gridLayout.rowCount(),self.gridLayout.columnCount()
        ic=0
        j=0
        while self.i> -1 and self.ir<irow and ic<icol :
            t=self.GRIDCONT[self.i][1:3]+self.GRIDCONT[self.i][4:6]
            while j<4:
                item = self.gridLayout.itemAtPosition(self.ir,j)
                widget=item.widget()
                widget.setText(t[j])
                j+=1
            j,self.i,self.ir=0,self.i-1,self.ir+1
        

if __name__=='__main__':
    app=QApplication(argv)
    widget=QtWidgets.QStackedWidget()
    #comptes=BUDGET(operations_stock('38654157',21)[0],operations_stock('38654157',21)[1])
    comptes=BUDGET(operations_stock('59455164',14)[0],operations_stock('59455164',14)[1])
    widget.addWidget(comptes)
    widget.setFixedHeight(850)
    widget.setFixedWidth(1100)
    widget.show()
    app.exec_()