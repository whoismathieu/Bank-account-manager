from _ident_et_base import *
import _comptes
from _gestion_budget import *

import sys
from pyside2_loadui import loadUi
from PySide2 import QtWidgets
from PySide2.QtWidgets import QDialog, QApplication, QWidget, QLineEdit, QMainWindow
from PySide2 import QtCore

from loadui_ACCUEIL import ACCUEIL
from loadui_CHOIX import CHOIX
from loadui_COMPTES import COMPTES
from loadui_AJOUT_COMPTE import AJOUT_COMPTE
from loadui_AJOUT_OPE import AJOUT_OPE
from loadui_AJOUT_VIR import AJOUT_VIR
from loadui_BUDGET import BUDGET
from loadui_AJOUT_BUDGET import AJOUT_BUDGET

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.essais=2

        self.stackedWidget = QtWidgets.QStackedWidget()
        # Set the central widget of the main window
        self.setCentralWidget(self.stackedWidget)
        self.setFixedSize(1100,850)

        self.show_accueil()

    def show_accueil(self):
        try :
            del self.name,self.user,self.cipher,self.ope_stock,self.BUD_stock
        except:
            None
        def connexion(self,widget,user,mot_de_passe):
            if not check_user(user,mot_de_passe)[0] and self.essais>0:
                self.essais-=1 
                widget.label_erreur.setText('ⓘ Identifiant ou mot de passe incorrect,  '+str(self.essais+1)+' essais restants')
                widget.label_erreur.setVisible(True)

            elif self.essais == 0 and not check_user(user,mot_de_passe)[0]:
                self.close()

            else:
                condition , line, cipher = check_user(user,mot_de_passe)
                self.name=dechif_cesar(line.split('*')[2],int(cipher))
                self.user=dechif_cesar(line.split('*')[0],int(cipher))
                self.cipher=cipher
                self.ope_stock,self.BUD_stock = operations_stock(user,cipher)
                del condition , line, cipher,widget,user,mot_de_passe
                self.show_choix()

        self.stackedWidget.removeWidget(self.stackedWidget.currentWidget())

        _accueil = ACCUEIL()
        _accueil.label_erreur.setVisible(False)
        self.stackedWidget.addWidget(_accueil )
        

        _accueil.pushButton_valider.clicked.connect(lambda : connexion(self,_accueil,_accueil.zoneID.text(),_accueil.zoneMDP.text()))
        self.stackedWidget.setCurrentWidget(_accueil)
        
    def ecrire_fichier(self):
        reorganiser(self.user,self.cipher,self.ope_stock,self.BUD_stock)

    def show_choix(self,ope=None,BUD=None):
        self.ope_stock = ope or self.ope_stock
        self.BUD_stock = BUD or self.BUD_stock

        self.stackedWidget.removeWidget(self.stackedWidget.currentWidget())

        _choix = CHOIX(self.ope_stock,self.BUD_stock,self.name)
        _choix.pushButton_deco.clicked.connect(lambda : self.show_accueil())
        _choix.pushButton_comptes.clicked.connect(lambda : self.show_gest_comptes())
        _choix.pushButton_budget.clicked.connect(lambda : self.show_gest_budget())
            
        self.stackedWidget.addWidget(_choix)
        self.stackedWidget.setCurrentWidget(_choix)
    
    def show_gest_comptes(self, ope=None, BUD=None):
        self.ope_stock = ope or self.ope_stock
        self.BUD_stock = BUD or self.BUD_stock

        self.stackedWidget.removeWidget(self.stackedWidget.currentWidget())

        _gest_comptes = COMPTES(self.ope_stock,self.BUD_stock)
        _gest_comptes.pushButton_retour.clicked.connect(lambda : self.show_choix(ope=_gest_comptes.ope_stock))
        _gest_comptes.pushButton_retour.clicked.connect(lambda : self.ecrire_fichier())
        _gest_comptes.pushButton_ajout_compte.clicked.connect(lambda : self.show_ajout_compte())
        _gest_comptes.pushButton_ajout_ope.clicked.connect(lambda : self.show_ajout_ope())
        _gest_comptes.pushButton_ajout_vir.clicked.connect(lambda : self.show_ajout_vir())
        self.stackedWidget.addWidget(_gest_comptes)
        self.stackedWidget.setCurrentWidget(_gest_comptes)
    
    def show_ajout_compte(self):
        # Supprime le widget (fenêtre) actuel.
        self.stackedWidget.removeWidget(self.stackedWidget.currentWidget())

        _ajout_compte = AJOUT_COMPTE(self.ope_stock,self.BUD_stock)
        _ajout_compte.pushButton_retour.clicked.connect(lambda : self.show_gest_comptes())
        _ajout_compte.pushButton_retour.clicked.connect(lambda : self.show_gest_comptes(_ajout_compte.ope_stock,_ajout_compte.BUD_stock))
        self.stackedWidget.addWidget(_ajout_compte)
        self.stackedWidget.setCurrentWidget(_ajout_compte)
    
    def show_ajout_ope(self):
        self.stackedWidget.removeWidget(self.stackedWidget.currentWidget())

        _ajout_ope = AJOUT_OPE(self.ope_stock,self.BUD_stock)
        _ajout_ope.pushButton_retour.clicked.connect(lambda : self.show_gest_comptes())
        _ajout_ope.pushButton_retour.clicked.connect(lambda : self.show_gest_comptes(_ajout_ope.ope_stock,_ajout_ope.BUD_stock))
        self.stackedWidget.addWidget(_ajout_ope)
        self.stackedWidget.setCurrentWidget(_ajout_ope)
    
    def show_ajout_vir(self):
        self.stackedWidget.removeWidget(self.stackedWidget.currentWidget())

        _ajout_vir = AJOUT_VIR(self.ope_stock,self.BUD_stock)
        _ajout_vir.pushButton_retour.clicked.connect(lambda : self.show_gest_comptes())
        _ajout_vir.pushButton_retour.clicked.connect(lambda : self.show_gest_comptes(_ajout_vir.ope_stock,_ajout_vir.BUD_stock))
        self.stackedWidget.addWidget(_ajout_vir)
        self.stackedWidget.setCurrentWidget(_ajout_vir)
    
    def show_gest_budget(self, ope=None, BUD=None):
        self.ope_stock = ope or self.ope_stock
        self.BUD_stock = BUD or self.BUD_stock

        self.stackedWidget.removeWidget(self.stackedWidget.currentWidget())

        _gest_budget = BUDGET(self.ope_stock,self.BUD_stock)
        _gest_budget.pushButton_ajouter.clicked.connect(lambda : self.show_ajout_budget())
        _gest_budget.pushButton_retour.clicked.connect(lambda : self.show_choix(BUD=_gest_budget.BUD_stock))
        _gest_budget.pushButton_retour.clicked.connect(lambda : self.ecrire_fichier())
        self.stackedWidget.addWidget(_gest_budget)
        self.stackedWidget.setCurrentWidget(_gest_budget)

    def show_ajout_budget(self):
        self.stackedWidget.removeWidget(self.stackedWidget.currentWidget())

        _ajout_budget = AJOUT_BUDGET(self.BUD_stock)
        _ajout_budget.pushButton_retour.clicked.connect(lambda : self.show_gest_budget(BUD=_ajout_budget.BUD_stock))
        self.stackedWidget.addWidget(_ajout_budget)
        self.stackedWidget.setCurrentWidget(_ajout_budget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())