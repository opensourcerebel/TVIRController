#!/usr/bin/env python
import os
import time
import sys, getopt
import RPi.GPIO as GPIO
import datetime
# Use GPIO numbers not pin numbers
GPIO.setmode(GPIO.BCM)
 
# set up the GPIO channels - one input and one output
GPIO.setup(25, GPIO.IN)

def checkIO():	
    return not GPIO.input(25)

def main(argv): 
  print "started"
  offDetected = checkIO();
  while True:
    state = checkIO();
    
    if state:    
      if offDetected:
	f = open('/home/pi/ir/myfile','a+')
	f.write('tv on: ')
	f.write(datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S"))
	f.write('\n') 
	f.close() 
	print "TV on"
	os.system('wget http://192.168.1.231:8082/cgi/query')
	os.system('su pi /home/pi/ir/startMidori.sh')
	print "midory ok, wait for tv switch"
	time.sleep(20)
	os.system('irsend SEND_ONCE neo KEY_TV')
	time.sleep(5)
	os.system('su pi /home/pi/ir/time.sh')
	os.system('su pi /home/pi/ir/pf.sh')
	time.sleep(300)	
	os.system('wget http://192.168.1.231:8082/cgi/query')
	while checkIO():
	  os.system('irsend SEND_ONCE neo KEY_1')
	  time.sleep(1)
	  os.system('irsend SEND_ONCE neo KEY_TV')
	  time.sleep(30)
	offDetected = False	
    else:
      if not offDetected:
	print "TV off"	
	f = open('/home/pi/ir/myfile','a+')
	f.write('tv off: ')
	f.write(datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S"))
	f.write('\n') 
	f.close() 
	offDetected = True
    time.sleep(1);
  print "done"
  

if __name__ == "__main__":
    main(sys.argv[1:])