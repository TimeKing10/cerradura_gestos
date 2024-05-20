import os
import json
import speech_recognition as sr
from gtts import gTTS
from googletrans import Translator
import paho.mqtt.client as paho
import time

broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("APP_CERR")
client1.connect(broker, port)

translator = Translator()

def on_publish(client, userdata, result):
    print("El dato ha sido publicado \n")
    pass

def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Habla ahora...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="es-ES") # Cambia el idioma según sea necesario
        print("Texto reconocido:", text)
        return text
    except sr.UnknownValueError:
        print("No se pudo entender el audio.")
        return None
    except sr.RequestError as e:
        print("Error en la solicitud de reconocimiento de voz: ", str(e))
        return None

def text_to_voice(text, language='es'):
    tts = gTTS(text=text, lang=language, slow=False)
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")

def translate_text(text, dest_language='en'):
    translation = translator.translate(text, dest=dest_language)
    return translation.text

def control_lights(command):
    if command == "encender luces":
        client1.publish("IMIA", "{'gesto': 'prender luces'}", qos=0, retain=False)
    elif command == "apagar luces":
        client1.publish("IMIA", "{'gesto': 'apagar luces'}", qos=0, retain=False)

client1.on_publish = on_publish

while True:
    voice_command = voice_to_text()
    if voice_command:
        translated_command = translate_text(voice_command, dest_language='es')
        print("Comando traducido:", translated_command)
        control_lights(translated_command)
        text_to_voice("Comando recibido: " + translated_command)
    time.sleep(2)  # Espera antes de escuchar el siguiente comando de voz
