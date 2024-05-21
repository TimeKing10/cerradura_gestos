import paho.mqtt.client as paho
import streamlit as st
import json

broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("StreamlitApp")

def on_publish(client, userdata, result):
    print("El dato ha sido publicado\n")

def send_message(topic, gesture):
    client1.connect(broker, port)
    client1.on_publish = on_publish
    message = json.dumps({"gesto": gesture})
    ret = client1.publish(topic, message)

st.title("Control de Luces")

if st.button('Encender'):
    client1.publish("IMIA","{'gesto': 'Prender'}",qos=0, retain=False)
    st.success("El LED ha sido encendido.")

if st.button('Apagar'):
    client1.publish("IMIA","{'gesto': 'Apagar'}",qos=0, retain=False)
    st.success("El LED ha sido apagado.")
