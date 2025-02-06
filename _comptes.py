from _ident_et_base import *

def tri_rapide_date(listeope):
    '''list -> list
    Permet de trier une liste d'opérations de la plus
    ancienne date à la plus récente.
    Le tri utilisé est un quicksort.
    '''
    def tri_rapide_jour(listeope):
        #Trie un liste d'opérations par rapport à leurs jours
        if listeope == []: 
            return []
        else:
            pivot = int(listeope[0][1].split('/')[0])
            moins = tri_rapide_jour([x for x in listeope[1:] if int(x[1].split('/')[0]) < pivot])
            plus = tri_rapide_jour([x for x in listeope[1:] if int(x[1].split('/')[0]) >= pivot])
            return moins + [listeope[0]] + plus
    def tri_rapide_mois(listeope):
        #Trie un liste d'opérations par rapport à leurs mois
        if listeope == []: 
            return []
        else:
            pivot = int(listeope[0][1].split('/')[1])
            moins = tri_rapide_mois([x for x in listeope[1:] if int(x[1].split('/')[1]) < pivot])
            plus = tri_rapide_mois([x for x in listeope[1:] if int(x[1].split('/')[1]) >= pivot])
            return moins + [listeope[0]] + plus
    def tri_rapide_annee(listeope):
        #Trie un liste d'opérations par rapport à leurs années
        if listeope == []:
            return []
        else:
            pivot = int(listeope[0][1].split('/')[2])
            moins = tri_rapide_annee([x for x in listeope[1:] if int(x[1].split('/')[2]) < pivot])
            plus = tri_rapide_annee([x for x in listeope[1:] if int(x[1].split('/')[2]) >= pivot])
            return moins + [listeope[0]] + plus
    
    #Tri complet des opérations.
    return tri_rapide_annee(tri_rapide_mois(tri_rapide_jour(listeope)))
    
def operations_stock(user,cipher):
    '''str x int --> tuple(dict x dict)
    Retourne la base de donnée d'un utilisateur sous forme
    de deux dictionnaires. Un pour les opérations,
    un pour les budgets et opérations associées.
    Les clées correspondent aux comptes.
    Les valeurs sont les opérations.
    '''
    assert type(user) is int or type(user) is str
    #Création des deux dictionnaires
    dictionnaire_ope=dict()
    dictionnaire_bud=dict()

    #Overture de la base de donnée de l'user
    #Et récupération de la première ligne
    fichier=open(chemin("users/" + chif_cesar(user,cipher) + ".txt"), "r")
    ligne=dechif_cesar(fichier.readline(),cipher).split('*')

    #Parcour du fichier
    while ligne!=['']:
        if ligne[0]=='CPT':
            #Création des clés (comptes) dans les deux dictionnaires.
            dictionnaire_ope[ligne[1]]=[]
            dictionnaire_bud[ligne[1]]=dict()
            dictionnaire_bud[ligne[1]]['budgets']=dict()

        if ligne[0]=='OPE':
            #Ajout de l'opération dans le dictionnaire opérations.
            #Et aussi dans le dictionnaire budget si l'opération est associée
            #à un budget. 
            dictionnaire_ope[ligne[3]].append(ligne)
            if (ligne[3] in dictionnaire_bud) and (ligne[-1] in dictionnaire_bud[ligne[3]]):
                if float(ligne[4])<0:
                    dictionnaire_bud[ligne[3]][ligne[-1]].append(ligne)

        if ligne[0]=='BUD':
            #Ajout du budget dans le dictionnaire budget, avec son montant.
            dictionnaire_bud[ligne[3]]['budgets'][ligne[1]] = float(ligne[2])
            if ligne[1] not in dictionnaire_bud[ligne[3]]:
                dictionnaire_bud[ligne[3]][ligne[1]] = []
        
        #Passage à la ligne suivante
        ligne=dechif_cesar(fichier.readline(),cipher).split('*')

    #Tri des opérations par dates. ancien -> récent.
    for i in dictionnaire_ope:
        dictionnaire_ope[i]=tri_rapide_date(dictionnaire_ope[i])
    for i in dictionnaire_bud:
        for j in dictionnaire_bud[i]:
            if j!='budgets':
                dictionnaire_bud[i][j]=tri_rapide_date(dictionnaire_bud[i][j])
    
    return dictionnaire_ope,dictionnaire_bud
#print(operations_stock('38654157',21)[1])


def ajouter_compte(ope_stock,BUD_stock,newcompte):
    '''dict x dict x str --> tuple
    Permet à l'utilisateur d'ajouter un compte.
    Si le compte existe déjà, aucun changement ne sera réalisé.
    '''
    assert type(newcompte) is str and len(newcompte)>0
    assert type(ope_stock) is dict
    if newcompte not in ope_stock:
        ope_stock[newcompte]=[]
    if newcompte not in BUD_stock:
        BUD_stock[newcompte]=dict()
        BUD_stock[newcompte]['budgets']=dict()
    return ope_stock,BUD_stock




def ajouter_virement(ope_stock,BUD_stock,compte1,compte2,date,montant,statut,budget):
    '''dict x dict x str x str x str x str x float x str x str --> tuple
    Permet à l'utilisateur de faire un virement entre deux de ses comptes.
    '''
    assert type(ope_stock) is dict
    assert type(compte1+compte2+date+str(montant)+statut+budget) is str
    if compte1==compte2:
        return ope_stock
    
    #Ajout de l'operation dans le dictionnaire ope.
    virement_compte1=['OPE',date,compte1,compte2,str(montant),'VIR',statut,budget]
    virement_compte2=['OPE',date,compte2,compte1,str(-montant),'VIR',statut,'']
    ope_stock[compte2].append(virement_compte1)
    ope_stock[compte1].append(virement_compte2)

    #On verifie si l'ope est associée à un budget.
    if budget in BUD_stock[compte2]['budgets']:
        #Ajout de l'operation dans le dictionnaire bud.
        BUD_stock[compte2][budget].append(virement_compte2)
    
    #On retourne les dictionnaires.
    return ope_stock,BUD_stock



def ajouter_operation(ope_stock,BUD_stock,compte,date,libelle,montant,typeOPE,statut,budget):
    '''
    dict x dict x str x str x str x str x str x str x str --> tuple
    Permet à l'utilisateur d'ajouter une opération sur un de ses comptes.
    '''
    assert type(ope_stock) is dict and type(typeOPE) is str and type(statut) is str
    assert type(compte) is str and type(date) is str and type(budget) is str
    assert (type(montant) is int) or (type(montant) is float)
    assert len(str(montant))>0 and montant!=0 and len(libelle)>0

    #Ajout de l'operation dans le dictionnaire ope.
    operation=['OPE',date,libelle,compte,str(montant),typeOPE,statut,budget]
    ope_stock[compte].append(operation)

    #Ajout de l'operation dans le dictionnaire budget.
    if budget in BUD_stock[compte]['budgets'] and montant<0:
        BUD_stock[compte][budget].append(operation)
    
    #On retourne les dictionnaires.
    return ope_stock,BUD_stock


def solde(compte,ope_stock):
    '''str x dict --> float
    Permet d'obtenir le solde d'un des compte d'un utilisateur à partir
    d'un dictionnaire des operations de ses comptes.
    '''
    total=0
    if compte in ope_stock:
        for i in ope_stock[compte]:
            total+=float(i[4])

    #On arrondis pour eviter les problemes d'affichage.
    return round(total,2)



####### ----------- SEULEMENT POUR PARTIE TEXTUELLE ----------- #######

def affiche_comptes(ope_stock):
    ''' dict --> None
    Affiche tous les comptes d'un utilisateur à partir d'un
    dictionnaire des operations de ses comptes.

    Ne sert que pour la partie textuelle !
    '''
    assert type(ope_stock) is dict
    liste_comptes=list(ope_stock.keys())
    for i in range(len(liste_comptes)):
        print(str(i+1)+'-',liste_comptes[i])

def affiche_ope_compte(ope_stock,compte='Compte A'):
    '''dict x str --> None
    Affiche toutes les opérations d'un des comptes d'un utilisateur à
    partir d'un dictionnaire des operations de ses comptes.
    
    Ne sert que pour la partie textuelle !
    '''
    assert type(ope_stock) is dict
    assert type(compte) is str
    for i in ope_stock[compte]:
        print(i[1:3]+i[4:5]+i[6:])       

def pas_doublons(ope_stock,newcompte):
    '''dict x str --> bool
    Permet de s'assurer qu'un compte n'apparaissae pas deux fois
    dans un même fichier.

    Ne sert que pour la partie textuelle !
    '''
    if newcompte in ope_stock:
        return False
    return True


def premier_compte(user,cipher):
    '''str x int --> str
    Retourne le premier compte qui apparaît dans 
    la base de données d'un utilisateur.

    Ne sert que pour la partie textuelle !
    '''
    #Ouverture de la base de donnée de l'utilisateur.
    fichier=open(chemin("users/" + chif_cesar(user,cipher) + ".txt"), "r")

    #On retourne la première ligne du fichier.
    return dechif_cesar(fichier.readline(),cipher).split('*')[1]
