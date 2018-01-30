#!/usr/bin/env python
import socket, sys, getopt

def main(argv):
   command=""
   try:
      opts, args = getopt.getopt(argv,"udmos")
   except getopt.GetoptError:
    #  print 'parse_filmlist.py -i <inputfile> -s <searchstring>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-u':
         command="MVUP\r"
      elif opt in ('-d'):
         command="MVDOWN\r"
      elif opt in ('-o'):
         command="PWON\r"
      elif opt in ('-s'):
         command="PWSTANDBY\r"
      elif opt in ('-m'):
         command="mute"
         
      
   ip = '192.168.2.37'
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   
   s.connect((ip, 23))
   nachricht = 'PW?\r'
   s.send(nachricht)
   pwstatus = s.recv(1024)
   print (pwstatus)
   if pwstatus == 'PWON\r':
      if command == "mute":
         s.send("MU?\r")
         status = s.recv(1024)
         print ("#1"+pwstatus)
         if status == "MUOFF\r":
            command = "MUON\r"
         else:
            command = "MUOFF\r"
         
      nachricht = command
      s.send(nachricht)
   else:
      if command == "PWON\r":
         s.send(command)
         pwstatus = s.recv(1024)
         print ("#1"+pwstatus)    
         nachricht = 'SI?\r'
         s.send(nachricht)
         sistatus = s.recv(1024)
         if sistatus == 'SISAT/CBL\r':
             print ("#2"+sistatus)
         else:
             s.send('SISAT/CBL\r')
             s.send("MV55\r")
   s.close()
   
             
if __name__ == "__main__":
   main(sys.argv[1:])    

