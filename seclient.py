import sys
import socket
import os

'''
The init function is used to create a socket and set the socket to a non blocking state with 
timer value equal to 10 seconds.
'''
def init():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)#initialises a UDP socket
		s.setblocking(0)#sets the socket to non blocking state.
		s.settimeout(10)#if the client doesnt recieve a reply from server, exception is thrown
		return s

	except:
		print "UNABLE to create socket!"
		sys.exit(0)

'''
The instruction function is used to take a instruction from the user. The instruction function then performs
tasks assigned to each instruction.

'''	

def instruction(s):
	try:
		choice = raw_input("\tget [file_name] \n\tput [file_name] \n\tlist \n\texit\n ->")
		s.sendto(choice,(host,port))
		command  = choice.split(' ')

		if (command[0] == 'put'):# If the user input is "put"
			#This if block checks if the file name entered by the user is a valid file name. If an invalid 
			#file name is entered it prompts the user to enter a correct name.
			if (os.path.isfile(path+"/"+command[1])):
				fh  = open(path+'/'+command[1],'rb')
				size = os.path.getsize(path+'/'+command[1])
				num_chunk = size/2048
				leftout = size%2048
				x=0
				s.sendto(str(num_chunk),(host,port))
				for seq in range(0,num_chunk):
					x= x+2048
					strin = fh.read(2048)
					data = strin 
					s.sendto(data,(host,port))
					data,addr = s.recvfrom(4096)
					fh.seek(x)
				strin = fh.read(leftout)
				data = strin
				s.sendto(data,(host,port))

			else:
				print "\nERROR: No such file exists!\n"
				pass
							
			 	
		elif (command[0] == 'get'):#the user has entered the get command
	
			msg=[]
			i=0
			chunks, clientaddr = s.recvfrom(4096)
			print(chunks)
			for i in range (0,int(chunks)):
				data,clientaddr = s.recvfrom(4096)
				ackn ="hi"
				s.sendto(ackn,clientaddr)
				msg1 = data
				msg.append(msg1)

			data,clientaddr = s.recvfrom(4096)
			msg1 = data
			msg.append(msg1)
				 

			msg = ''.join(msg)


			if (data == "Error: File could not be found"):#print error on client if no such data is present.
				print ("\n"+data+"\n")
			else:
				filehandle = open(path+"/"+"recieved_"+command[1],"wb")
				filehandle.write(msg)
				filehandle.close()				
				s.sendto("Message from client : Data written Sucessfully!",clientaddr)#send sucessful ack to server
							
			
		elif (command[0] == 'list'):#user enters the command list.
			#mfool2 = command[0]
			#s.sendto(mfool2, (host,port))#send the command to the server
			data,serverAddr = s.recvfrom(4096)#wait for the server's response.
			print "\nContents in servers local directory: "
			print data
			print "\n"

		elif (command[0] == 'exit') :#user enters the command exit
			ms = "lol"
			#mfool2 = command[0]
			#s.sendto(mfool2, (host,port))	#send the command to the server
		else:#if user enters an invalid command
			#s.sendto(command[0],(host,port))#send the command to the server.
			data,servAddr = s.recvfrom(4096)#wait for server's response.
			print data

		
	except KeyboardInterrupt:
		print "KeyboardInterrupt detected! Client terminating"
		sys.exit(0)



if __name__ == '__main__':
	try:
		s=init()
		path = "clientudp"#set path to the folder name in which the files of the client exists.
		while True:

			try:
				sys.argv = tuple(sys.argv)

				host= sys.argv[1]
				
				port = int(sys.argv[2])
				if (port < 5000):#check if the port number is valid
					print("Please enter port number that can be ephemeral")
					sys.exit()
			except:
				print "Please enter valid host and port numbers in command line argument!"
				sys.exit(0)
			print "Please enter a command in the following format."
			
			instruction(s)
	except KeyboardInterrupt:
		print "KeyboardInterrupt detected. terminating!"
		sys.exit(0)
	except (socket.timeout) :#handle the non blocking error.
		print "Time out has occured!! Action failed! please try again"
		instruction(s)



