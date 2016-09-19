import sys
import socket


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
		
			foo1 = open(path+"/"+command[1],"rb")
			mfoo1 = foo1.read()
			
			foo1.close()
			mfool2 = command[0]+"|||"+command[1]+"|||"+mfoo1
		
			s.sendto(mfool2, (host,port))
			data,servAddr = s.recvfrom(1024)
			print data			
		 	
		elif (command[0] == 'get'):
			mfool2 = command[0]+"|||"+command[1]
			print mfool2
			s.sendto(mfool2, (host,port))
			print "ho"
			data,servAddr = s.recvfrom(1024)
	
			foo2 = open(path+"/"+"recv_"+command[1],"wb")
			foo2.write(data)
			print "Data written!"
			foo2.close()
			s.sendto("Sucess!",servAddr)
			if not data:
				print "no more data"
					
			
		elif (command[0] == 'list'):
			mfool2 = command[0]
			s.sendto(mfool2, (host,port))

		elif (command[0] == 'exit') :
			mfool2 = command[0]
			s.sendto(mfool2, (host,port))	
		else:
			print "please enter a valid option"
			sys.exit(0)
		#print k
		
	except KeyboardInterrupt:
		print "KeyboardInterrupt detected! program terminating"
		sys.exit(0)



if __name__ == '__main__':
	s=init()
	path = "clientudp"
	print "hi" 
	while True:

		try:
			sys.argv = tuple(sys.argv)

			host= sys.argv[1]
			
			port = int(sys.argv[2])
		except:
			print "Please enter host and port numbers in command line argument!"
			sys.exit(0)
		print "Please enter a command in the following format."
		choice = raw_input("\tget [file_name] \n\tput [file_name] \n\tlist \n\texit\n ->")
		command  = choice.split(' ')
		#print(command)
		#print(type(command[1]))
		
		
		instruction(s)



