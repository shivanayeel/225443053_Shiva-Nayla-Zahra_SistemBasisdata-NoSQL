import pandas as pd
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client["piton"]
collection = db["test2"]

data = pd.read_csv("maintenance.csv")

data["tanggal"] = pd.to_datetime(data["tanggal"])

records = data.to_dict(orient="records")

result = collection.insert_many(records)

print(f"Berhasil insert {len(result.inserted_ids)} data")