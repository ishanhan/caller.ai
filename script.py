import speech_recognition as sr
import os
import sys
import requests
import json
import random
from subprocess import call
from gtts import gTTS

data_plans = [["0.1GB Booster Plans", 11 ], ["1GB Booster Plans", 51], ["2GB Booster Plans", 91]]
calling_plans = [["199 Super Saver", 199], ["299 Super Saver", 299], ["399 Super Saver", 399]]
already_in_use_numbers = ["9829055445", "9731794141", "8954012345","9663595184"]

def say(msg):
    os.system("espeak -ven+f3 "+msg)

def record():
    session_id = 'zeokav'
    r = sr.Recognizer()
    m = sr.Microphone()
    a = sr.AudioFile("recording.wav")
    value = ""
    try:
        print ("Say Something!")
        with a as source: 
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)
            print ("Set minimum energy threshold to {}".format(r.energy_threshold))
            print ("Got It!")
        try:
            value = r.recognize_google(audio)
            print ("Sent: " + value)
            # say(value)
            send_to_wit(value, session_id)

        except sr.UnknownValueError:
            print("Oops! Didn't catch that")

    except KeyboardInterrupt:
        pass

def send_to_wit(input_str, session):
    response = requests.post(url='https://api.wit.ai/converse?v=20170408&session_id='+session+'&q='+input_str,headers={ "Content-Type": "application/json","Accept": "application/json","Authorization": "Bearer Y6V5XF5UNI2ETGKO3NUJLWANYKUKJIJ2"})
    dict_response = json.loads(response.text)
    print (dict_response)
    while dict_response['type']!='stop':
        if dict_response['type'] == 'action':
            try:
                if dict_response['action'] == 'updateNumber':
                    print ("ysasf")
                    inp_number = dict_response['entities']['phone_number'][0]['value']
                    inp_number = "".join(inp_number.split(" "))
                    print (inp_number)
                    if inp_number not in already_in_use_numbers:
                        print ("yes")
                        response = requests.post(url='https://api.wit.ai/converse?v=20170408&session_id='+session,headers={ "Content-Type": "application/json","Accept": "application/json","Authorization": "Bearer Y6V5XF5UNI2ETGKO3NUJLWANYKUKJIJ2"}, json={"successful":"True"})
                        dict_response = json.loads(response.text)
                        print (dict_response)
                    else:
                        print ("no")
                        response = requests.post(url='https://api.wit.ai/converse?v=20170408&session_id='+session,headers={ "Content-Type": "application/json","Accept": "application/json","Authorization": "Bearer Y6V5XF5UNI2ETGKO3NUJLWANYKUKJIJ2"}, json={"notSuccessful":"True"})
                        dict_response = json.loads(response.text)
                        print (dict_response)
            except Exception as e:
                print ("Exception in action")
        if dict_response['type'] == 'msg': 
            try:
                # say(dict_response['msg'])
                print dict_response['msg']
                # os.system("espeak -ven+f3 "+dict_response['msg']+" -w /home/raamish/projects/AH10/static/recording.wav")
                tts = gTTS(text = dict_response['msg'], lang = 'en')
                tts.save('/home/raamish/projects/AH10/static/output.mp3')
        
            except Exception as e:
                print (e)
        response = requests.post(url='https://api.wit.ai/converse?v=20170408&session_id='+session,headers={ "Content-Type": "application/json","Accept": "application/json","Authorization": "Bearer Y6V5XF5UNI2ETGKO3NUJLWANYKUKJIJ2"})
        dict_response = json.loads(response.text)
        print (dict_response)    

if __name__ == "__main__":
    record()