import socket
import os
import sys

def client_connect():


	'''
	create socket object
	bind the created object to the host and port
	listen for 1 active connections
	accept the connections which returns connection and address
	'''
	try:
		s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	except:
		print "failed to create socket" 
	try:
		s.bind(("",port))
	except socket.error as msg:
		print 'Failed to bind . Error :' + str(msg[0])+ 'Message = ' + str(msg[1])
		sys.exit()
	
	print "Waiting for port...", port
	return s
	


def rcvd_data(s):
	try:
		while True : 
			data,clientAddr = s.recvfrom(1024)
			print data
			#try:
			splitclient = data.split("|||")
			if len(splitclient) == 3:#command is put
				try:
					command = splitclient[0]
					filename = splitclient[1]
					content = splitclient[2]
					foo2 = open(path+"/"+filename,"wb")
					foo2.write(content)
					print "Data written!"
					foo2.close()
					s.sendto("Sucess!",clientAddr)
					if not data:
						print "no more data"
						break
				except :
					s.sendto("Error has occured!",clientAddr)

			elif len(splitclient) == 2 :#command is get
				command = splitclient[0]
				filename = splitclient[1]
				foo1 = open(path+"/"+filename,"rb")
				mfoo1 = foo1.read()
				foo1.close()
				s.sendto(mfoo1,clientAddr)
			elif len(splitclient) == 1 :
				if splitclient[0] == "list" :
					print "list"
					#path = "serverudp"
				
					#print "hio"
					#print path


					dirs = os.listdir(path)
					for files in dirs:
						print files
				else :
					print "exit"
			#except:
			#	print "byebye"

		s.close()
	except KeyboardInterrupt :
		print "\n \n KeyboardInterrupt detected! program now terminating!"
		sys.exit(0)
if __name__ == '__main__':
	path = "serverudp"
	
	port = int(sys.argv[1])

	s= client_connect()
	print (sys.argv[0])

	#choice,clientAddr = s.recvfrom(1024)
	#print choice


	rcvd_data(s)





