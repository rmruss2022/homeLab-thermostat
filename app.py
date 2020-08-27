import requests
import time
import RPi.GPIO as GPIO
import datetime
import pytz

GPIO.cleanup()

url = 'http://192.168.6.37:5000/secFloorTemp'
current_time = datetime.datetime.now(pytz.timezone('America/New_York')) 
#print(current_time.hour)

tempArr = [ 74, 77, 77, 77, 77, 77, 77, 74, 73, 73, 73, 73, 73, 73, 73, 73, 74, 74, 74, 74, 73, 72, 72, 72 ]  

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)

def getPostTemp():
    r = requests.get(url = url)
    temp = r.json()
    #print(temp)
    return temp

def getCurTemp():
    r = requests.get(url = 'http://192.168.6.37:5000/secFloorTempRT')
    temp = r.json()
    return temp

def relayON():
    GPIO.output(17, 0)
    GPIO.output(23, 0)
    GPIO.output(24, 0)

while True:
    f = open("log.txt", "a")    
    postTemp = getPostTemp()
    currTemp = getCurTemp() 
    current_hour = datetime.datetime.now(pytz.timezone('America/New_York')).hour
    f.write("TIME: " + str(datetime.datetime.now(pytz.timezone('America/New_York'))) + " | Current temp: " + str(currTemp) + " | Posted temp: " + str(postTemp) + " | Array Temp: " + str(tempArr[current_hour]) + "\n")
    
    if currTemp == -1 or type(currTemp) is dict:
        f.write("error - continuing, currTemp: " + str(currTemp) + "\n")
        continue
    if type(postTemp) is dict:
        f.write("internal server error check api\n")
        time.sleep(60)
        continue 
    if postTemp != -1:
        if postTemp < currTemp: # or type(temp) is dict:
            relayON()
            f.write("User Posted Temp: " + str(postTemp) + ", relay on!\n")
        else:
            f.write("User Posted Temp: " + str(postTemp) + " conditions not met, relay off\n")
            GPIO.output(17, 1)
            GPIO.output(23, 1)
            GPIO.output(24, 1)
    elif tempArr[current_hour] < currTemp:
        relayON()
        f.write("Temp Arr: " + str(tempArr[current_hour]) + ", relay on!\n")
    else:
        f.write("Temp arr: " + str(tempArr[current_hour]) + " conditions not met, relay off\n")
        GPIO.output(17, 1)
        GPIO.output(23, 1)
        GPIO.output(24, 1)
    f.write("----------------------------------------------------------------------------------------------------------------\n")
    f.close()
    time.sleep(60)
    GPIO.cleanup()
    

