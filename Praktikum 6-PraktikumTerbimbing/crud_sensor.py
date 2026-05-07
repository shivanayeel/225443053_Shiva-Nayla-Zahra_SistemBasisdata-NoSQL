import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("crud_sensor.log"),
        logging.StreamHandler()
    ]
)

from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timedelta
import random, os

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db["sensor"]

data = []
for i in range(10):
    doc = {
        "mesin": f"CNC-{random.randint(1,3):02d}",
        "suhu": round(random.uniform(60, 100), 2),
        "getaran": round(random.uniform(0.1, 0.5), 2),
        "timestamp": datetime.utcnow() - timedelta(minutes=i*5),
        "status": "normal"
    }
    data.append(doc)
try:
    result = collection.insert_many(data)
    logging.info(f"Insert berhasil, {len(result.inserted_ids)} dokumen")
except Exception as e:
    logging.error(f"Insert gagal: {e}")




