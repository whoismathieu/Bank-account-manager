from _ident_et_base import *
from _comptes import *

def date_to_mois(liste):#New
    '''list --> str
    Renvoie le mois d'une opération.
    Exemple : ['OPE', '01/01/2022', 'etc'] --> 'Janvier'
    '''
    assert type(liste) is list and len(liste)>=2
    liste_mois=['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août',\
    'Septembre','Octobre','Novembre','Décembre']
    return liste_mois[int(liste[1].split('/')[1])-1]

def date_to_annee(liste,annee):#New
    '''list x str --> bool
    Renvoie le True si l'année de l'opération correspond.
    False sinon.
    '''
    assert type(liste) is list and len(liste)>=2
    if liste[1].split('/')[2]==annee:
        return True
    return False
#print(date_to_annee(['OPE', '01/01/2022', 'cinema', 'Compte A', '-18.50', 'CB', 'False', 'sorties'],'2022'))

def operations_budget(BUD_stock,compte,budget,mois,annee):#New 
    '''dict x str x str x str x str --> list
    Renvoie les operations d'un compte pour un mois et une année choisie. 
    '''
    assert type(BUD_stock) is dict
    assert type(compte) is str and type(budget) is str and type(mois) is str
    
    if compte not in BUD_stock:
        return []
    if budget not in BUD_stock[compte]:
        return []
    mois=mois.capitalize()
    return [i for i in BUD_stock[compte][budget] if (date_to_mois(i)==mois and date_to_annee(i,annee))]
#print(operations_budget(operations_BUD(38654157),'Compte B','alimentation','janvier'))


def depenses(BUD_stock,compte,budget,mois,annee):#New
    '''dict x str x str x str x str --> Number
    Retourne la somme des dépenses d'un compte.
    '''
    if compte not in BUD_stock:
        return 0
    if budget not in BUD_stock[compte]:
        return 0
    count=0
    for i in operations_budget(BUD_stock,compte,budget,mois,annee):
        negatif=float(i[4])
        if negatif<0:
            count+=negatif
    return round(count,2)
#print(depenses(operations_BUD(38654157),'Compte A','divers','Janvier'))


def soldeBUD(BUD_stock,compte,budget):
    '''dict x str x str --> number
    Retourne le montant du budget recherché.
    '''
    if compte not in BUD_stock:
        return 0
    if 'budgets' not in BUD_stock[compte]:
        return 0
    solde=BUD_stock[compte]['budgets']
    if budget in solde:
        return round(solde[budget],2)
    return 0
#print(soldeBUD(operations_BUD(38654157),'Compte A','divers'))

def difference(BUD_stock,compte,budget,mois,annee):
    '''dict x str x str x str x str--> number
    Retourne le solde restant du budget concerné.
    '''
    return soldeBUD(BUD_stock,compte,budget) + depenses(BUD_stock,compte,budget,mois,annee)
#print(difference(operations_BUD(38654157),'Compte A','divers','Janvier'))


def ajouter_BUD(compte,budget,montant,BUD_stock):
    '''str x str x str x dict --> dict
    Permet d'ajouter une ligne de budget dans la base de
    donnée d'un utilisateur.
    '''
    assert len(budget)>0
    if compte in BUD_stock and budget not in BUD_stock[compte]['budgets']:
        BUD_stock[compte]['budgets'][budget]=float(montant)
        BUD_stock[compte][budget]=[]
    return BUD_stock
#print(ajouter_BUD('Compte B','chupapi','700',operations_BUD('38654157')))

def liste_to_str(liste_ope):
    '''list --> str
    Transforme une liste en chaine de caracteres separées par des étoiles.
    Ex : ['OPE','01/01/2022','cinema','Compte A','18.50','CB','False','sorties']
         --> OPE*01/01/2022*cinema*Compte A*18.50*CB*False*sorties 
    '''
    assert len(liste_ope)>0
    s=''
    for i in range(len(liste_ope)-1):
        s+=liste_ope[i]+'*'
    s+=liste_ope[-1]
    return s
#print(liste_to_str(['OPE','01/01/2022','cinema','Compte A','18.50','CB','False','sorties']))


def reorganiser(user,cipher,ope_stock,BUD_stock):
    '''str x int x dict x dict --> None
    Permet de reorganiser la base de donnée d'un utilisateur 
    dans l'ordre de ses comptes.
    '''
    #Ouverture du fichier.
    fichier = open(chemin("users/" + chif_cesar(user,cipher) + ".txt"),'w')

    #Ecriture des comptes.
    for i in ope_stock:
        #print(chif_cesar(i,cipher))
        fichier.write(chif_cesar('CPT*'+i,cipher)+'\n')

    #Ecriture des budgets
    for i in BUD_stock:
        for j in BUD_stock[i]['budgets'] :
            bud='BUD*'+j+'*'+str(BUD_stock[i]['budgets'][j])+'*'+i
            #print(chif_cesar(bud,cipher))
            fichier.write(chif_cesar(bud,cipher)+'\n')
    
    #Ecriture des operations
    for i in ope_stock:
        for j in ope_stock[i]:
            #print(chif_cesar(liste_to_str(j),cipher))
            fichier.write(chif_cesar(liste_to_str(j),cipher)+'\n')

#print(reorganiser('38654157',21,operations_stock('38654157'),operations_BUD('38654157')))
#print(operations_stock('38654157'))
#print(dechif_cesar('JKZ*13/15/3134*xgvqdzm*Xjhkoz W*-291.1*XW*Avgnz*jxxvndjiizg',21))



####### ----------- SEULEMENT POUR PARTIE TEXTUELLE ----------- #######

def affiche_ope_bud(BUD_stock,compte,budget,mois,annee):
    '''dict x str x str x str x str --> None
    Affiche en cascade les operations correspondant aux critères choisis.

    Ne sert que pour la partie textuelle ! 
    '''
    for i in operations_budget(BUD_stock,compte,budget,mois,annee):
        print(i[1:3]+i[4:6])
#affiche_ope_bud(operations_stock('38654157',21)[1],'Compte A','sorties','Janvier','2022'))

def liste_BUD(BUD_stock,compte):
    '''dict x str --> list
    retourne la liste les budgets d'un compte.

    Ne sert que pour la partie textuelle !
    '''
    if compte not in BUD_stock:
        return []
    if 'budgets' not in BUD_stock[compte]:
        return []
    t=[]
    for i in BUD_stock[compte]['budgets']:
        t.append(i)
    return t
#print(liste_BUD(operations_stock(38654157,21)[1],'Compte A'))

def premier_BUD(user,cipher,compte):
    '''str x int x str --> str
    Renvoie le premier budget apparaissant dans la base
    de donnée d'un utilisateur.
    
    Ne sert que pour la partie textuelle !
    '''
    l=open(chemin("users/" + chif_cesar(user,cipher) + ".txt"), "r")
    ligne = dechif_cesar(l.readline(),cipher).split('*')
    while  ligne != ['']:
        if ligne[0]=='BUD' and ligne[-1]==compte:
            return ligne[1]
        ligne = dechif_cesar(l.readline(),cipher).split('*')   
    return ''
#print(premierBUD('38654157',21))

def affiche_BUD(BUD_stock,compte):
    '''dict x str --> None
    Affiche en cascade les budgets du compte d'un
    utilisateur.

    Ne sert que pour la partie textuelle !
    '''
    c=1
    for i in BUD_stock[compte]['budgets']:
        print(str(c)+'-',i)
        c+=1
#affiche_BUD(operations_BUD(38654157),'Compte A')