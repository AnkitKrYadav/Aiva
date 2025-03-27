#modules needed are imported
import os ,playsound, pyttsx3,subprocess as sp,speech_recognition as sr,sys #pip install playsound==1.2.2 SpeechRecognition pyttsx3 pyaudio pocketsphinx
from google import genai #pip install -U google-genai
from google.genai import types

# Global variables
api_key= os.getenv("GEMINI_API_KEY")
api_key2= os.getenv("GEMINI_API_KEY2")
client = genai.Client(api_key=api_key)
name=''

#pyttsx initialisation
engine= pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

#Functions to use repetitively

def askai(q):#Process the user querry and provide output
    global client 
    try:   
        response = client.models.generate_content(
        model="gemini-2.0-flash",    
        config=types.GenerateContentConfig(system_instruction='You are Aiva a reliable ai assistant who provides consize and to the point answers as much as possible,and be soothing/friendly',
        temperature=1),
        contents=q
        )
        return response.text.replace('*','')
    except Exception as e:
        print('1: '+str(e))
        try:            
            client = genai.Client(api_key=api_key2)
            api_key,api_key2=api_key2,api_key

            response = client.models.generate_content(
            model="gemini-2.0-flash",    
            config=types.GenerateContentConfig(system_instruction='You are Aiva a reliable ai assistant who provides consize and to the point answers as much as possible,and be soothing/friendly.',
            temperature=1),
            contents=q
            )
            return response.text.replace('*','')
        except Exception as e:
            print('2: '+str(e))

def speak(txt):#text to speech
    engine.say(txt)
    print('AI   : '+txt+'\n')
    engine.runAndWait()    

def tc():  #take_voice_command(speech to text)  
    r,order=sr.Recognizer(),''
    #r.energy_threshold=50
    #r.pause_threshold=0.5

    with sr.Microphone() as source:        
        #r.adjust_for_ambient_noise(source,duration=0.5)
        print('Listening.........')        
        audio=r.listen(source)        
        try:
            order=r.recognize_google(audio,language='en-IN')
            print('USER : '+ order)

        except Exception :
           print("Exception: " + str(Exception)+'|| Unable to recognise your voice\n')         

    return order

def intro():#Greet user
    speak('Hello sir, what\'s your name ?')
    global name
    name=tc().title()
    speak(f'Nice to meet you {name}, i am aiva how can i help you today sir ?')

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
            pass

    elif ('exit'==order):
        speak(f"Have a great day ahead, good bye {name}.")
        sys.exit()

    elif (order==''):
     pass

    else:       
        speak(askai(order))
