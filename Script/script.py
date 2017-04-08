import speech_recognition as sr
import os
import sys
import requests
import json
import random


def record():
    session_id = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(8))
    r = sr.Recognizer()
    m = sr.Microphone()
    value = ""
    try:
        while True:
            print ("Say Something!")
            with m as source: 
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                print ("Set minimum energy threshold to {}".format(r.energy_threshold))
                print ("Got It!")
            try:
                value = r.recognize_google(audio)
                print ("Sent: " + value)
                send_to_wit(value, session_id)

            except sr.UnknownValueError:
                print("Oops! Didn't catch that")

    except KeyboardInterrupt:
        pass

def send_to_wit(input_str, session):
    response = requests.post(url='https://api.wit.ai/converse?v=20170408&session_id='+session+'&q='+input_str,headers={ "Content-Type": "application/json","Accept": "application/json","Authorization": "Bearer Y6V5XF5UNI2ETGKO3NUJLWANYKUKJIJ2"})
    dict_response = json.loads(response.text)
    print (dict_response)

if __name__ == "__main__":
    record()