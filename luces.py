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
    send_message("gestos", "ON")
    st.success("El LED ha sido encendido.")

if st.button('Apagar'):
    send_message("gestos", "OFF")
    st.success("El LED ha sido apagado.")
