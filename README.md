# Projet de Simulation de Véhicules avec MQTT

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![MQTT Protocol](https://img.shields.io/badge/protocol-MQTT-green.svg)

## Description
Ce projet simule le déplacement de véhicules en utilisant des files MQTT pour la communication. Chaque véhicule publie sa position sur une file MQTT et peut recevoir des requêtes pour sa position actuelle et son horloge. Un upper-tester est inclus pour tester le bon fonctionnement des boitiers de communication des véhicules.

## Installation

1. **Cloner le dépôt Git** :
    ```bash
    git clone https://github.com/votre-nom-utilisateur/nom-du-repo.git
    cd nom-du-repo
    ```

2. **Installer les dépendances** :
    Assurez-vous d'avoir Python et `pip` installés, puis installez les dépendances :
    ```bash
    pip install paho-mqtt
    ```

3. **Configurer les fichiers JSON** :
    - `init3.json` : Contient les paramètres initiaux du véhicule (ID, position, direction, vitesse).
    - `params2.json` : Contient les étapes de déplacement du véhicule (vitesse, direction).

## Utilisation

### Lancer le script du véhicule

Ce script simule le déplacement d'un véhicule et publie sa position sur la file MQTT.
```bash
python vehicle_script.py
