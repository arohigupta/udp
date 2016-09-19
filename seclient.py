import sys
import socket
import os



def init():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return s

	except:
		print "UNABLE to create socket!"
		sys.exit(0)
	



def instruction(s):
	#print "jhky"
	try:
		#s.sendto(command, (host,port))


		if (command[0] == 'put'):
			if (os.path.isfile(path+"/"+command[1])):
				foo1 = open(path+"/"+command[1],"rb")
				mfoo1 = foo1.read()
				
				foo1.close()
				mfool2 = command[0]+"|||"+command[1]+"|||"+mfoo1
			
				s.sendto(mfool2, (host,port))
				data,servAddr = s.recvfrom(4096)
				print data	
			else:
				print "\nERROR: No such file exists!\n"
				pass
							
			 	
		elif (command[0] == 'get'):
			mfool2 = command[0]+"|||"+command[1]
			#print mfool2
			s.sendto(mfool2, (host,port))
			#print "ho"
			data,servAddr = s.recvfrom(4096)
			if (data == "Error: File could not be found"):
				print ("\n"+data+"\n")
			else:
				foo2 = open(path+"/"+"received_"+command[1],"wb")
				foo2.write(data)
				foo2.close()
				s.sendto("Data written Sucessfully!",servAddr)
						
			
		elif (command[0] == 'list'):
			mfool2 = command[0]
			s.sendto(mfool2, (host,port))
			data,serverAddr = s.recvfrom(4096)
			print "\nContents in servers local directory: "
			print data
			print "\n"

		elif (command[0] == 'exit') :
			mfool2 = command[0]
			s.sendto(mfool2, (host,port))	
		else:
			s.sendto(command[0],(host,port))
			data,servAddr = s.recvfrom(4096)
			print data
			#print "please enter a valid option"
			#sys.exit(0)
		#print k
		
	except KeyboardInterrupt:
		print "KeyboardInterrupt detected! program terminating"
		sys.exit(0)



if __name__ == '__main__':
	try:
		s=init()
		path = "clientudp"
		while True:

			try:
				sys.argv = tuple(sys.argv)

				host= sys.argv[1]
				
				port = int(sys.argv[2])
				if (port < 5000):
					print("Please enter port number that can be ephemeral")
					sys.exit()
			except:
				print "Please enter valid host and port numbers in command line argument!"
				sys.exit(0)
			print "Please enter a command in the following format."
			choice = raw_input("\tget [file_name] \n\tput [file_name] \n\tlist \n\texit\n ->")
			command  = choice.split(' ')
			instruction(s)
	except KeyboardInterrupt:
		print "KeyboardInterrupt detected. terminating!"
		sys.exit(0)


