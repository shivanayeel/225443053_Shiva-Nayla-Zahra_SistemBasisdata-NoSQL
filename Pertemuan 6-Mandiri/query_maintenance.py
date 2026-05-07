import pandas as pd
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["piton"]
collection = db["maintenance"]

print("=== 1. Mencari Dokumen dengan Biaya > 1.000.000 ===")
query_biaya = {"biaya": {"$gt": 1000000}}
data_biaya = list(collection.find(query_biaya))

df_biaya = pd.DataFrame(data_biaya)
if not df_biaya.empty:
    print(df_biaya.drop(columns=["_id"]).to_string(index=False))
else:
    print("Tidak ada data yang ditemukan.")


print("\n=== 2. Melakukan Update Data ===")
query_update = {"mesin": "CNC-01", "biaya": 1200000}
update_values = {"$set": {"teknisi": "Dewi"}}

update_result = collection.update_many(query_update, update_values)
print(f"Berhasil memperbarui {update_result.modified_count} dokumen (Teknisi diubah menjadi 'Dewi').")


print("\n=== 3. Menghitung Total Biaya per Bulan ===")
pipeline = [
    {
        "$group": {
            "_id": {"$dateToString": {"format": "%Y-%m", "date": "$tanggal"}},
            "total_biaya": {"$sum": "$biaya"}
        }
    },
    {
        "$sort": {"_id": 1}
    }
]

agg_result = list(collection.aggregate(pipeline))
df_agg = pd.DataFrame(agg_result)

if not df_agg.empty:
    df_agg.rename(columns={"_id": "Bulan"}, inplace=True)
    print(df_agg.to_string(index=False))
else:
    print("Tidak ada data agregasi.")