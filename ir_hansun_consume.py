#!/usr/bin/env python
import os
import os.path
import time
import sys, getopt
import datetime
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT) 
GPIO.setup(25, GPIO.IN)

def checkIO():	
    return GPIO.input(25)

def main(argv): 
  print "started hansun"
  offDetected = checkIO()
  while True:
    state = checkIO()
    
    if state:      
      if offDetected:
	f = open('/home/pi/ir/myfile','a+')
	f.write('tv on: ')
	f.write(datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S"))
	f.write('\n') 
	f.close()
	print "STB TV on"
	GPIO.output(4, True) ## Turn on the cam!
	os.system('su pi /home/pi/ir/startMidori.sh')
	time.sleep(40)
	os.system('irsend SEND_ONCE hdmi_switch BTN_3')
	time.sleep(6)
	os.system('su pi /home/pi/ir/time.sh')
	os.system('su pi /home/pi/ir/pf.sh')
	time.sleep(300)
	GPIO.output(4, False) ## Turn off the cam!
	offDetected = False
	print "Recording completed"
    else:
      if not offDetected:
	print "STB TV off"
	f = open('/home/pi/ir/myfile','a+')
	f.write('tv off: ')
	f.write(datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S"))
	f.write('\n') 
	f.close()
	offDetected = True
    time.sleep(1);
  print "done"
  GPIO.cleanup()
  

if __name__ == "__main__":
    main(sys.argv[1:])