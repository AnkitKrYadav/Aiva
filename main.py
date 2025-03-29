'''Modules needed for stt,q processing,interacting with system to do work,tts are imported'''
#Todo : Add chat system to remember prev talks,better speech recognition.

import os, sys, subprocess as sp
import pyttsx3, speech_recognition as sr     #pip install SpeechRecognition pyttsx3 pyaudio, pocketsphinx playsound==1.2.2
from google import genai                     #pip install -U google-genai
from google.genai import types
from google.genai.types import Tool,GoogleSearch

# Global variables
name=''
prompt=(f'You are Aiva,a reliable AI assistant known for providing concise,to-the-point answers in respect to user name {name} '
       'from india, in max 120 words.Your tone is friendly, and always approachable.')
api_key= os.getenv("GEMINI_API_KEY")
api_key2= os.getenv("GEMINI_API_KEY2")
client = genai.Client(api_key=api_key)
google_search_tool = Tool(
    google_search = GoogleSearch()
)

#pyttsx initialization
engine= pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


#Functions:
def askai(q):
    '''Provide output of query through G-api'''
    global client,api_key,api_key2,name

    try:
        response = client.models.generate_content(
        model="gemini-2.0-flash",    
        config=types.GenerateContentConfig(
        tools=[google_search_tool],
        #response_modalities=["TEXT"],
            system_instruction=prompt,
            temperature=0.9),
        contents=q
        )
        return response.text.replace('*','')

    except Exception as e:
        print('1: '+str(e))#edit 1
        try:
            client = genai.Client(api_key=api_key2)
            api_key,api_key2=api_key2,api_key

            response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=prompt,
                temperature=0.9),
            contents=q
            )
            return response.text.replace('*','')
        except Exception as f:
            print('2: '+str(f))

def speak(txt):
    '''convert text to speech'''
    engine.say(txt)
    print('AI   : '+txt+'\n')
    engine.runAndWait()    

def tc():  
    '''Take_voice_command and return command in text format'''    
    #r.energy_threshold=50
    #r.pause_threshold=0.5
    r,order=sr.Recognizer(),''

    with sr.Microphone() as source:        
        #r.adjust_for_ambient_noise(source,duration=0.5)
        print('Listening.........')        
        audio=r.listen(source)        
        try:
            order=r.recognize_google(audio,language='en-IN')
            print('USER : '+ order)

        except Exception :
            print("Exception: " + str(Exception)+'|| Unable to recognize your voice\n')         

    return order

def intro():
    '''Greet user with name'''
    speak('Hello sir, what\'s your name ?')
    global name
    name=tc().title()
    speak(f'Great to meet you {name}, i am aiva, how can i help you today sir ?')

# Program starts here
print('\n------------------------------------------------------------------------------------------------------------------')
intro()

while True:
    order=tc().lower()

    if ('open browser' in order) or 'open firefox' in order:
        fpath="C:\\Program Files\\Mozilla Firefox\\firefox.exe"
        os.startfile(fpath)
    elif ('open vs code' in order):
        vpath="C:\\Users\\abhim\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(vpath)
    elif ('open notepad' in order):
        npath='C:\\Windows\\System32\\notepad.exe'
        os.startfile(npath)
    elif ('cmd' in order):
        cfile='C:\\Windows\\System32\\cmd.exe'
        os.startfile(cfile)
    elif ('shutdown computer' in order):
        speak('please confirm Y/N')
        order=tc()
        if 'yes' in order or 'ya' in order:
            sp.call(['shutdown','/s'])
        else:
            pass

    elif ('restart computer' in order):
        speak('please confirm Yes/No')
        order=tc()
        if 'yes' in order or 'ya' in order:
            sp.call(['shutdown','/r'])
        else:
            pass

    elif('sleep computer' in order):
        speak('please confirm Yes/No')
        order=tc().lower()
        if 'yes' in order or 'ya' in order:
            sp.call(['shutdown','/h'])
        else:
            print(order)

    elif ('exit'==order):
        speak(f"Have a great day ahead, good bye {name}.")
        sys.exit()

    elif (order==''):
        pass

    else:       
        speak(askai(order))
