from pymongo import MongoClient
from datetime import datetime, timedelta
import random

NIM = "225443053"
client = MongoClient('mongodb://localhost:27017')

db = client[f'latihan5_{225443053}']

db.data_sensor.drop()

sensor_list = [f"S{i:03d}" for i in range(1, 21)]  # S001 sampai S020
kategori_list = ["suhu", "tekanan", "kelembaban", "getaran", "arus"]

docs = []
start_date = datetime(2026, 4, 1, 0, 0)

for i in range(5000):
    kategori = random.choice(kategori_list)
    
    if kategori == "suhu":
        nilai = round(random.uniform(25.0, 95.0), 2)
    elif kategori == "kelembaban":
        nilai = round(random.uniform(40.0, 99.0), 2)
    else:
        nilai = round(random.uniform(10.0, 150.0), 2)

    timestamp = start_date + timedelta(minutes=random.randint(0, 60*24*30))
    
    doc = {
        "sensor_id": random.choice(sensor_list),
        "nilai": nilai,
        "timestamp": timestamp,
        "category": kategori
    }
    
    docs.append(doc)
    
    if len(docs) >= 500:
        db.data_sensor.insert_many(docs)
        docs.clear()

if docs:
    db.data_sensor.insert_many(docs)

print(f"Database: latihan5_{NIM}")
print("Data sensor selesai dimasukkan. Total:", db.data_sensor.count_documents({}), "dokumen.")