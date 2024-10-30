'''importing modules'''
from spotipy.oauth2 import SpotifyOAuth
from chat_interface import ChatInterface             ### this is a special module designed particlarly for ths project
from customtkinter import CTk
import speech_recognition as sr 
from dotenv import load_dotenv
import webbrowser
import wikipedia
import datetime
import requests
import spotipy
import pyttsx3
import cohere
import time
import os

# Loading the credentials
load_dotenv("API_CREDENTIALS.env")

# ASSIGNING VARIABLES 
api_key = os.getenv("api_key")
weather_api_key=os.getenv("wapi_key")
client_id=os.getenv('client_id')
client_secret =os.getenv('client_secret')

redirect_uri = 'http://localhost:8888/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope="user-library-read"))

chat_mode_active = False

# Defining voice agent
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

'''Defining functions'''

def speak(audio):
    engine.setProperty('rate', 175)
    engine.say(audio)
    engine.runAndWait()

def open_chat_mode():
    global chat_mode_active
    chat_mode_active = True
    start_time = time.time()

    # Initialize the CustomTkinter window instead of Tkinter
    root = CTk()  # CustomTkinter window
    chat_interface = ChatInterface(root)  # Create an instance of ChatInterface
    root.mainloop()

    end_time = time.time()
    chat_mode_active = False
    return end_time - start_time

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good   Morning")
    elif hour >= 12 and hour < 17:
        speak("Good   Afternoon")
    elif hour >= 17 and hour < 20:
        speak("Good    evening")
    else:
        speak("Good to see you again ")

    speak("I AM ,JARVIS ,HOW CAN I HELP U TODAY?")

def conversation(query):
    try:
        co = cohere.Client(api_key)
        if "who are you" in query.lower() or "what is your name" in query.lower():
            bot_identity = (
                "I am ,JARVIS   , your personal AI assistant created to help you with "
                "tasks, answer your questions, and make your life easier."
            )
            speak(bot_identity)
            print(bot_identity)
            return

        try:
            response = co.generate(
                model='command',
                prompt=query,
                return_likelihoods='GENERATION'
            )
            generated_text = response.generations[0].text
            print(generated_text)
            speak(generated_text)

        except cohere.errors as e:
            print("Error:", e)
            speak("Sorry, I'm having trouble understanding you. Please try again.")
    except Exception as e :
         print('INTERNET ERROR : TRY RECHECKING YOUR MODEM')
         speak('INTERNET ERROR : TRY RECHECKING YOUR MODEM')

def takecommand():
    # Converts voice to string
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            try:
                print("\nListening...")
                r.pause_threshold = 1
                audio = r.listen(source, phrase_time_limit=7)
                break
            except sr.WaitTimeoutError:
                print("An unexpected error occurred: please speak again")
                speak("Please speak again")
                break

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"user said:{query}\n")

    except Exception as e:
        print("Say that again please...")
        speak("Say that again please...")
        return takecommand()
    return query

'''setting up jarvis to run'''
if __name__ == '__main__':
    wishme()
    while True:
        query = takecommand().lower()
        
        #creating logical handles

        if 'wikipedia' in query:
            speak('searching the web...')
            print('This process might take some time:::')
            query = query.replace('wikipedia', "")
            result = wikipedia.summary(query, sentences=4)
            speak("According to wikipedia")
            print(result)
            speak(result)
        
        elif 'music' in query:
            speak("What music would you like to search for?")
            print("What music would you like to search for?")
            query = takecommand().lower()
            results = sp.search(q=query, type='track')
            speak("Here are the search results:")
            print("Here are the search results:")
            for result in results['tracks']['items']:
                print(f"{result['name']} by {result['artists'][0]['name']}")
            track_url = results['tracks']['items'][0]['external_urls']['spotify']
            webbrowser.open(track_url)
            break

        
        
        elif 'time ' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {strtime}")                                  
            print(f"the time is {strtime}")                                  
            speak("IS THERE ANYTHING ELSE I CAN HELP WITH")
        
        elif 'weather' in query:
            speak("Checking the weather of Raipur region...")
            print("Checking the weather of Raipur region...")
            city = 'Raipur'
            url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}"
            response = requests.get(url)
            data = response.json()
            if 'error' in data:
                speak("Sorry, I am unable to find the weather of Raipur region")
                print("Sorry, I am unable to find the weather of Raipur region")
            else:
                weather_result = data['current']['condition']['text']
                temperature = data['current']['temp_c']
                print(f"The weather in {city} is {weather_result} with a temperature of {temperature} degrees Celsius")
                speak(f"The weather in {city} is {weather_result} with a temperature of {temperature} degrees Celsius")
                speak("Is there anything else I can help you with?")

        elif 'chat  ' in query or 'chat mod' in query:
            speak("Chat mode is now activated, see you around")
            open_chat_mode()
            speak("Chat mode deactivated .")

        else:
            conversation(query)
            speak("Is there anything else I can help with?")
