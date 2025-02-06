from _ident_et_base import *
import _comptes
from _gestion_budget import *

import sys
from pyside2_loadui import loadUi
from PySide2 import QtWidgets
from PySide2.QtWidgets import QDialog, QApplication, QWidget, QLineEdit
from PySide2 import QtCore



class ACCUEIL(QDialog):
    def __init__(self):
        import random
        super(ACCUEIL,self).__init__()
        loadUi(chemin("ACCUEIL.ui"),self)

        self.essais=3

        buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        random.shuffle(buttons)
        self.pushButton_1.setText(buttons[0])
        self.pushButton_2.setText(buttons[1])
        self.pushButton_3.setText(buttons[2])
        self.pushButton_4.setText(buttons[3])
        self.pushButton_5.setText(buttons[4])
        self.pushButton_6.setText(buttons[5])
        self.pushButton_7.setText(buttons[6])
        self.pushButton_8.setText(buttons[7])
        self.pushButton_9.setText(buttons[8])
        self.pushButton_10.setText(buttons[9])
        self.pushButton_1.clicked.connect(self.click_chiffre)
        self.pushButton_2.clicked.connect(self.click_chiffre)
        self.pushButton_3.clicked.connect(self.click_chiffre)
        self.pushButton_4.clicked.connect(self.click_chiffre)
        self.pushButton_5.clicked.connect(self.click_chiffre)
        self.pushButton_6.clicked.connect(self.click_chiffre)
        self.pushButton_7.clicked.connect(self.click_chiffre)
        self.pushButton_8.clicked.connect(self.click_chiffre)
        self.pushButton_9.clicked.connect(self.click_chiffre)
        self.pushButton_10.clicked.connect(self.click_chiffre)
        self.pushButton_annuler.clicked.connect(self.click_annuler)

        # Empêche la saisie clavier dans la zone de mot de passe et l'associe à une variable
        self.zoneMDP.setReadOnly(True)

    def click_chiffre(self):
        # Ajoute le texte du bouton cliqué à la zone de mot de passe
        button = self.sender()
        self.zoneMDP.insert(button.text())

    def click_annuler(self):
        # Efface le mot de passe
        self.zoneMDP.setText('')

if __name__=='__main__':
    app=QApplication(sys.argv)
    accueil=ACCUEIL()
    widget=QtWidgets.QStackedWidget()
    widget.addWidget(accueil)
    widget.setFixedHeight(850)
    widget.setFixedWidth(1100)
    widget.show()
    app.exec_()

