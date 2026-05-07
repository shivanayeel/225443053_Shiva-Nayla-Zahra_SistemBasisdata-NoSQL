import json, os
import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

mongo_client = MongoClient(MONGO_URI)
db = mongo_client[DB_NAME]
collection = db["sensor"]

def on_connect(client, userdata, flags, rc):
    print("Terhubung ke MQTT broker")
    client.subscribe("pabrik/sensor/suhu")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        payload['timestamp'] = datetime.fromisoformat(payload['timestamp'])
        result = collection.insert_one(payload)
        print(f"[MONGO] Tersimpan {result.inserted_id} - {payload['mesin']} {payload['suhu']}°C")
    except Exception as e:
        print("Error:", e)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect("broker.emqx.io", 1883, 60)
mqtt_client.loop_forever()