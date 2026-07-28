# Force ARM & Takeoff via MAVLink

## Description

Ce script se connecte à **ArduPilot** via **MAVLink**, place le drone en mode **GUIDED**, effectue un **ARM forcé**, puis envoie une commande de **décollage automatique** à une altitude de **30 mètres**.

Il permet d'illustrer comment un client MAVLink peut contrôler un véhicule à distance à l'aide de commandes standard.

---

# Fonctionnement

Le script réalise les opérations suivantes :

1. Connexion au véhicule via MAVLink.
2. Attente du message Heartbeat.
3. Passage en mode **GUIDED**.
4. Envoi d'un ARM forcé.
5. Attente de quelques secondes.
6. Envoi d'une commande de décollage automatique.

---

# Structure du code

## Connexion

```python
master = mavutil.mavlink_connection("udp:127.0.0.1:14550")
```

Le script ouvre une connexion UDP vers ArduPilot.

---

## Heartbeat

```python
master.wait_heartbeat()
```

Le programme attend que le pilote automatique confirme sa présence.

---

## Changement de mode

```python
master.set_mode("GUIDED")
```

Le drone est placé en mode **GUIDED**, ce qui autorise l'exécution de commandes de navigation envoyées par MAVLink.

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

## Décollage

Le script envoie ensuite une commande :

```
MAV_CMD_NAV_TAKEOFF
```

Le dernier paramètre fixe l'altitude cible :

```
30 mètres
```

Le pilote automatique démarre alors une procédure de décollage jusqu'à atteindre cette altitude.

---

# Exemple d'exécution

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

# Messages MAVLink utilisés

| Message | Rôle |
|---------|------|
| `HEARTBEAT` | Vérifie la présence du véhicule |
| `COMMAND_LONG` | Transporte les commandes envoyées au pilote automatique |
| `MAV_CMD_COMPONENT_ARM_DISARM` | Arme ou désarme le drone |
| `MAV_CMD_NAV_TAKEOFF` | Lance une procédure de décollage automatique |

---

# Objectif pédagogique

Ce script permet de comprendre :

- l'établissement d'une connexion MAVLink ;
- le changement de mode de vol ;
- l'envoi de commandes critiques (`ARM`, `TAKEOFF`) ;
- le fonctionnement du message `COMMAND_LONG` dans ArduPilot ;
- les conséquences potentielles d'une absence de contrôle d'accès aux commandes MAVLink dans un environnement de simulation.

# Force Disarm via MAVLink

## Description

Ce script établit une connexion avec un véhicule **ArduPilot** via le protocole **MAVLink**, puis envoie une commande de **désarmement forcé (Force DISARM)**.

Il illustre comment un client MAVLink peut transmettre une commande critique au pilote automatique à l'aide du message `COMMAND_LONG`.


---

# Fonctionnement

Le script effectue les étapes suivantes :

1. Connexion au véhicule via MAVLink.
2. Attente du message **Heartbeat**.
3. Identification du système cible.
4. Envoi d'une commande `MAV_CMD_COMPONENT_ARM_DISARM`.
5. Désarmement forcé du drone.

---

# Explication du code

## Connexion MAVLink

```python
master = mavutil.mavlink_connection("udp:127.0.0.1:14550")
```

Établit une connexion UDP avec ArduPilot sur le port **14550**.

---

## Attente du Heartbeat

```python
master.wait_heartbeat()
```

Le script attend qu'ArduPilot envoie un message **Heartbeat**, indiquant que la communication est établie.

---

## Commande de désarmement

```python
master.mav.command_long_send(...)
```

Cette fonction envoie un message MAVLink de type :

```
COMMAND_LONG
```

contenant la commande :

```
MAV_CMD_COMPONENT_ARM_DISARM
```

avec les paramètres :

- **param1 = 0** → désarmement (DISARM)
- **param2 = 21196** → code autorisant le désarmement forcé

Le code **21196** permet d'ignorer certaines vérifications de sécurité normalement effectuées par le pilote automatique.

---

# Exemple d'exécution

```bash
python3 force_disarm.py
```

Sortie :

```
[+] Connecté — sys=1
[+] DISARM forcé en vol
```

---

# Objectif pédagogique

Ce script montre comment :

- établir une connexion MAVLink ;
- envoyer une commande `COMMAND_LONG` ;
- utiliser la commande `MAV_CMD_COMPONENT_ARM_DISARM` ;
- comprendre les risques liés aux commandes critiques si elles ne sont pas protégées.
