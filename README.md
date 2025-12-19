# EVAP-CRIS  
## Simulation d’évaporation triple effet et cristallisation sucrière

Projet académique de **Génie des Procédés** visant à modéliser et simuler  
les opérations unitaires d’**évaporation multi-effet** et de  
**cristallisation du saccharose**, avec visualisation des résultats via  
une application web.


## <img width="24" height="24" alt="cible" src="https://github.com/user-attachments/assets/92987b6f-960b-441f-b8d2-b275b8ecda81" /> Objectifs du projet

- Simuler un évaporateur à **triple effet**
- Modéliser le processus de **cristallisation**
- Réaliser les **bilans matière et énergie**
- Dimensionner les principaux équipements
- Effectuer une **analyse technico-économique**
- Visualiser les résultats sous forme de **graphiques interactifs**



## <img width="24" height="24" alt="chimie" src="https://github.com/user-attachments/assets/6e40da09-242a-4407-b843-351fb76ffbe4" /> Domaine d’application

Ce projet s’inscrit dans le cadre du **Génie des Procédés**, notamment :

- Industrie sucrière
- Évaporation multi-effet
- Cristallisation industrielle
- Thermodynamique appliquée
- Calcul scientifique et modélisation



## <img width="24" height="24" alt="outils-de-reparation" src="https://github.com/user-attachments/assets/a826d630-191b-4491-acbc-ff2df28a84d1" /> Technologies utilisées

### <img width="24" height="24" alt="programmation-web" src="https://github.com/user-attachments/assets/58d09153-1264-4bf0-ab37-3a8bfae8142b" /> Langages & Frameworks

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow?logo=javascript)
![HTML5](https://img.shields.io/badge/HTML5-Markup-orange?logo=html5)
![CSS3](https://img.shields.io/badge/CSS3-Style-blue?logo=css3)

### <img width="24" height="24" alt="calculatrice-scientifique" src="https://github.com/user-attachments/assets/4f4bf6f1-9da6-46c3-a3f4-7f1f897f450b" /> Calcul scientifique & visualisation
![NumPy](https://img.shields.io/badge/NumPy-Scientific-blue?logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Graphs-green)
![CoolProp](https://img.shields.io/badge/CoolProp-Thermodynamics-red)

### <img width="24" height="24" alt="soutien-technique" src="https://github.com/user-attachments/assets/96897f1e-9e8a-4a62-aa40-aa1756808380" /> Outils & Environnement
![Git](https://img.shields.io/badge/Git-VersionControl-orange?logo=git)
![GitHub](https://img.shields.io/badge/GitHub-Repository-black?logo=github)
![VS Code](https://img.shields.io/badge/VS%20Code-Editor-blue?logo=visualstudiocode)

## <img width="24" height="24" alt="application" src="https://github.com/user-attachments/assets/cb3d38ab-7f1f-492c-8c1d-1364bfc75ff4" /> Aperçu de l’application

L’application web permet :

- La saisie des paramètres opératoires
- L’exécution des calculs numériques en Python
- La génération automatique de graphiques
- L’affichage structuré des résultats
- Le téléchargement des figures produites

Interface développée avec **Flask**, **Bootstrap** et **JavaScript**.



## 📂 Structure du projet

```text
EVAP-CRIS/
│
├── app/
│   ├── app_flask.py
│   ├── evaporateurs.py
│   ├── cristallisation.py
│   ├── thermodynamique.py
│   ├── optimisation.py
│   ├── economie.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── main.js
│
├── resultats/          
│   ├── graphiques/         
│   └── .gitkeep
│
├── README.md
├── requirements.txt
└── .gitignore
