#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys , getopt,os ,urllib
#from vsgui.api import *
import commands
import datetime as dt
import pickle





# Show_stream will start either MPlayer or MythAVtest
def show_stream(liste):
   print 'Jetzt kommt: "%s"' %(liste[2])
   print 'Sender:',liste[0]
   print 'Thema:',liste[1]
   print 'Inhalt: ',liste[7]
   if liste[8][:4]=='rtmp':
      command="mplayer -fs "+liste[8] #+" 2> mplayer.err"
   else:
      command="mythavtest "+liste[8] #+" 2> mplayer.err"
   try:
      os.system(command)
   except:
      command="vlc "+liste[8]+" 2> mplayer.err"
      os.system(command)
   return()

def create_filmliste(f):
   filmliste=[]
   for line in f:
      if line[:10]=='  "X" : [ ':
         line= line[11:-4] # Cut first chars and last 4 chars
         liste=line.split('", "')
         # Merke Sender 
         if liste[0]:
            sender=liste[0]
         else:
            liste[0]=sender
            
         #Merke Thema
         if liste[1]:
            thema=liste[1]
         else:
            liste[1]=thema                  
#         if not (liste[14]==""):
#            hd=liste[14].split('|')
#            print hd
#            print liste[8]
#            liste[8]=liste[8][:int(hd[0])]+hd[1]
#            print liste[8]
            
         filmliste.append([liste[0],liste[1],liste[2],liste[3],liste[8],liste[7],liste[5]])
   return filmliste

def get_line(f):
   last2=""
   last3="xxx"
   line=""
   last=""
   while last3!=':["':
      nextchar=f.read(1)
      if nextchar=="":
	 break
      last3=last3[1:]+nextchar
#      last3=last2+nextchar
#      last2=last+nextchar
#      last=nextchar
   last=""   
#   f.read(1)
   while last3!='"],':
      nextchar=f.read(1)
      if nextchar=="":
	 break
      line += last
      last3=last3[1:]+nextchar
#      last3=last2+nextchar
#      last2=last+nextchar
      last=nextchar
   if nextchar!="":
      line=line[:-2]
      line=line.split('","')
   else:
      line =[]
   return line

def get_line_old(f):
   line=f.readline()
   if line != "}":
      line=line.split('", "')
      test= line[0][-6:]
      if test=="Sender":
	 line[0]= "Sender"
      test = line[0][:11]
      if test=='  "X" : [ "':
	 line[0]= line[0][11:]
   else :
      return []
      
   return line

def create_filmdict(f,senderliste=""):
   filmdict={}
   line=get_line_old(f)
   while line[0] != "Sender":
     line=get_line_old(f)
   if senderliste=="": 
      while True:
	 liste=get_line_old(f)
	 if liste!=[]:
	    # Merke Sender 
	    if liste[0]:
	       sender=liste[0]
	       print(sender)
	       filmdict[sender]={}
	    if liste[1]:
	       thema=liste[1]
	       thema=thema.replace("'",'_')
	       thema=thema.replace(':','_')
	       thema=thema.replace(',','_')
	       thema=thema.replace('`','_')
	       filmdict[sender][thema]=[]
	       
	    filmdict[sender][thema].append([sender,thema,liste[2],liste[3],liste[8],liste[7],liste[5],liste[14]])
	 else:
	    break
   else:
      while True:
	 liste=get_line_old(f)
	 if liste!=[]:
	    # Merke Sender 
	    if liste[0]:
	       sender=liste[0]
	       print(sender)
	       if sender in senderliste:
		  filmdict[sender]={}
		  run=True
	       else:
		  run=False
	    if run:
	       if liste[1]:
		  thema=liste[1]
		  thema=thema.replace("'",'_')
		  thema=thema.replace(':','_')
		  thema=thema.replace(',','_')
		  thema=thema.replace('`','_')
		  filmdict[sender][thema]=[]
		  
	       filmdict[sender][thema].append([sender,thema,liste[2],liste[3],liste[8],liste[7],liste[5],liste[14]])
	 else:
	    break
      
   #senderlist=["RBB","BR","HR","MDR","NDR","SWR","WDR"]
   #for sender in senderlist:
      #try: filmdict[sender]:
	 #for key in filmdict[sender]:
	    ##if key in ['Tatort','Die Sendung mit der Maus']:
	    #if True:
	       #pass
	    #else:
	       #try:
		  #del filmdict["ARD"][key]
	       #except:
		  #print "nix gefunden"
	 
   return filmdict



def write_result(name,feld,liste,url_liste):
   f_name= name+'.xml'
   f_out = open(f_name,'w')
   f_out.write('<?xml version="1.0" encoding="utf-8"?>\n<mythmenu name="'+name+'">\n\n')
   for row in liste:
      thema=row[1]
      thema=thema.replace('&','und')
      titel=row[2]
      titel=titel.replace('&','und')
      titel=titel.replace('\\"','"')
      beschreibung="Datum: "+row[3]+" Dauer: "+row[6]+"\n"+row[5]
      beschreibung=beschreibung.replace('&','und')
      beschreibung=beschreibung.replace('\\"','"')
      url=row[4]
      #url=url.replace('https','http')
      if row[7]:
	 url_HD=row[7].split("|")
	 new_url=url[:int(url_HD[0])]+url_HD[1]
	 url=new_url
	 pass
      else:
	 pass
      url=url.replace('https','http')
      if not(url in url_liste):
      #if not(url in url_liste) and row[0]==name:
         f_out.write('   <button>\n')
         f_out.write('      <type>Gucken</type>\n')
         f_out.write('      <text>'+titel+'</text>\n')
         #f_out.write('      <text>'+thema+'</text>\n')
         f_out.write("      <description>"+beschreibung+"</description>\n")
         if url[:4]=="rtmp":
#            f_out.write('      <action>EXEC mplayer --fs '+url+'</action>\n')
            f_out.write('      <action>EXEC cvlc -f '+url+'</action>\n')
         else:
            f_out.write('      <action>EXEC ~/.mythtv/themes/Meins/result/showvideo.py -v '+url+'</action>\n')
         f_out.write('   </button>\n\n')
         url_liste.append(url)
   f_out.write('\n</mythmenu>\n')
   f_out.close()
   return(url_liste)

def write_menu_xml(filename,name):
   filename=filename+'.xml'
   f_out=open(filename,'w')
   f_out.write('<?xml version="1.0" encoding="utf-8"?>\n<mythmenu name="start">\n\n')
   for row in name:
      f_out.write('   <button>\n')
      f_out.write('      <type>Gucken</type>\n')
      f_out.write('      <text>'+row+'</text>\n')
      f_out.write("      <description>"+row+" Anschauen</description>\n")
      f_out.write('      <action>MENU result/'+row+'.xml</action>\n')
      f_out.write('   </button>\n\n')
   f_out.write('\n</mythmenu>\n')
   f_out.close()

def pick(liste,last,frage):
   command='export NO_AT_BRIDGE=1 && zenity  --list  --text "'+frage+'" --checklist  --column "Pick" --column "options"'
   for row in sorted(liste):
      if row in last:
         command=command+' TRUE "'+row+'"'
      else:
         command=command+' FALSE "'+row+'"'
   command=command+' --separator="," --width 600 --height 400'
   print command
   antwort = commands.getoutput(command)
   liste = antwort.split(',')
   return liste


def update_filmliste():
   #print("wget http://wp11128329.server-he.de/filme/Filmliste-akt.xz 2>&1 | sed -u 's/.* \([0-9]\+%\)\ \+\([0-9.]\+.\) \(.*\)/\1\n# Downloading at \2\/s, ETA \3/' | zenity --progress --no-cancel --title='Downloading' --auto-close")
   #os.system("wget http://wp11128329.server-he.de/filme/Filmliste-akt.xz 2>&1 | sed -u 's/.* \\([0-9]\\+%\\)\\ \\+\\([0-9.]\\+.\\) \\(.*\\)/\\1\\n# Downloading at \\2\\/s, ETA \\3/' | zenity --progress --no-cancel --title='Downloading' --auto-close")
   try:
      os.system('rm Filmliste-akt*')
      print "Dowloading new Filmliste"
      os.system("wget http://m.picn.de/f/Filmliste-akt.xz 2>&1 | sed -u 's/.* \\([0-9]\\+%\\)\\ \\+\\([0-9.]\\+.\\) \\(.*\\)/\\1\\n# Downloading at \\2\\/s, ETA \\3/' | zenity --progress --no-cancel --title='Downloading' --auto-close")
      #urllib.urlretrieve('http://wp11128329.server-he.de/filme/Filmliste-akt.xz','Filmliste-akt.xz')
   except:
      print 'Fehler beim download'
   try:
      os.system('unxz Filmliste-akt.xz')
      inputfile= 'Filmliste-akt'
      #f_in= open(inputfile)
   except:
      print 'Fehler beim entpacken'
   return inputfile
   


def main(argv):
   inputfile = ''
   outputfile = ''
   suche=""
   update_only=False
   tree=True
   try:
      opts, args = getopt.getopt(argv,"hfui:o:s:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'parse_filmlist.py -i <inputfile> -s <searchstring>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-s"):
         suche = arg
      elif opt in ("-u"):
         update_only=True
      elif opt in ("-f"):
         tree=False
      
       
   print 'Input file is "%s"' %( inputfile )

   if update_only:
      f_in=open(update_filmliste())
#      f_in=open(inputfile)
   else:
      try:
         f_in=open(inputfile)
      except:
         f_in=open(update_filmliste())
   
   
   # Teste, ob letzte Konfiguration vorhanden ist und lade sie
   # Falls nicht, gneriere leer Konfiguration und lösche Update_only Flag
   try:
      last_conf=open('last.p','rb')
      last_themen=pickle.load(last_conf)
      last_conf.close()
   except:
      last_themen={}
      update_only=False
      
   
      
   
   #Erstelle komplette Fimliste
   if update_only:
      senderliste=list(last_themen.keys())
      film_dict=create_filmdict(f_in,senderliste)
      f_in.close()
      themen=last_themen
   else:
      film_dict=create_filmdict(f_in)
      f_in.close()
      senderliste=pick(film_dict,last_themen,"Bitte Sender wählen!")
      if not (senderliste[0]==""):
         themen={}
         for sender in senderliste:
            if sender in last_themen:
               themen[sender]=pick(film_dict[sender],last_themen[sender],"Bitte Themen für %s wählen!" %(sender))
            else:
               themen[sender]=pick(film_dict[sender],[],"Bitte Themen für %s wählen!" %(sender))
            print sender,themen[sender]
      else:
         print "fehler keine Senderwahl"
         sys.exit(15)
      last_conf=open('last.p','wb')
      pickle.dump(themen,last_conf)
         
   
      last_conf.close()

   if tree:
      url_liste=[]
      os.system('rm *.xml')
      for sender in senderliste:
         sender_xml=[]
         for thema in themen[sender]:
            if not (thema==""):
               name=sender+"_"+thema
               name=name.replace(' ','_')
               name=name.replace("'",'_')
               name=name.replace('&','und')
               name=name.replace('/','_')
               try:
                  url_liste=write_result(name,0,sorted(film_dict[sender][thema]),url_liste)
                  sender_xml.append(name)
               except:
                  print 'Thema nicht vorhanden'
                  
         if sender_xml:
            write_menu_xml(sender,sorted(sender_xml))
      write_menu_xml('start',sorted(senderliste))
   else:
      url_liste=[]
      os.system('rm *.xml')
      sender_xml=[]
      for sender in senderliste:
         for thema in themen[sender]:
            if not (thema==""):
               name=sender+"_"+thema
               name=name.replace(' ','_')
               name=name.replace("'",'_')
               name=name.replace('&','und')
               name=name.replace('/','_')
               try:
                  url_liste=write_result(name,0,film_dict[sender][thema],url_liste)
                  sender_xml.append(name)
               except:
                  print 'Thema nicht vorhanden'
                  
      if sender_xml:
         write_menu_xml('start',sorted(sender_xml))
   
   f_dict=open('film_dict.csv','w')
   for sender in film_dict:
      for themen in film_dict[sender]:
         for thema in film_dict[sender][themen]:
#            f_dict.write("'%s' '%s' '%s' '%s' '%s' '%s' '%s'\n" %(thema[0],thema[1],thema[2],thema[3],thema[4],thema[5],thema[6]))
            f_dict.write('"%s","%s","%s","%s","%s","%s","%s"\n' %(thema[0],thema[1],thema[2],thema[3],thema[4],thema[5],thema[6]))
   f_dict.close()
         
         
if __name__ == "__main__":
   main(sys.argv[1:])    


