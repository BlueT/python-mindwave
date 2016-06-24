import socket, sys
from numpy import *
import scipy
from pyeeg import bin_power
from parser import Parser


p = Parser()

# Mindset
raw_eeg = True
spectra = []
iteration = 0

record_baseline = False





# TCP Server

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
	sys.stderr.write("[ERROR] %s\n" % msg[1])
	sys.exit(1)

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #reuse tcp
sock.bind(('', 54321))
sock.listen(5)
sock.settimeout(10)

attention_prev = 0
meditation_prev = 0

while True:
	(csock, adr) = sock.accept()
	print "Client Info: ", csock, adr
	#~ msg = csock.recv(1024)
	#~ if not msg:
		#~ pass
	#~ else:
		#~ print "Client send: " + msg
		#~ csock.send("Hello I'm Server.\r\n")
	#~ csock.close()
	
	#~ csock.send("Hello I'm Server.\r\n")
	
	while True:
		p.update()
		if p.sending_data:
			iteration+=1
			
			flen = 50
				
			if len(p.raw_values)>=500:
				spectrum, relative_spectrum = bin_power(p.raw_values[-p.buffer_len:], range(flen),512)
				spectra.append(array(relative_spectrum))
				if len(spectra)>30:
					spectra.pop(0)
					
				spectrum = mean(array(spectra),axis=0)
				for i in range (flen-1):
					value = float(spectrum[i]*1000) 
					#~ if i<3:
						#~ color = deltaColor
					#~ elif i<8:
						#~ color = thetaColor
					#~ elif i<13:
						#~ color = alphaColor
					#~ elif i<30:
						#~ color = betaColor
					#~ else:
						#~ color = gammaColor
					
					#~ msg = "Spectrum: " + str(25+i*10) + " + " + str(400-value) + " + " + str(value)
					#~ print "Sending: " + msg
					#~ csock.send(msg)
			else:
				pass
			
			#~ msg = "attention: " + str(p.current_attention)
			#~ print "Sending: " + msg
			#~ csock.send(msg)
			
			attention_latest = p.current_attention
			if attention_latest != attention_prev:
				attention_prev = attention_latest
				msg = "attention:" + str(attention_latest)
				print "Sending: " + msg
				csock.send(msg)
			
			
			#~ msg = "meditation: " + str(p.current_meditation)
			#~ print "Sending: " + msg
			#~ csock.send(msg)
			
			meditation_latest = p.current_meditation
			if meditation_latest != meditation_prev:
				meditation_prev = meditation_latest
				msg = "meditation:" + str(meditation_latest)
				print "Sending: " + msg
				csock.send(msg)
			
			#~ if len(p.current_vector)>7:
				#~ m = max(p.current_vector)
				#~ for i in range(7):
					#~ value = p.current_vector[i] *100.0/m
					#~ # pygame.draw.rect(window, redColor, (600+i*30,450-value, 6,value))
					#~ msg = "vector " + str(i) + ": " + str(600+i*30) + " + " + str(450-value) + " + " + str(value)
					#~ print "Sending: " + msg
					#~ csock.send(msg)
	
			#~ if raw_eeg:
				#~ lv = 0
				#~ for i,value in enumerate(p.raw_values[-1000:]):
					#~ v = value/ 255.0/ 5
					#~ # pygame.draw.line(window, redColor, (i+25,500-lv),(i+25, 500-v))
					#~ msg = "raw: " + str(i+25) + " + " + str(500-lv) + " + " + str(500-v)
					#~ print "Sending: " + msg
					#~ csock.send(msg)
					#~ lv = v
