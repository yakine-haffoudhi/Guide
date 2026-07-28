# gps_circle_spoof.py

Script d'injection GPS falsifié via MAVLink — simule un drone qui tourne en cercle autour d'un point fixe, indépendamment de sa position réelle dans le simulateur.

## Description

Le script se connecte à ArduPilot SITL sur le port UDP `14552` (dédié, pour laisser le port `14550` libre pour QGroundControl) et lui envoie en boucle des messages `GPS_INPUT` MAVLink calculés pour décrire une trajectoire circulaire autour d'un point central fixe (par défaut : IMT Atlantique, Brest).

Comme SITL accepte ce flux GPS externe comme source de vérité, le drone "croit" suivre ce cercle même si sa position réelle (physique/simulée) est différente — c'est une attaque de type **GPS spoofing par injection**.

## Paramètres 

| Variable | Description | Valeur par défaut |
|---|---|---|
| `center_lat` / `center_lon` | Centre du cercle, en degrés × 1e7 | IMT Atlantique Brest (48.3579, -4.5714) |
| `radius` | Rayon du cercle en unités × 1e7 de degré (~500 m) | `50000` |
| `angle` step | Incrément d'angle par itération (degrés) | `2` |
| `time.sleep(...)` | Fréquence d'envoi des trames | `1.0` s |
| Port d'écoute | Port UDP MAVLink dédié au script | `14552` |

## Utilisation

```bash
python3 gps_circle_spoof.py
```

Le script :
1. Attend un heartbeat MAVLink de SITL sur le port `14552` (timeout 30 s)
2. Une fois connecté, envoie en continu des positions GPS calculées point par point sur le cercle
3. Affiche à chaque itération l'angle courant et la position injectée (`lat`, `lon`)
