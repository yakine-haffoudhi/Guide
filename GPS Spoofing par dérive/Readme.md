# GPS Drift Spoofer – ArduPilot SITL

## Description

Ce code implémente un **GPS Drift Spoofer** destiné à un environnement **ArduPilot SITL** (Software In The Loop). Le programme se connecte au pilote automatique via **MAVLink**, récupère les données GPS réelles, calcule une dérive progressive de la position, puis envoie une position GPS falsifiée afin de simuler une attaque de type **GPS Spoofing**.

---

# Fonctionnement

Le programme suit les étapes suivantes :

1. Connexion à ArduPilot via MAVLink.
2. Attente du message Heartbeat.
3. Lecture des messages GPS (`GPS_RAW_INT`) et de position (`GLOBAL_POSITION_INT`).
4. Attente d'un délai avant le début de l'attaque.
5. Calcul d'une position GPS falsifiée en fonction d'une vitesse et d'une direction.
6. Envoi de cette position via le message MAVLink `SET_POSITION_TARGET_GLOBAL_INT`.
7. Affichage en temps réel de la dérive appliquée.

---

# Structure du code

## `compute_drift()`

Cette fonction calcule la position GPS falsifiée.

### Paramètres

- `real` : position GPS réelle.
- `rate` : vitesse de dérive (m/s).
- `direction_rad` : direction en radians.
- `elapsed` : temps écoulé depuis le début de l'attaque.

### Fonctionnement

La distance parcourue est calculée par :

```
distance = vitesse × temps
```

Puis cette distance est convertie en variation de latitude et de longitude.

---

## `send_position()`

Cette fonction construit et envoie un message MAVLink :

```
SET_POSITION_TARGET_GLOBAL_INT
```

Les coordonnées GPS sont converties au format MAVLink :

```
latitude × 10⁷
longitude × 10⁷
```

Les champs vitesse, accélération et orientation sont ignorés grâce au masque `TYPE_MASK`.

---

## `dist_m()`

Cette fonction calcule la distance entre la position réelle et la position falsifiée.

Elle est utilisée uniquement pour afficher la dérive en mètres.

---

## `main()`

La fonction principale réalise :

- lecture des arguments de la ligne de commande ;
- connexion au drone via MAVLink ;
- récupération des données GPS ;
- attente avant le lancement de l'attaque ;
- génération de la position falsifiée ;
- envoi des coordonnées modifiées ;
- affichage de l'évolution de la dérive.

---

# Paramètres disponibles

## Connexion MAVLink

```
--connection
```

Valeur par défaut :

```
udp:0.0.0.0:14552
```

---

## Vitesse de dérive

```
--drift-rate
```

Exemple :

```
--drift-rate 0.5
```

La position GPS sera déplacée de **0,5 mètre par seconde**.

---

## Direction

```
--direction
```

| Valeur | Direction |
|--------|-----------|
| 0 | Nord |
| 90 | Est |
| 180 | Sud |
| 270 | Ouest |

---

## Délai avant attaque

```
--pre-attack
```

Nombre de secondes à attendre avant le début du GPS Spoofing.

---

# Exemple d'utilisation

```bash
python3 gps_drift_spoofer.py \
    --connection udp:0.0.0.0:14552 \
    --drift-rate 1 \
    --direction 90 \
    --pre-attack 10
```

Dans cet exemple :

- la connexion est établie sur le port UDP 14552 ;
- l'attaque commence après 10 secondes ;
- la position GPS dérive progressivement vers l'Est à une vitesse de 1 m/s.

---

# Affichage

Avant l'attaque :

```
PRE-ATTAQUE

lat=...
lon=...
satellites=...
hdop=...
```

Pendant l'attaque :

```
DRIFT

Dpos=15.2 m

real=(...)
spoof=(...)
cmds=245
```

où :

- **Dpos** est la distance entre la position réelle et la position falsifiée ;
- **real** correspond aux coordonnées GPS réelles ;
- **spoof** correspond aux coordonnées GPS envoyées ;
- **cmds** indique le nombre de messages MAVLink transmis.

---

# Architecture

```
                GPS_RAW_INT
           GLOBAL_POSITION_INT
                     │
                     ▼
        +-------------------------+
        |  GPS Drift Spoofer      |
        |                         |
        | - lecture du GPS        |
        | - calcul de la dérive   |
        | - génération du spoof   |
        +-------------------------+
                     │
                     │
     SET_POSITION_TARGET_GLOBAL_INT
                     │
                     ▼
             ArduPilot SITL
```

---

# Objectif

Ce projet permet d'étudier :

- le fonctionnement des messages MAVLink ;
- la manipulation des coordonnées GPS ;
- la simulation d'une dérive GPS progressive ;
- l'impact potentiel d'une attaque de type GPS Spoofing sur un pilote automatique dans un environnement de simulation sécurisé.
