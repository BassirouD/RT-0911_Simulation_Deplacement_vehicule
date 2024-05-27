import json
import time
import paho.mqtt.client as mqtt
from datetime import datetime

# Initialiser le client MQTT
client = mqtt.Client()

# Connexion au broker MQTT
client.connect("localhost", 1883)
client.subscribe("vehicle")
client.subscribe("request")

# Démarrer la boucle MQTT pour traiter les messages entrants
client.loop_start()


# Fonction callback pour la réception des messages MQTT
def on_message(client, userdata, message):
    global next_destination
    # Convertir le message JSON en objet Python
    data = json.loads(message.payload.decode())
    if message.topic == "vehicle":
        print(data['position'])
        # Vérifier si la position du message correspond à la prochaine destination
        if data['position'] == next_destination:
            print(f"Prochaine destination ({next_destination}) est occupée par le véhicule {data['id']}. En attente...")
        else:
            print(f"Aucun véhicule occupant la prochaine destination ({next_destination}). Déplacement autorisé.")
    elif message.topic == "request":
        # Répondre à une requête de position et d'horloge
        if data['request'] == 'get_status' and data['id'] == vehicle['id']:
            response = {
                'id': vehicle['id'],
                'position': vehicle['position'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            client.publish("response", json.dumps(response))
# Assigner la fonction callback à l'événement de réception de message MQTT
client.on_message = on_message


# Fonction pour lire les paramètres initiaux du véhicule à partir du fichier
def read_init_params(file_path):
    with open(file_path) as f:
        init_params = json.load(f)
    return init_params['id'], init_params['x'], init_params['y'], init_params['dir'], init_params['speed']


# Fonction pour lire les étapes de déplacement à partir du fichier
def read_steps(file_path):
    with open(file_path) as f:
        steps = json.load(f)
    return steps['steps']


# Fonction pour avancer le véhicule
def move_vehicle(vehicle, speed, direction):
    x, y = vehicle['position']

    # Calculer la nouvelle position en fonction de la vitesse et de la direction
    if direction == 1:
        x += speed
    elif direction == -1:
        x -= speed
    elif direction == 2:
        y += speed
    elif direction == -2:
        y -= speed

    # Mettre à jour la position du véhicule
    vehicle['position'] = (x, y)

    # Publier la nouvelle position sur le topic "vehicle"
    client.publish("vehicle", json.dumps({'id': vehicle['id'], 'position': (x, y)}))


# Lire les paramètres initiaux du véhicule à partir du fichier
vehicle_id, x, y, direction, speed = read_init_params('init3.json')

# Initialiser le véhicule avec les paramètres initiaux
vehicle = {
    'id': vehicle_id,
    'position': (x, y),
    'direction': direction,
    'speed': speed
}

# Lire les étapes de déplacement à partir du fichier
steps = read_steps('params2.json')

# Boucle de simulation
for step in steps:
    # Extraire la vitesse et la direction de l'étape
    speed, direction = step['speed'], step['direction']

    # Avancer le véhicule avec les paramètres de cette étape
    move_vehicle(vehicle, speed, direction)

    # Afficher la position du véhicule
    print(f"Véhicule {vehicle['id']} - Position : {vehicle['position']}")

    # Déterminer la prochaine destination
    next_destination = (vehicle['position'][0] + (speed if direction in [1, -1] else 0),
                        vehicle['position'][1] + (speed if direction in [2, -2] else 0))

    # Attendre un certain temps avant de vérifier à nouveau la file vehicle
    time.sleep(5)

# Arrêter la boucle MQTT à la fin de la simulation
client.loop_stop()
