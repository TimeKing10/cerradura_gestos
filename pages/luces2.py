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
    client1.publish(topic, message)

st.title("Control de Luces")

if st.button('Encender'):
    client1.connect(broker, port)
    send_message("IMIA", "Prender")
    st.success("Se hizo la luz.")

if st.button('Apagar'):
    client1.connect(broker, port)
    send_message("IMIA", "Apagar")
    st.success("No veo nah.")
