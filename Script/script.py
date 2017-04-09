import speech_recognition as sr
import os
import sys
import requests
import json
import random
from subprocess import call

data_plans = [["11 Booster Plans", 1 ], ["51 Booster Plans", 2], ["100 Booster Plans", 3]]
calling_plans = [["199 Super Saver", 199], ["299 Super Saver", 299], ["399 Super Saver", 399]]
already_in_use_numbers = ["9829055445", "9731794141", "8954012345","9663595184"]

def say(msg):
    call(["espeak", '-ven+f3', msg], shell=True)

def record():
    session_id = 'zeokav'
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
    while dict_response['type']!='stop':
        if dict_response['type'] == 'action':
            try:
                if dict_response['action'] == 'updateNumber':
                    print ("ysasf")
                    inp_number = dict_response['entities']['phone_number'][0]['value']
                    inp_number.replace(" ", "")
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
                elif dict_response['action'] == 'getDataPlans':
                    our_data_limit = "" + dict_response['entities']['dataplan'][0]['value']
                    print (our_data_limit)
                    for i in data_plans:
                        print (i[1])
                        if i[1] == int(our_data_limit[0]):
                            plan = i[0]
                            break
                    print (plan)
                    response = requests.post(url='https://api.wit.ai/converse?v=20170408&session_id='+session,headers={ "Content-Type": "application/json","Accept": "application/json","Authorization": "Bearer Y6V5XF5UNI2ETGKO3NUJLWANYKUKJIJ2"}, json={"size":plan})
                    dict_response = json.loads(response.text)

            except Exception as e:
                print ("Exception in action")
            


        if dict_response['type'] == 'msg': 
            try:
                say(dict_response['msg'])
            except Exception as e:
                print ("Exception in message")
        
        response = requests.post(url='https://api.wit.ai/converse?v=20170408&session_id='+session,headers={ "Content-Type": "application/json","Accept": "application/json","Authorization": "Bearer Y6V5XF5UNI2ETGKO3NUJLWANYKUKJIJ2"})
        dict_response = json.loads(response.text)
        print (dict_response)

if __name__ == "__main__":
    record()