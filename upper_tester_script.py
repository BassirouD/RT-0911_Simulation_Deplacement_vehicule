import json
import time
import paho.mqtt.client as mqtt

# Initialiser le client MQTT
client = mqtt.Client()

# Connexion au broker MQTT
client.connect("localhost", 1883)
client.subscribe("response")

# Démarrer la boucle MQTT pour traiter les messages entrants
client.loop_start()

# Stocker les réponses des véhicules
responses = []


# Fonction callback pour la réception des messages MQTT
def on_message(client, userdata, message):
    data = json.loads(message.payload.decode())

    if message.topic == "response":
        print(f"Réponse reçue : {data}")
        responses.append(data)


# Assigner la fonction callback à l'événement de réception de message MQTT
client.on_message = on_message


# Fonction pour envoyer des requêtes aux véhicules
def send_request(vehicle_id):
    request = {
        'request': 'get_status',
        'id': vehicle_id
    }
    client.publish("request", json.dumps(request))


# ID du véhicule à tester
vehicle_id = 3  # Changez ceci pour tester d'autres véhicules

# Envoyer une requête au véhicule
send_request(vehicle_id)

# Attendre un certain temps pour recevoir la réponse
time.sleep(5)

# Arrêter la boucle MQTT à la fin du test
client.loop_stop()
