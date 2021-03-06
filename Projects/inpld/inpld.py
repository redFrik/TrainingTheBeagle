# inpld project - python script
# - AIM: poll the value of a sensor and send as OSC to sclang e.g. '/gsr 52'

import OSC
from OSC import OSCClient, OSCMessage
from threading import Timer
import Adafruit_BBIO.ADC as ADC
import random # for faking random ADC values

inPin = "P9_40" # connect sensor to this pin
sendAddress = '127.0.0.1', 57120 # address to send to SuperCollider
sensingPollRate = 0.05 # rate at which values will be read (0.05 = 20ms)

def init_sensing_loop():
	Timer(sensingPollRate, sense_and_send_values).start()

def sense_and_send_values():
	# sensedValue = ADC.read(inPin)
	sensedValue = random.random() * 400 # faking it for now in the range 0 to 400
	msg = OSC.OSCMessage() # do we need the OSC. here when OSCMessage has been declared explicitingly above?
	msg.setAddress('/gsr')
	msg.append(sensedValue)
	print "sending locally to supercollider: '{0}', '{1}'".format(msg, client)
	try:
		client.send ( msg )
	except:
		print "waiting for supercollider to become available"
		pass
	init_sensing_loop() # recursive call, keeps timer going

# main:
ADC.setup()
client = OSCClient()
client.connect( sendAddress )
init_sensing_loop() # init call to start the sensing loop

try: 
     while True: 
         time.sleep(1) 

except KeyboardInterrupt:
    print "\nClosing OSCServer."
    pythonServer.close()
    print "Waiting for Server-thread to finish"
    st.join() ##!!!
    print "Done"
