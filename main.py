# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import os
import speech_recognition as sr
from gtts import gTTS
from openai import OpenAI
from tempfile import NamedTemporaryFile

# Fonction pour convertir le texte en parole avec gTTS et le lire
def speak(text):
    with NamedTemporaryFile(delete=True, suffix='.mp3') as fp:
        tts = gTTS(text=text, lang='en')  # Création de l'objet gTTS
        tts.save(fp.name)  # Sauvegarde du texte en parole dans un fichier temporaire
        os.system(f"start {fp.name}")  # Lecture du fichier sur Windows
        # Sur Linux, utilisez os.system(f"mpg321 {fp.name}")
        # Sur MacOS, utilisez os.system(f"afplay {fp.name}")

# Initialisation du reconnaisseur de parole
listener = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        voice = listener.listen(source)
        command = ""
        try:
            command = listener.recognize_google(voice)
            print(f"You said: {command}")
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
        except sr.RequestError:
            print("Sorry, my speech service is down.")
        return command

# Traitement des commandes avec OpenAI
def process_command(command):
    response = openai.Completion.create(
        engine="text-davinci-003",  # Vous pouvez choisir l'engine qui convient à votre besoin
        prompt=command,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Chargement de la clef API d'une variable d'environnement pour des raisons de sécurité
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("La clé API OpenAI n'est pas définie dans les variables d'environnement.")
openai = OpenAI(api_key=openai_api_key)

# Boucle principale de l'assistant
def main():
    while True:
        command = listen()
        if 'exit' in command:
            speak("Goodbye!")
            break
        response = process_command(command)
        speak(response)

if __name__ == "__main__":
    main()
