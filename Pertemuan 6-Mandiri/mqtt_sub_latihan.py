import paho.mqtt.client as mqtt
from pymongo import MongoClient
from datetime import datetime, timezone
import json


# ── Konfigurasi MQTT ─────────────────────────────────────────────────────────
BROKER = "broker.hivemq.com"
PORT   = 1883
TOPIC  = "pabrik/produksi"


# ── Konfigurasi MongoDB ──────────────────────────────────────────────────────
MONGO_URI  = "mongodb://localhost:27017/"
DB_NAME    = "pabrik_iot"
COL_NAME   = "produksi_mqtt"


REJECT_THRESHOLD = 5.0   # persen


# ── Inisialisasi MongoDB ──────────────────────────────────────────────────────
mongo_client = MongoClient(MONGO_URI)
db           = mongo_client[DB_NAME]
collection   = db[COL_NAME]
print(f"[SUB] MongoDB terhubung → {DB_NAME}.{COL_NAME}")


# ── Callback MQTT ─────────────────────────────────────────────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[SUB] Terhubung ke broker {BROKER}:{PORT}")
        client.subscribe(TOPIC, qos=1)
        print(f"[SUB] Subscribe ke topik: {TOPIC}\n")
    else:
        print(f"[SUB] Gagal terhubung, kode: {rc}")




def on_message(client, userdata, msg):
    try:
        # 1. Parse payload JSON
        data = json.loads(msg.payload.decode("utf-8"))


        # 2. Tambahkan timestamp saat pesan diterima
        data["timestamp"] = datetime.now(timezone.utc)


        # 3. Hitung reject rate
        jumlah = data.get("jumlah", 0)
        reject = data.get("reject", 0)


        if jumlah > 0:
            reject_rate = (reject / jumlah) * 100
        else:
            reject_rate = 0.0


        data["reject_rate"] = round(reject_rate, 2)


        # 4. Cek threshold — tambahkan flag peringatan jika > 5 %
        if reject_rate > REJECT_THRESHOLD:
            data["peringatan"] = True
            print(
                f"[SUB] ⚠️  PERINGATAN! Reject rate tinggi: {reject_rate:.2f}% "
                f"| Batch={data.get('batch')} Mesin={data.get('mesin')}"
            )
        else:
            data["peringatan"] = False


        # 5. Simpan ke MongoDB
        result = collection.insert_one(data)
        print(
            f"[SUB] Disimpan → _id={result.inserted_id} | "
            f"batch={data.get('batch')} mesin={data.get('mesin')} "
            f"jumlah={jumlah} reject={reject} "
            f"rate={reject_rate:.2f}% peringatan={data['peringatan']}"
        )


    except json.JSONDecodeError as e:
        print(f"[SUB] Error parse JSON: {e}")
    except Exception as e:
        print(f"[SUB] Error tidak terduga: {e}")




def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"[SUB] Terputus (kode={rc}), coba reconnect otomatis…")


# ── Setup client MQTT ─────────────────────────────────────────────────────────
client = mqtt.Client(client_id="sub_produksi_001")
client.on_connect    = on_connect
client.on_message    = on_message
client.on_disconnect = on_disconnect


client.connect(BROKER, PORT, keepalive=60)


# ── Blocking loop ─────────────────────────────────────────────────────────────
print("[SUB] Menunggu pesan. Tekan Ctrl+C untuk berhenti.\n")
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\n[SUB] Dihentikan oleh pengguna.")
finally:
    client.disconnect()
    mongo_client.close()
    print("[SUB] Koneksi MQTT & MongoDB ditutup.")
