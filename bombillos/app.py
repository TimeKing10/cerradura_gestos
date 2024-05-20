import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
import time
import paho.mqtt.client as paho

st.title("Control por Voz de Cerradura Inteligente")

st.write("Presiona el botón y habla para controlar la cerradura inteligente.")

stt_button = Button(label="Iniciar reconocimiento de voz", width=200)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
    """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("Control_Cerradura")

def on_publish(client, userdata, result):
    print("El dato ha sido publicado \n")

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

client1.on_message = on_message
client1.on_publish = on_publish
client1.connect(broker, port)

if result:
    if "GET_TEXT" in result:
        voice_command = result.get("GET_TEXT")
        st.write("Comando de voz reconocido:", voice_command)
        client1.publish("cerradura_comandos", voice_command, qos=0, retain=False)
