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

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Buenos días!")
    elif hour >= 12 and hour < 18:
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
        query = r.recognize_google(audio, language='es-ES')
        print(f"Usuario: {query}\n")

        return query.lower()

    except Exception as e:
        print("Lo siento, no pude entender. Por favor, repita.")
        return ""

def calculator():
    speak("¿Qué operación desea realizar?")
    query = takeCommand().lower()
    try:
        result = eval(query)
        speak(f"El resultado es {result}")

    except:
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
    time = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"La hora es {time}")

def playMusic():
    speak("¿Qué canción desea reproducir?")
    query = takeCommand().lower()
    url = f"https://music.youtube.com/search?q={query}"
    webbrowser.open(url)

    time.sleep(5)  # Espera 5 segundos para asegurarte de que la página esté cargada

    # Ubicación del botón de reproducción en la pantalla (ajusta estos valores según tu pantalla)
    play_button_x = 870
    play_button_y = 362

    pyautogui.click(play_button_x, play_button_y)  # Simula el clic en el botón de reproducción

def googleSearch(query):
    query = query.replace("búscame en google", "")
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

def change_brightness():
    speak("¿Qué porcentaje de brillo desea?")
    brightness = takeCommand()
    if "bajar" in brightness:
        brightness = 50
    elif "subir" not in brightness:
        brightness = int(brightness.split()[0])
    if brightness > 100 or brightness < 0:
        speak("Lo siento, porcentaje inválido. Debe ser entre 0 y 100.")
        return
    subprocess.run(f"powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness({brightness}, 0)")

def turn_off_wifi():
    speak("¿Está seguro de que desea apagar el Wi-Fi?")
    query = takeCommand().lower()
    if "sí" in query:
        subprocess.run("netsh interface set interface Wi-Fi admin=disable")
        speak("Wi-Fi apagado.")
    else:
        speak("Cancelando.")

def turn_on_wifi():
    speak("¿Está seguro de que desea encender el Wi-Fi?")
    query = takeCommand().lower()
    if "sí" in query:
        subprocess.run("netsh interface set interface Wi-Fi admin=enable")
        speak("Wi-Fi encendido.")
    else:
        speak("Cancelando.")

def turn_off_bluetooth():
    subprocess.run(["cmd", "/c", "net stop bthserv"])
    time.sleep(2)
    subprocess.run(["cmd", "/c", "net start bthserv"])
    speak("Bluetooth apagado y encendido.")

def turn_on_bluetooth():
    subprocess.run(["cmd", "/c", "net stop bthserv"])
    time.sleep(2)
    subprocess.run(["cmd", "/c", "net start bthserv"])
    speak("Bluetooth encendido y apagado.")

def find_file():
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
    print("Presione 's' o 'f' para activar el asistente.")
    activate_assistant = False
    while not activate_assistant:
        activate_assistant = takeCommand().lower() in ["s", "f"]

    wishMe()

    while True:
        try:
            query = takeCommand().lower()

            if query == "f":
                print("Presione 's' o 'f' para activar el asistente.")
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
                change_brightness()
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
                turn_off_wifi()
            elif "encender wifi" in query:
                speak("Ejecutando encendido del Wi-Fi.")
                turn_on_wifi()
            elif "apagar bluetooth" in query:
                speak("Ejecutando apagado del Bluetooth.")
                turn_off_bluetooth()
            elif "encender bluetooth" in query:
                speak("Ejecutando encendido del Bluetooth.")
                turn_on_bluetooth()
            elif "buscar archivo" in query:
                speak("Ejecutando búsqueda de archivo.")
                find_file()
            else:
                speak("No pude entender su comando. Por favor, repita.")

            print("Presione 's' o 'f' para activar el asistente.")
            activate_assistant = False
            while not activate_assistant:
                activate_assistant = takeCommand().lower() in ["s", "f"]

        except KeyboardInterrupt:
            print("Presione 's' o 'f' para activar el asistente.")
            break
