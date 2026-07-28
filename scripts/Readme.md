# Déploiement de la plateforme dans un conteneur Docker

## Description

Afin de simplifier le déploiement de l'environnement expérimental et de garantir la reproductibilité des tests, l'ensemble de la plateforme a été intégré dans **un unique conteneur Docker**.
Ce conteneur regroupe tous les composants nécessaires à la simulation d'attaques GPS Spoofing ainsi qu'à leur détection par intelligence artificielle. L'utilisateur n'a donc pas besoin d'installer individuellement ArduPilot, Gazebo, QGroundControl, les dépendances Python ou les bibliothèques d'apprentissage profond sur sa machine hôte.
Le conteneur fournit un environnement Linux complet dans lequel tous les logiciels sont déjà configurés et interconnectés.

---

# Architecture générale

Le conteneur contient les éléments suivants :

```
                 +------------------------------------------------+
                 |                Docker Container                 |
                 |                                                |
                 |  +------------------------------------------+  |
                 |  | Gazebo Harmonic                         |  |
                 |  +------------------------------------------+  |
                 |                     │                          |
                 |                     ▼                          |
                 |  +------------------------------------------+  |
                 |  | ArduPilot SITL                          |  |
                 |  +------------------------------------------+  |
                 |          │                 │                  |
                 |          │                 │                  |
                 |          ▼                 ▼                  |
                 |   QGroundControl      attaque.py             |
                 |                           │                  |
                 |                           ▼                  |
                 |                     detect.py                |
                 |                                                |
                 +------------------------------------------------+
```

Tous les composants communiquent via le protocole **MAVLink** en utilisant des connexions UDP internes au conteneur.

---

# Contenu du conteneur

Le conteneur embarque les logiciels suivants :

- Ubuntu Linux ;
- Docker Runtime ;
- Gazebo Harmonic ;
- ArduPilot SITL ;
- MAVProxy ;
- QGroundControl ;
- Python 3 ;
- PyTorch ;
- pymavlink ;
- le modèle CNN-BiLSTM entraîné ;
- les scripts de simulation d'attaque ;
- le détecteur IA.

Ainsi, après le démarrage du conteneur, aucun téléchargement ou compilation supplémentaire n'est nécessaire.

---

# Script de simulation d'attaque : `attaque.py`

## Objectif

Le script **attaque.py** est responsable de la génération des scénarios de GPS Spoofing.
Il reçoit les messages MAVLink provenant d'ArduPilot SITL, applique une modification des données GPS puis retransmet les messages modifiés au détecteur IA.
En parallèle, lorsque le mode **--mode-both** est utilisé, il envoie également des commandes de navigation au véhicule simulé afin que le déplacement observé dans Gazebo et QGroundControl corresponde au GPS falsifié.

Le script joue ainsi un double rôle :

- simulateur d'attaque GPS ;
- proxy MAVLink entre le simulateur et le détecteur.

---

## Fonctionnement

Le fonctionnement du script peut être résumé comme suit :

1. connexion au flux MAVLink provenant d'ArduPilot ;
2. réception des messages GPS ;
3. attente d'un délai avant l'attaque ;
4. génération des coordonnées GPS falsifiées ;
5. modification des messages MAVLink ;
6. transmission du flux GPS modifié au détecteur IA ;
7. envoi éventuel des commandes de déplacement au véhicule.

---

## Modes de fonctionnement

Le simulateur propose trois modes :

### Mode SITL

```
--mode-sitl
```

Le script contrôle uniquement le véhicule simulé.

---

### Mode Proxy

```
--mode-proxy
```

Le script modifie les messages GPS et les transmet au détecteur sans déplacer le véhicule.

---

### Mode Complet

```
--mode-both
```

Le simulateur agit simultanément comme :

- proxy MAVLink ;
- générateur d'attaque GPS ;
- contrôleur du véhicule.

C'est le mode utilisé dans cette étude.

---

# Script de détection : `detect.py`

## Objectif

Le script **detect.py** constitue le système de détection intelligent.
Il écoute en permanence les messages MAVLink transmis par **attaque.py**, extrait automatiquement les caractéristiques GPS puis applique un modèle de Deep Learning afin de déterminer si les données reçues correspondent à une trajectoire normale ou à une attaque GPS Spoofing.
Le résultat est affiché en temps réel sous la forme :

```
✓ CLEAN
```

ou

```
⚠ SPOOFED
```

accompagné de la probabilité calculée par le modèle.

---

## Extraction des caractéristiques

Le détecteur extrait **23 caractéristiques** à partir des messages MAVLink.

Ces variables sont regroupées en plusieurs catégories.

| Catégorie | Caractéristiques |
|------------|------------------|
| Navigation | latitude, longitude, altitude, altitude ellipsoïdale |
| Qualité GPS | HDOP, VDOP, EPH, EPV |
| EKF | variances vitesse et compas |
| Satellites | nombre de satellites utilisés |
| Cinématique | vitesse totale, vitesses Nord, Est, Bas, cap |
| Variations | Δlatitude, Δlongitude, Δaltitude |
| Cohérence | vitesse calculée, cohérence des vitesses |
| Bruit | bruit par satellite, rapport HDOP/EPH |

Ces caractéristiques décrivent à la fois :

- la qualité du signal GPS ;
- le mouvement du véhicule ;
- les incohérences pouvant révéler une falsification.

---

## Modèle d'intelligence artificielle

Après extraction des caractéristiques, celles-ci sont normalisées puis regroupées dans une fenêtre temporelle de **30 trames**.
Le détecteur utilise ensuite un modèle de Deep Learning composé de :

- une couche de normalisation ;
- une projection des caractéristiques ;
- plusieurs blocs **BiLSTM résiduels** ;
- un mécanisme **Multi-Head Attention** ;
- une couche de classification finale.

Le modèle calcule la probabilité qu'une attaque GPS soit présente.
Lorsque cette probabilité dépasse le seuil défini, une alerte est immédiatement affichée.

---

## Résultats du modèle

Les performances obtenues lors de l'entraînement sont :

| Indicateur | Valeur |
|------------|---------|
| Accuracy | **0,82** |
| F1-score | **0,75** |
| Validation Loss | **0,39** |
| Nombre de caractéristiques | **23** |

Ces résultats montrent que le modèle est capable d'identifier des attaques GPS progressives, notamment les attaques de type **Drift**, qui sont généralement difficiles à détecter avec des règles statiques.

---

# Communication entre les scripts

Les deux scripts communiquent exclusivement via MAVLink.
Le flux de données est le suivant :

```
ArduPilot SITL
       │
       │ UDP :14552
       ▼
attaque.py
(simulation + proxy MAVLink)
       │
       │ GPS falsifié
       │ UDP :14553
       ▼
detect.py
(extraction des features +
détection IA)
```

---

# Avantages de cette architecture

L'intégration de l'ensemble de la plateforme dans un unique conteneur Docker présente plusieurs avantages :

- environnement entièrement reproductible ;
- aucune installation complexe sur la machine hôte ;
- isolation complète des dépendances logicielles ;
- exécution simultanée de la simulation, de l'attaque et de la détection ;
- architecture modulaire facilitant les expérimentations ;
- possibilité de tester différents scénarios de GPS Spoofing sans modifier le système hôte.

Cette architecture constitue ainsi une plateforme complète permettant de simuler des attaques GPS sur ArduPilot SITL et d'évaluer, en temps réel, les performances d'un détecteur basé sur un modèle CNN-BiLSTM.
