import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import subprocess
import ctypes
import time
import pyautogui
import pygatt

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Buenos días!")
    elif 12 <= hour < 18:
        speak("Buenas tardes!")
    else:
        speak("Buenas noches!")
    speak("Soy su asistente personal. ¿En qué puedo ayudarle?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Reconociendo...")
        query = r.recognize_google(audio, language ='es-ES')
        print(f"Usuario: {query}\n")
        return query.lower()

    except sr.UnknownValueError:
        print("Lo siento, no pude entender. Por favor, repita.")
        return ""
    except sr.RequestError as e:
        print("Error de conexión. Por favor, inténtelo de nuevo más tarde.")
        return ""

def calculator():
    speak("¿Qué operación desea realizar?")
    query = takeCommand().lower()
    try:
        result = eval(query)
        speak(f"El resultado es {result}")

    except Exception as e:
        speak("Lo siento, no pude realizar la operación.")

def openApp(app):
    if "google" in app:
        webbrowser.open("https://www.google.com")
    elif "youtube" in app:
        webbrowser.open("https://www.youtube.com")
    elif "spotify" in app:
        os.startfile("C:\\Users\\usuario\\AppData\\Roaming\\Spotify\\Spotify.exe")
    else:
        speak("Lo siento, no pude entender. Por favor, repita.")

def tellTime():
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"La hora es {time_now}")

def playMusic():
    speak("¿Qué canción desea reproducir?")
    query = takeCommand().lower()
    url = f"https://music.youtube.com/search?q={query}"
    webbrowser.open(url)
    time.sleep(8)  # Espera 8 segundos para asegurarte de que la página esté cargada
    pyautogui.click(963, 399)  # Simula el clic en el botón de reproducción

def googleSearch(query):
    query = query.replace("", "")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def shutdownComputer():
    speak("¿Está seguro de que desea apagar el ordenador?")
    query = takeCommand().lower()
    if "sí" in query:
        os.system("shutdown /s /t 1")
    else:
        speak("Cancelando apagado.")

def lockScreen():
    speak("Bloqueando pantalla.")
    subprocess.run("rundll32.exe user32.dll,LockWorkStation")

def changeBrightness():
    speak("¿Qué porcentaje de brillo desea?")
    brightness = takeCommand()
    if "bajar" in brightness:
        brightness = 50
    elif "subir" not in brightness:
        brightness = int(brightness.split()[0])
    if not 0 <= brightness <= 100:
        speak("Lo siento, porcentaje inválido. Debe ser entre 0 y 100.")
        return
    subprocess.run(f"powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness({brightness}, 0)")

def turnOffWifi():
    speak("¿Está seguro de que desea apagar el Wi-Fi?")
    query = takeCommand().lower()
    if "sí" in query:
        subprocess.run("netsh interface set interface Wi-Fi admin=disable")
        speak("Wi-Fi apagado.")
    else:
        speak("Cancelando.")

def turnOnWifi():
    speak("¿Está seguro de que desea encender el Wi-Fi?")
    query = takeCommand().lower()
    if "sí" in query:
        subprocess.run("netsh interface set interface Wi-Fi admin=enable")
        speak("Wi-Fi encendido.")
    else:
        speak("Cancelando.")

def turnOffBluetooth():
    adapter = pygatt.GATTToolBackend()
    try:
        adapter.start()
        devices = adapter.scan(run_as_root=True)
        for device in devices:
            adapter.connect(device)
            print(f"Apagando Bluetooth para el dispositivo {device['address']}")
            adapter.disconnect(device)
        speak("Bluetooth apagado.")
    except Exception as e:
        print(f"Error al apagar Bluetooth: {str(e)}")
        speak("No se pudo apagar Bluetooth.")
    finally:
        try:
            adapter.stop()
        except Exception as e:
            print(f"Error al detener el adaptador Bluetooth: {str(e)}")

def listenForCommands():
    while True:
        try:
            query = takeCommand().lower()

            if query == "coco":
                print("Diga coco para activar el asistente.")
                break

            # Resto de las funciones aquí

        except KeyboardInterrupt:
            print("Diga coco para activar el asistente.")
            break

def findFile():
    speak("¿Qué archivo desea buscar?")
    query = takeCommand().lower()
    for root, dirs, files in os.walk("C:\\"):
        for file in files:
            if query in file.lower():
                speak(f"Encontré el archivo {file} en {root}. ¿Desea abrirlo?")
                query = takeCommand().lower()
                if "sí" in query:
                    os.startfile(os.path.join(root, file))
                    return
                else:
                    speak("Cancelando.")
                    return
    speak("Lo siento, no pude encontrar el archivo.")

if __name__ == "__main__":
    print("diga coco para activar el asistente.")
    activateAssistant = False
    while not activateAssistant:
        activateAssistant = takeCommand().lower() in ["COCO", "coco"]

    wishMe()

    while True:
        try:
            query = takeCommand().lower()

            if query == "coco":
                print("diga coco para activar el asistente.")
                break

            if "calculadora" in query or "calcular" in query:
                speak("Ejecutando calculadora.")
                calculator()
            elif "abrir" in query:
                speak("Ejecutando apertura de aplicación.")
                app = query.replace("abrir ", "")
                openApp(app)
            elif "hora" in query:
                speak("Ejecutando consulta de hora.")
                tellTime()
            elif "reproducir música" in query:
                speak("Ejecutando reproducción de música.")
                playMusic()
            elif "cambiar brillo" in query:
                speak("Ejecutando cambio de brillo.")
                changeBrightness()
            elif "buscar en google" in query:
                speak("Ejecutando búsqueda en Google.")
                googleSearch(query)
            elif "apagar el ordenador" in query:
                speak("Ejecutando apagado del ordenador.")
                shutdownComputer()
                break
            elif "bloquear pantalla" in query:
                speak("Ejecutando bloqueo de pantalla.")
                lockScreen()
                break
            elif "apagar wifi" in query:
                speak("Ejecutando apagado del Wi-Fi.")
                turnOffWifi()
            elif "encender wifi" in query:
                speak("Ejecutando encendido del Wi-Fi.")
                turnOnWifi()
            elif "apagar bluetooth" in query:
                speak("Ejecutando apagado del Bluetooth.")
                turnOffBluetooth()
            elif "encender bluetooth" in query:
                speak("Ejecutando encendido del Bluetooth.")
                turnOnBluetooth()
            elif "buscar archivo" in query:
                speak("Ejecutando búsqueda de archivo.")
                findFile()
            else:
                speak("No pude entender su comando. Por favor, repita.")

            print("Presione 's' o 'f' para activar el asistente.")
            activateAssistant = False
            while not activateAssistant:
                activateAssistant = takeCommand().lower() in ["s", "f"]

        except KeyboardInterrupt:
            print("diga coco para activar el asistente.")
            break
