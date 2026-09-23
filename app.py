import pymysql
import paho.mqtt.client as mqtt

MQTT_HOST = "119.18.62.146"
MQTT_PORT = 1883

DB_HOST = "119.18.62.146"
DB_PORT = 3306
DB_USER = "dbadmin"
DB_PASSWORD = "StrongAdminPass123!"
DB_NAME = "dsp_train"

def on_connect(client, userdata, flags, rc, properties=None):
    print("MQTT Connected:", rc)

    client.subscribe("train/signall1")
    client.subscribe("train/signalr1")

def on_message(client, userdata, msg):

    signal = msg.payload.decode().strip()

    print(f"{msg.topic} -> {signal}")

    try:
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO train_messages
            (signal_value, topic)
            VALUES (%s,%s)
            """,
            (
                signal,
                msg.topic
            )
        )

        conn.commit()

        cur.close()
        conn.close()

        print("Saved to Database")

    except Exception as e:
        print("DB Error:", e)

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(
    MQTT_HOST,
    MQTT_PORT,
    60
)

client.loop_forever()