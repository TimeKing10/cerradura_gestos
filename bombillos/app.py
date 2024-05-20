import streamlit as st
import paho.mqtt.client as mqtt

# Configuración del cliente MQTT
mqtt_broker = "broker.mqttdashboard.com"
mqtt_port = 1883
mqtt_topic = "bombillos/control"
client = mqtt.Client("Bombillos_Client")
client.connect(mqtt_broker, mqtt_port)

st.title("Control de los Bombillos con Palmadas")

# Función para publicar mensajes MQTT para encender o apagar los bombillos
def publish_light_command(command):
    client.publish(mqtt_topic, command)

# Control de los bombillos con palmadas
if st.button("Encender Bombillos con Palmadas"):
    st.write("Escuchando palmadas...")
    # Aquí puedes implementar la lógica para detectar palmadas y publicar el comando MQTT correspondiente
    # Ejemplo:
    # if detect_claps():
    #     publish_light_command("encender")

if st.button("Apagar Bombillos"):
    publish_light_command("apagar")
