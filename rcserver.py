import os
#import fake_rpi as GPIO
import RPi.GPIO as GPIO
from flask import Flask, render_template, Response
import datetime
import time




# signal pin setup
GPIO.setmode(GPIO.BCM) # Broadcom SOC channel designation

dataPin=[i for i in range(2,28)]
for dp in dataPin: GPIO.setup(dp,GPIO.IN)

LED0 = 10
LED1 = 9
LED2 = 25

# Motor Drive Interface Definition 
ENA = 13	#L298 enable A
ENB = 20	#//L298 enable B
IN1 = 19	#Motor Interface 1
IN2 = 16	#Motor Interface 2
IN3 = 21	#Motor Interface 3
IN4 = 26	#Motor Interface 4

#Ultrasonic Interface Definition
ECHO = 4	#Ultrasonic receiver pin  
TRIG = 17   #Ultrasonic transmitter pin'

#Infrared sensor interface definition
IR_R = 18	#Infrared patrol line on the right side of the car
IR_L = 27	#Infrared patrol line on the left side of the car
IR_M = 22	#Infrared obstacle avoidance in the middle of the car
IRF_R = 23	#The car follows the right infrared
IRF_L = 24	#The car follows the left infrared
global Cruising_Flag
Cruising_Flag = 0	#//当前循环模式
global Pre_Cruising_Flag
Pre_Cruising_Flag = 0 	#//预循环模式

global RevStatus
RevStatus = 0
global TurnAngle
TurnAngle=0;
global Golength
Golength=0
buffer = ['00','00','00','00','00','00']
global motor_flag
motor_flag=1

global left_speed
global right_speed
global left_speed_hold
global right_speed_hold
left_speed=100
right_speed=100


#Pin type setting and initialization

GPIO.setwarnings(False)

#leds initialized to LOW
GPIO.setup(LED0,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(LED1,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(LED2,GPIO.OUT,initial=GPIO.HIGH)

#motor initialized to low
GPIO.setup(ENA,GPIO.OUT,initial=GPIO.LOW)
ENA_pwm=GPIO.PWM(ENA,1000) 
ENA_pwm.start(0) 
ENA_pwm.ChangeDutyCycle(100)
GPIO.setup(IN1,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN2,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(ENB,GPIO.OUT,initial=GPIO.LOW)
ENB_pwm=GPIO.PWM(ENB,1000) 
ENB_pwm.start(0) 
ENB_pwm.ChangeDutyCycle(100)
GPIO.setup(IN3,GPIO.OUT,initial=GPIO.LOW)
GPIO.setup(IN4,GPIO.OUT,initial=GPIO.LOW)



#Infrared is initialized as input and set high internally
GPIO.setup(IR_R,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_L,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IR_M,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IRF_R,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(IRF_L,GPIO.IN,pull_up_down=GPIO.PUD_UP)



#Ultrasonic module pin type setting
GPIO.setup(TRIG,GPIO.OUT,initial=GPIO.LOW) #Ultrasonic module transmitter pin setting trig
GPIO.setup(ECHO,GPIO.IN,pull_up_down=GPIO.PUD_UP) #Ultrasonic module receiver pin setting echo

####CAR FUNCTIONS####

def	Open_Light():
	GPIO.output(LED0,False)
	time.sleep(1)
	print("light on")

def	Close_Light():
	GPIO.output(LED0,True)
	time.sleep(1)
    
def Motor_Forward():
	print('motor forward')
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
	GPIO.output(LED1,False)
	GPIO.output(LED2,False)
	
def Motor_Backward():
	print('motor_backward')
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
	GPIO.output(LED1,True)
	GPIO.output(LED2,False)
	
def Motor_TurnLeft():
	print('motor_turnleft')
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,True)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,True)
	GPIO.output(LED1,False)
	GPIO.output(LED2,True) 
def Motor_TurnRight():
	print('motor_turnright')
	GPIO.output(ENA,True)
	GPIO.output(ENB,True)
	GPIO.output(IN1,False)
	GPIO.output(IN2,True)
	GPIO.output(IN3,True)
	GPIO.output(IN4,False)
	GPIO.output(LED1,False)
	GPIO.output(LED2,True) 
def Motor_Stop():
	print('motor_stop')
	GPIO.output(ENA,False)
	GPIO.output(ENB,False)
	GPIO.output(IN1,False)
	GPIO.output(IN2,False)
	GPIO.output(IN3,False)
	GPIO.output(IN4,False)
	GPIO.output(LED1,True)
	GPIO.output(LED2,True)

"""

dataPin=[i for i in range(2,28)]
for dp in dataPin: GPIO.setup(dp,GPIO.IN)

data=[]
now=datetime.datetime.now()
timeString=now.strftime("%Y-%m-%d %H:%M")
templateData={
    'title': 'Raspberry Pi 3B+ Web Controller',
    'time':timeString,
    'data':data,
}
"""

#update data from GPIO input
def getData():
    data=[]
    for i,dp in enumerate(dataPin): 
        data.append(GPIO.input(dataPin[i]))
    return data


app=Flask(__name__)
    
@app.route('/')
def index():
    #return 'hello world!'
    now=datetime.datetime.now()
    timeString=now.strftime("%Y-%m-%d %H:%M")
    data=getData()
    templateData={
        'title':'Raspberry Pi 3B+ RC Car Web Controller',
        'time':timeString,
        'data':data,
    }

    return render_template('rpi3b_webcontroller.html',**templateData)           

@app.route('/<actionid>') 
def handleRequest(actionid):
    print("Button pressed : {}".format(actionid))
    if(actionid == "dig2on"):
        Open_Light()
    elif(actionid == "dig2off"):
        Close_Light()
    if(actionid == "dig3on"):
        Motor_Forward()
    elif(actionid == "dig3off"):
        Motor_Stop()
    if(actionid == "dig4on"):
        Motor_Backward()
    elif(actionid == "dig4off"):
        Motor_Stop()

    return "OK 200"   
                              
if __name__=='__main__':
    os.system("sudo rm -r  ~/.cache/chromium/Default/Cache/*")
    app.run(debug=True, port=5000, host='0.0.0.0',threaded=True)
    #local web server http://192.168.1.200:5000/
    #after Port forwarding Manipulation http://xx.xx.xx.xx:5000/
