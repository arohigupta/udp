import socket
import os
import sys

def client_connect():


	'''
	create socket object
	bind the created object to the host and port
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
			data,clientAddr = s.recvfrom(4096)
			command = data.split(" ")
			command1 = command[0]
			if command1 == "get" or command1=="put":
				filename = command[1]
			else:
				pass

			#splitclient = data.split("|||")
			if command1 == "put":#command is put
				try:
					imp, clientaddr = s.recvfrom(4096)
					if (imp == "file"):
						print("Message recieved from client: PUT")
						msg=[]
						i=0
						chunks, clientaddr = s.recvfrom(4096)
						#print(chunks)
						for i in range (0,int(chunks)):
							data,clientaddr = s.recvfrom(4096)
							ackn ="hi"
							s.sendto(ackn,clientAddr)
							msg1 = data
							msg.append(msg1)

						data,clientaddr = s.recvfrom(4096)
						msg1 = data
						msg.append(msg1)
							 

						msg = ''.join(msg)
						filehandle = open(path+"/"+filename,"wb")
						filehandle.write(msg)
						filehandle.close()
						impmsg = "Message recvd from server: PUT Succesfull"
						s.sendto(impmsg,(clientaddr))
					else:
						pass

				except :
					s.sendto("Error has occured!",clientAddr)

			elif command1 == "get":#command is get
				

				print("Command recieved from client: GET")
				if (os.path.isfile(path+"/"+filename)):
					msg="yes!"
					s.sendto(msg,clientAddr)
					fh  = open(path+'/'+command[1],'rb')
					size = os.path.getsize(path+'/'+command[1])
					num_chunk = size/2048
					leftout = size%2048
					x=0
					s.sendto(str(num_chunk),clientAddr)
					for seq in range(0,num_chunk):
						x= x+2048
						strin = fh.read(2048)
						data = strin 
						s.sendto(data,clientAddr)
						data,clientAddr = s.recvfrom(4096)
						fh.seek(x)
					strin = fh.read(leftout)
					data = strin
					s.sendto(data,clientAddr)
					data,clientaddr = s.recvfrom(4096)
					print data
				else:
					msg = "Error: File could not be found"
					s.sendto(msg,clientAddr)

			elif command1 == "list" :

			
				print("Command recieved from client: LIST")
				dirs = os.listdir(path)
			
				dirs='\n'.join(dirs)
				if (dirs == ""):
					msg = "Message from server: No files in server directory!"
					s.sendto(msg,clientAddr)
				else:
					s.sendto(dirs,clientAddr)

			elif command1 == "exit" :
				print("Command recieved from client: Exit")
				print("BYE-BYE")
				s.close()
				sys.exit()
			else:
				print("Message recieved from client: "+ command[0])
				msg = "The command " + command[0] + " was not understood!"
				s.sendto(msg,clientAddr)
			#except:
			#	print "byebye"

		s.close()
	except KeyboardInterrupt :
		print "\n \n KeyboardInterrupt detected! program now terminating!"
		sys.exit(0)
if __name__ == '__main__':
	path = "serverudp"
	port = int(sys.argv[1])
	if (port < 5000):
		print "Please enter an ephermeral port"
		sys.exit(0)
	s= client_connect()
	rcvd_data(s)





