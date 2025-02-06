# Gestion de Comptes Bancaires et de Budgets

Ce projet a été réalisé dans le cadre de l'Option Informatique 2 en L1 à l'Université Paris Cité (année universitaire 2022-2023) par Dylan LIN, Jacques ZHENG, Egemen YAPSIK et Matthieu MOUSTACHE.

---

## Description du Projet

L'objectif de ce projet était de développer une application graphique en Python permettant de gérer des comptes bancaires et des budgets d'un utilisateur. Le projet est divisé en trois parties principales :

1. **Phase d'Identification :**
   - Authentification via un identifiant et un mot de passe saisis sur un clavier virtuel.
   - Verification des identifiants dans un fichier texte crypté (algorithme de chiffrement de type César).

2. **Gestion des Comptes :**
   - Gestion de plusieurs comptes bancaires.
   - Ajout et gestion des opérations (virements, dépenses, etc.).
   - Stockage des informations dans des fichiers cryptés pour chaque utilisateur.

3. **Gestion des Budgets :**
   - Visualisation et suivi des dépenses par budget mensuel.
   - Configuration des budgets et allocation des dépenses aux différents budgets.

---

## Fonctionnalités Principales

- **Fenêtre d'authentification :**
  - Saisie de l'identifiant et du mot de passe.
  - Clavier virtuel avec agencement aléatoire des touches.

- **Fenêtre de bord :**
  - Visualisation de l'état du compte principal.
  - Accès aux onglets de gestion des comptes et des budgets.

- **Gestion des comptes :**
  - Affichage des soldes des comptes.
  - Ajout de nouvelles opérations et virements entre comptes.

- **Gestion des budgets :**
  - Configuration des budgets par compte.
  - Suivi des dépenses mensuelles.

---

## Structure des Données

Les données sont organisées dans des fichiers texte cryptés selon l'algorithme de chiffrement César :

- **Fichier `ident.txt` :** Contient les identifiants et les mots de passe des utilisateurs.
- **Fichiers par utilisateur :** Stockent les comptes, les budgets et les opérations associées.

### Exemple de structure d'un fichier utilisateur décrypté :
```
CPT*Compte A
CPT*Compte B
OPE*01/01/2022*cinema*Compte A*18.50*CB*False*sorties
OPE*06/01/2022*galette*Compte B*10.54*CB*True*alimentation
BUD*sorties*300.0*Compte A
BUD*divers*1000.0*Compte A
```

---

## Technologies Utilisées

- **Langage :** Python
- **Interface graphique :** PySide2 (QT Designer)
- **Algorithme de chiffrement :** César

---

## Choix de Conception

- Utilisation de fichiers texte cryptés pour le stockage des données, garantissant la sécurité.
- Sauvegarde immédiate des modifications pour prévenir les pertes de données.
- Organisation des données sous forme de dictionnaires pour une manipulation efficace.

---

## Instructions pour l’Exécution

1. Cloner le projet :
   ```bash
   git clone https://github.com/whoismathieu/Bank-account-manager
   cd Bank-account-manager
   ```

2. Installer les dépendances :
   ```bash
   pip install PySide2
   ```

3. Lancer l'application :
   ```bash
   python main.py
   ```

---

## Auteurs

- Dylan LIN
- Jacques ZHENG
- Egemen YAPSIK
- Matthieu MOUSTACHE
