import paho.mqtt.client as mqtt
import json
import random
import time


# ── Konfigurasi broker ──────────────────────────────────────────────────────
BROKER   = "broker.hivemq.com"
PORT     = 1883
TOPIC    = "pabrik/produksi"
INTERVAL = 3   # detik antar pengiriman


# ── Data referensi ──────────────────────────────────────────────────────────
DAFTAR_BATCH  = ["B001", "B002", "B003", "B004", "B005"]
DAFTAR_MESIN  = ["M-Alpha", "M-Beta", "M-Gamma", "M-Delta"]


# ── Callback ────────────────────────────────────────────────────────────────
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[PUB] Terhubung ke broker {BROKER}:{PORT}")
    else:
        print(f"[PUB] Gagal terhubung, kode: {rc}")


def on_publish(client, userdata, mid):
    print(f"[PUB] Pesan terkirim (mid={mid})")


# ── Setup client ─────────────────────────────────────────────────────────────
client = mqtt.Client(client_id="pub_produksi_001")
client.on_connect = on_connect
client.on_publish  = on_publish


client.connect(BROKER, PORT, keepalive=60)
client.loop_start()


# ── Loop pengiriman ──────────────────────────────────────────────────────────
print("[PUB] Mulai mengirim data produksi. Tekan Ctrl+C untuk berhenti.\n")
try:
    while True:
        payload = {
            "batch"  : random.choice(DAFTAR_BATCH),
            "mesin"  : random.choice(DAFTAR_MESIN),
            "jumlah" : random.randint(100, 500),
            "reject" : random.randint(0, 50),
        }
        msg = json.dumps(payload)
        result = client.publish(TOPIC, msg, qos=1)
        print(f"[PUB] Kirim → {msg}")
        time.sleep(INTERVAL)


except KeyboardInterrupt:
    print("\n[PUB] Dihentikan oleh pengguna.")


finally:
    client.loop_stop()
    client.disconnect()
    print("[PUB] Koneksi ditutup.")
