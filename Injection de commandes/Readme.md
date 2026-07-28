# Contrôle des commandes ARM, DISARM et TAKEOFF via MAVLink

## Description

Ces deux scripts illustrent l'utilisation du protocole **MAVLink** pour envoyer des commandes de contrôle à un véhicule **ArduPilot** dans un environnement **SITL (Software In The Loop)**.

Le premier script réalise un **ARM forcé**, place le drone en mode **GUIDED**, puis lui envoie une commande de **décollage automatique**. Le second effectue un **DISARM forcé**, démontrant qu'un client MAVLink peut également ordonner l'arrêt des moteurs.

Ces exemples permettent de comprendre le fonctionnement des commandes critiques transportées par le message **COMMAND_LONG**.

---

# Fonctionnement

Les scripts suivent les étapes suivantes :

1. Connexion au véhicule via MAVLink.
2. Attente du message **Heartbeat**.
3. Identification du système cible.
4. Envoi d'une ou plusieurs commandes de contrôle.

Selon le script exécuté :

- **Force ARM & Takeoff**
  - Passage en mode **GUIDED**.
  - ARM forcé.
  - Décollage automatique à 30 mètres.

- **Force DISARM**
  - Désarmement forcé du véhicule.

---

# Structure des scripts

## Connexion MAVLink

```python
master = mavutil.mavlink_connection("udp:127.0.0.1:14550")
```

Les deux scripts ouvrent une connexion UDP vers ArduPilot sur le port **14550**.

---

## Attente du Heartbeat

```python
master.wait_heartbeat()
```

Le programme attend la réception d'un message **Heartbeat**, confirmant que la communication avec le pilote automatique est établie.

---

# Script 1 : Force ARM & Takeoff

## Passage en mode GUIDED

```python
master.set_mode("GUIDED")
```

Le drone est placé en mode **GUIDED**, ce qui autorise le contrôle du véhicule par des commandes MAVLink.

---

## ARM forcé

Le script envoie une commande :

```
MAV_CMD_COMPONENT_ARM_DISARM
```

avec les paramètres :

- **param1 = 1** → ARM
- **param2 = 21196** → ARM forcé

Le code **21196** permet de contourner certaines vérifications de sécurité réalisées avant l'armement.

---

## Décollage automatique

Une fois le drone armé, le script envoie :

```
MAV_CMD_NAV_TAKEOFF
```

Le dernier paramètre fixe l'altitude cible :

```
30 mètres
```

Le pilote automatique lance alors la procédure de décollage.

---

## Exemple d'exécution

```bash
python3 force_arm_takeoff.py
```

Sortie :

```
[+] Connecté — sys=1
[+] ARM forcé envoyé
[+] TAKEOFF 30 m injecté — observez QGC
```

---

# Script 2 : Force DISARM

## Désarmement forcé

Le second script envoie également une commande :

```
MAV_CMD_COMPONENT_ARM_DISARM
```

mais avec les paramètres :

- **param1 = 0** → DISARM
- **param2 = 21196** → désarmement forcé

Le pilote automatique reçoit alors une demande de désarmement, même si certaines conditions de sécurité ne sont pas remplies.

---

## Exemple d'exécution

```bash
python3 force_disarm.py
```

Sortie :

```
[+] Connecté — sys=1
[+] DISARM forcé en vol
```

---

# Messages MAVLink utilisés

| Message | Rôle |
|---------|------|
| `HEARTBEAT` | Vérifie la présence du véhicule |
| `COMMAND_LONG` | Transporte les commandes MAVLink |
| `MAV_CMD_COMPONENT_ARM_DISARM` | Arme ou désarme le drone |
| `MAV_CMD_NAV_TAKEOFF` | Lance une procédure de décollage automatique |

---

# Différences entre les deux scripts

| Fonction | Force ARM & Takeoff | Force DISARM |
|----------|----------------------|--------------|
| Connexion MAVLink | ✓ | ✓ |
| Attente du Heartbeat | ✓ | ✓ |
| Passage en mode GUIDED | ✓ | ✗ |
| ARM forcé | ✓ | ✗ |
| TAKEOFF | ✓ | ✗ |
| DISARM forcé | ✗ | ✓ |

---

# Objectif pédagogique

Ces deux scripts permettent d'étudier :

- l'établissement d'une connexion avec ArduPilot via MAVLink ;
- l'utilisation du message `COMMAND_LONG` pour transmettre des commandes critiques ;
- les mécanismes d'armement (`ARM`) et de désarmement (`DISARM`) du véhicule ;
- le déclenchement d'un décollage automatique (`TAKEOFF`) ;
- le rôle du mode **GUIDED** dans l'exécution de commandes de navigation ;
- les implications de sécurité liées à l'acceptation de commandes MAVLink non authentifiées dans un environnement de simulation.
