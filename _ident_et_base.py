from os.path import join,dirname

def chemin(s):
    '''str --> str
    retourne le chemin d'un fichier
    (fonction créée pour une meilleure compatibilité entre les OS)
    '''
    return join(dirname(__file__), s)

def chif_cesar(string,cle):
    '''str x int --> str
    Renvoie une chaine de caractère chiffrée en césar.
    '''
    assert type(string) is str or type(string) is int
    assert type(cle) is int
    if type(string) is int:
        string=str(string)
    mot=''
    for i in string:
        if i == "\n":
            mot+=""
        elif i.isdigit():#Verification : nombre
            mot+=str((int(i)+cle)%10)
        elif not (i in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            mot+=i
        elif i.isupper():#Verification : majuscule
            mot+=chr((ord(i)+cle-65)%26+65)
        elif i.islower():#Verification : minuscule
            mot+=chr((ord(i)+cle-97)%26+97)
        else :
            mot+=i
    return mot
        
def dechif_cesar(string,cle):
    '''str x int --> str
    Déchiffre une chaine de caractère chiffrée en césar.
    '''
    assert type(string) is str or type(string) is int
    assert type(cle) is int 
    if type(string) is int:
        string=str(string)
    mot=''
    for i in string:
        if i == "\n":
            mot+=""
        elif i.isdigit():
            mot+=str((int(i)-cle)%10)
        elif not (i in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            mot+=i
        elif i.isupper():
            mot+=chr((ord(i)-cle-65)%26+65)
        elif i.islower() :
            mot+=chr((ord(i)-cle-97)%26+97)
        else:
            mot+=i
    return mot
#print(dechif_cesar('WPY*gjydwdyôi*31111*Xjhkoz V',21))

def findline(iduser):
    '''int or str --> tuple
    Cherche l'utilisateur dans le fichier texte et
    Renvoie un tuple contenant :
    bool , ligne de l'utilisateur , clé de chiffrement
    '''
    assert type(iduser) is int or type(iduser) is str
    doc = open(chemin('ident.txt'), "r")
    ligne=doc.readline()
    while ligne!='':
        #On efface \n (saut de ligne) s'il est présent
        if ligne[-1]=='\n':
            ligne=ligne[:-1]
        
        #clé de chiffrement
        cipher=ligne.split('*')[-1]

        #Reherche l'user dans la ligne actuelle
        if chif_cesar(iduser,int(cipher)) == ligne.split('*')[0]:
            #User trouvé 
            return (True,ligne,cipher)
        
        #Passage à la ligne suivante
        ligne = doc.readline()
    
    #User non trouvé dans la base de donnée.
    return (False,"",0)

def check_user(iduser,mdp):
    '''(str or int) x (str or int) --> tuple (bool,str,int)
    Return True si l'identifiant et le mot de passe sont corrects
    False sinon.
    '''
    assert type(iduser) is str or type(iduser) is int
    assert type(mdp) is str or type(mdp) is int 
    condition , line, cipher=findline(iduser)

    #Si le l'identififant d'utilisateur a été trouvé
    if condition:

        #Vérification du mot de passe dans la ligne de l'utilisateur
        if chif_cesar(mdp,int(cipher)) == line.split('*')[1]:

            #Mot de passe trouvé, donc correct.
            return (True,line,int(cipher))
            
    #Identifiant ou mot de passe incorrect.
    return (False,'',0)

def est_date_valide(date):
    '''str -> bool
    Revoie True si la date entrée existe vraiment, False sinon.
    Exemples : '29/02/2023' -> False
               '29/02/2024' -> True
    '''
    date=date.split('/')
    jour, mois, annee=int(date[0]),int(date[1]),int(date[2])
    jours_par_mois = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if annee%4==0 and (annee%100 != 0 or annee%400==0):
        jours_par_mois[1] = 29
    return (1 <= mois <= 12 and 1 <= jour <= jours_par_mois[mois-1])
#print(est_date_valide('29/02/2024'))








































