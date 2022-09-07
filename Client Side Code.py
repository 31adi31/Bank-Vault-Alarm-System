# Bank Vault Security System

# Imports
import RPi.GPIO as GPIO
import socket
import time
import random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# UI Variables
statusList = ["╣              All Is Good!            ║", "╣    Alarm Tripped (Motion Detected)   ║", "╣     Alarm Tripped (Noise Detected)   ║",  "╣  Alarm Tripped (Vibrations Detected) ║"]
status = statusList[0]

# GPIO Setups
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# Pin IDs
pinBuzzer = 20
pinMotion = 22
pinSound = 26
pinVibration = 21
pinTouch = 25

# Pin Setups
GPIO.setup(pinMotion, GPIO.IN)
GPIO.setup(pinSound, GPIO.IN)
GPIO.setup(pinVibration, GPIO.IN)
GPIO.setup(pinBuzzer, GPIO.OUT)
GPIO.setup(pinTouch, GPIO.IN)

GPIO.output(pinBuzzer, 1)

# PIN Other Variables
motionCount = 0
soundCount = 0
vibrationCount = 0
touchCount = 0

# RSA
keyPair = RSA.generate(1024)

# Server-Client Variables
message = "-"
prevStatus = ""
aTs = "ON "
prevATS = aTs
activeStatus = True
alarmTripped = False
touchToggle = True

host = '192.168.29.1'
port = 5005

codeSendClear = "-"
codeSendMotion = "1"
codeSendSound = "2"
codeSendVibration = "3"
codeSendTouch = "0"

s = socket.socket()
s.connect((host, port))

# Starter Print Statements
for i in range(random.randint(1, 3)):
    print("connecting...")
print("Connected!")
print("Happy Monitoring!")
print()
print(" =========================< Bank Of GenCyber - Vault 2C >=========================")
print()

def printUI(onOFF, stats):
    print("╔══════════════╦════════╦════════════════════╦════════╗")
    print("╠═╗  <On/Off>  ╠════════╝      <Status>      ╚════════╣")
    print("║Å║    {}    ╔{}".format(onOFF, stats))
    print("╚═╩═══════════╩╩══════════════════════════════════════╝")    
   
printUI(aTs, status)
while True:
   
    if activeStatus:
        if GPIO.input(pinMotion):
            message = codeSendMotion
        elif GPIO.input(pinSound):
            message = codeSendSound
        elif GPIO.input(pinVibration):
            message = codeSendVibration
        else:
            message = codeSendClear
           
           
    if GPIO.input(pinTouch): # Touches!!!
        if touchToggle:
            message = codeSendTouch
            touchToggle = False
        else:
            touchToggle = True
   
    s.send(message.encode())
    data = s.recv(1024)
   
    if data.decode() == "a":
        if activeStatus: # Already ON
            activeStatus = False
            alarmTripped = False
            aTs = "OFF"
        else:   # Already OFF
            activeStatus = True
            aTs = "ON "
        status = statusList[0]
    elif data.decode() == "z":
        if activeStatus:
            alarmTripped = True
            status = statusList[1]
    elif data.decode() == "x":
        if activeStatus:
            alarmTripped = True
            status = statusList[2]
    elif data.decode() == "c":
        if activeStatus:
            alarmTripped = True
            status = statusList[3]
    else:
        status = statusList[0]
       
    if data.decode() != "=":
        if status != prevStatus or aTs != prevATS:
            printUI(aTs, status)
    prevStatus = status
    prevATS = aTs
       
       
    if alarmTripped:
        GPIO.output(pinBuzzer, 0) # ON
    else:
        GPIO.output(pinBuzzer, 1) # OFF
   
    #time.sleep(.1)

