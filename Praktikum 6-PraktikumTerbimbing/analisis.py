import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db["sensor"]

cursor = collection.find({}, {"_id": 0})
df = pd.DataFrame(list(cursor))

df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)

resampled = df.resample('10min').mean(numeric_only=True)
print(resampled.head())

plt.figure(figsize=(10,5))
df['suhu'].plot(title='Suhu dari Waktu ke Waktu')
plt.ylabel('Suhu (°C)')
plt.grid(True)
plt.savefig('suhu_plot.png')
plt.show()

client.close()