from _ident_et_base import *
import _comptes
from _gestion_budget import *

def identification():
    essais=2
    #identifiant = input('Veuillez entrez votre identifiant : ')
    #mot_de_passe = input('Veuillez entrer votre mot de passe : ')
    identifiant = '38654157'
    mot_de_passe = '144166'
    while not check_user(identifiant,mot_de_passe)[0] and essais>0:
        print('Identiant ou mot de passe erroné, veuillez les rentrer à nouveau.')
        identifiant = input('Veuillez entrez votre identifiant : ')
        mot_de_passe = input('Veuillez entrer votre mot de passe : ')
        essais-=1
    if essais == 0 and not check_user(identifiant,mot_de_passe)[0]:
        print('Nombre maximal de tentatives atteint...')
        return (False,0,'',0)
    else:
        condition , line, cipher = check_user(identifiant,mot_de_passe)
        name=dechif_cesar(line.split('*')[2],int(cipher))
        ident=dechif_cesar(line.split('*')[0],int(cipher))
        print('\nBienvenue '+name+'.\n')
        return (condition, ident, name, cipher)

def choix():
    compte = premier_compte(user,cipher)
    budget = premier_BUD(user,cipher,compte)
    selection=input('Choisissez une action parmi les suivantes :\n\n'
                 '1->Gérer vos comptes    2->Gérer vos budgets    '
                 '3->Déconnexion\n---> ')
    if selection == '1':
        comptes(user,compte)
    elif selection == '2' :
        gestion_bud(user,compte,budget)
    elif selection == '3':
        connexion()
    else:
        print('Veuillez entrer un nombre valide.')
        connexion()

def gestion_bud(user,compte,budget,mois='Janvier',annee='2023'):
    print('---------------------------------------------------------------------')
    ope_stock,BUD_stock = operations_stock(user,cipher)
    listemois = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet',\
                 'Août','Septembre','Octobre','Novembre','Décembre']
    print('\n\nOpérations avec paramètres :',compte,'->',budget,'->',mois,'->',annee)
    print('\n\nSolde du compte :',solde(compte,ope_stock))
    print('Budget fixé :',soldeBUD(BUD_stock,compte,budget))
    print('Budget restant :',difference(BUD_stock,compte,budget))
    print('Dépenses :',depenses(BUD_stock,compte,budget),'\n')
    affiche_ope_bud(BUD_stock,compte,budget,mois,annee)
    selection=input('\nVoulez-vous :\n\n'
                    '1- Changer de compte   2- Changer de budget\n'
                    '3- Changer de mois     4- Ajouter un budget\n'
                    '5- Changer l\'année    0- Revenir aux choix \n\n---> ')
    if selection == '0':
        print('---------------------------------------------------------------------')
        choix()
    elif selection == '1' :
        print('\n\nVoici tous vos comptes :\n')
        affiche_comptes(ope_stock)
        num = input('\nEntrez le numéro du compte souhaité :\n---> ')
        try :
            compte = list(ope_stock.keys())[int(num)-1]
            gestion_bud(user,compte,premier_BUD(user,cipher,compte),'Janvier')
        except :
            print('\n\nVeuillez entrer un nombre valide.\n\n')
            gestion_bud(user,compte,budget,mois)
    elif selection == '2':
        print('\n\nVoici tous vos budgets :\n')
        affiche_BUD(BUD_stock,compte)
        num = input('\nEntrez le numéro du budget souhaité :\n---> ')
        try :
            budget = list(BUD_stock[compte]['budgets'].keys())[int(num)-1]
            gestion_bud(user,compte,budget,mois)
        except:
            print('\n\nVeuillez entrer un nombre valide.\n\n')
            gestion_bud(user,compte,budget,mois)
    elif selection == '3':
        try:
            month = int(input('Veuillez entrer le nombre du mois souhaité : (Février -> 2)\n---> '))
            if 1<=month<=12 :
                gestion_bud(user,compte,budget,listemois[month-1])
            else:
                print('\n\nVeuillez entrer un nombre entier valide.\n\n')
                gestion_bud(user,compte,budget,mois)
        except:
            print('\n\nVeuillez entrer un nombre entier valide.\n\n')
            gestion_bud(user,compte,budget,mois)
    elif selection == '4':
        print('\n\nVoici tous vos comptes :\n')
        affiche_comptes(ope_stock)
        cmpt = input('\nVeuillez entrer le numéro du compte du nouveau budget :\n---> ')
        bud = input('Veuillez entrer le nom du budget à ajouter :\n---> ')
        mntnt = input('Veuillez entrer le montant du budget à ajouter :\n---> ')
        try:
            cmpt = list(ope_stock.keys())[int(cmpt)-1]
            mntnt = float(mntnt)
            BUDstock=ajouter_BUD(cmpt,bud,str(mntnt),BUD_stock)
            reorganiser(user,cipher,ope_stock,BUDstock)
            print('\n\nL\'opération a été effectuée avec succès.')
            gestion_bud(user,cmpt,bud,mois)
        except:
            print('\n\nVeuillez entrer des valeurs valides.\n\n')
            gestion_bud(user,compte,budget,mois)
    elif selection == '5':
        try:
            year = input('Veuillez entrer le l\'année souhaitée : (aaaa)\n---> ')
            gestion_bud(user,compte,budget,mois,year)
        except:
            print('\n\nVeuillez entrer un nombre entier valide.\n\n')
            gestion_bud(user,compte,budget,mois,annee)
    else :
        print('Veuillez entrer un nombre valide.')
        gestion_bud(user,compte,budget,mois)

def comptes(user,compte):
    print('---------------------------------------------------------------------')
    ope_stock,BUD_stock=operations_stock(user,cipher)
    print('\nOperations de votre',compte,':\n')
    print('Solde :', solde(compte,ope_stock),'\n')
    affiche_ope_compte(ope_stock,compte)
    selection=input('\nVoulez-vous :\n\n'
                '1- Changer de compte       2- Ajouter une opération\n'
                '3- Effectuer un virement   4- Ajouter un compte\n'
                '0- Revenir aux choix \n\n---> ')
    if selection == '0':
        print('---------------------------------------------------------------------')
        choix()
    elif selection == '1' :
        print('\n\nVoici tous vos comptes :\n')
        affiche_comptes(ope_stock)
        num = int(input('\nEntrez le numéro du compte souhaité :\n---> '))
        try :
            comptes(user,list(ope_stock.keys())[num-1])
        except :
            print('\n\nVeuillez entrer un nombre valide.\n\n')
            comptes(user,compte)
    elif selection == '2':
        print('\n\nVoici tous vos comptes :\n')
        affiche_comptes(ope_stock)
        compte1 = input('\nVeuillez entrer le numéro du compte sur lequel vous'
                       ' voulez ajouter une opération :\n---> ')
        date = input('Veuillez entrez une date (jj/mm/aaaa):\n---> ')
        libelle = input('Veuillez entrer le libellé de l\'opération :\n---> ')
        montant = input('Veuillez entrer le montant de l\'opération :\n---> ')
        typeOPE = input('Veuillez entrer le moyen utilisé (CB - CHE - VIR) :\n---> ')
        statut = input('Veuillez entrer le statut de l\'operations (True ou False):\n---> ')
        budget = input('Veuillez entrer le budget concerné :\n---> ')
        try:
            compte1 = list(ope_stock.keys())[int(compte1)-1]
            opestock = ajouter_operation(ope_stock,compte1,date,libelle,float(montant),typeOPE,statut,budget)
            reorganiser(user,cipher,opestock,BUD_stock)
            print('\n\nL\'opération a été effectuée avec succès.')
        except:
            print('Veuillez entrer des valeurs valides.')
        comptes(user,compte)
    elif selection == '3':
        print('\n\nVoici tous vos comptes :\n')
        affiche_comptes(ope_stock)
        comptelis = list(ope_stock.keys())
        compte1 = input('\nVeuillez entrer le compte sur lequel vous voulez retirer.\n---> ')
        compte2 = input('Veuillez entrer le compte que vous voulez approvisionner.\n---> ')
        date = input('Veuillez entrer le jour :\n---> ')
        montant = input('Veulliez entrer le montant que vous voulez virer :\n---> ')
        statut = input('Veulliez entrer le statut de l\'opération :\n---> ')
        budget = input('Veulliez entrer le budget concerné :\n---> ')
        try:
            compte1 = comptelis[int(compte1)-1]
            compte2 = comptelis[int(compte2)-1]
            opestock = ajouter_virement(ope_stock,compte1,compte2,date,float(montant),statut,budget)
            reorganiser(user,cipher,opestock,BUD_stock)
            print('\n\nLe virement a été effectué avec succès.')
        except:
            print('Veuillez entrer des valeurs valides.')
        comptes(user,compte)
    elif selection == '4':
        print('\n\nVoici tous vos comptes :\n')
        affiche_comptes(ope_stock)
        lettrecompte=input('Veuillez entrer une lettre pour votre nouveau compte :\n---> ')
        if pas_doublons(ope_stock,lettrecompte) and bonne_lettre(lettrecompte):
            opestock=ajouter_compte(ope_stock,lettrecompte)
            reorganiser(user,cipher,opestock,BUD_stock)
            print('Votre compte a été créé avec succès.')
        else:
            print('Erreur, le compte que vous voulez créer existe déjà.')
        comptes(user,compte)
    else :
        print('Veuillez entrer un nombre valide.')
        comptes(user,compte)

condition, user, name, cipher, compte, budget = 0,0,0,0,0,''
def connexion():
    global condition, user, name, cipher, compte, budget
    condition, user, name, cipher=identification()
    if condition : 
        choix()
connexion()
#38654157 144166  
