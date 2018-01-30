#!/usr/bin/python

import sys , getopt#,os ,urllib
import serial#, time
import commands


# TT_tech IR Remote

remote={
"541":["power"," /usr/bin/xte 'keydown Control_L' 'key w' 'keyup Control_L'"],
"565":["vol_up","amixer -q -D pulse sset Master 5%+ unmute"],
"566":["vol_down","amixer -q -D pulse sset Master 5%- unmute"],
"558":["mute","amixer -q -D pulse sset Master toggle"],
"54F":["ok","/usr/bin/xte 'key Return'"],
"54D":["up","/usr/bin/xte 'key Up'"],
"551":["down","/usr/bin/xte 'key Down'"],
"54E":["left","/usr/bin/xte 'key Left'"],
"550":["right","/usr/bin/xte 'key Right'"],
"553":["exit","/usr/bin/xte 'key Escape'"],
"57D":["rew","/usr/bin/xte 'key j'"],
"57F":["ffwd","/usr/bin/xte 'key l'"],
"57E":["pause","/usr/bin/xte 'key k'"],
"543":["1","/usr/bin/xte 'key 1'"],
"544":["2","/usr/bin/xte 'key 2'"],
"545":["3","/usr/bin/xte 'key 3'"],
"546":["4","/usr/bin/xte 'key 4'"],
"547":["5","/usr/bin/xte 'key 5'"],
"548":["6","/usr/bin/xte 'key 6'"],
"549":["7","/usr/bin/xte 'key 7'"],
"54A":["8","/usr/bin/xte 'key 8'"],
"54B":["9","/usr/bin/xte 'key 9'"],
"54C":["0","/usr/bin/xte 'key 0'"],
"542":["menu","/usr/bin/xte 'key m'"], #"542":["swap","/usr/bin/xte 'keydown Alt_L' 'key Tab' 'keyup Alt_L'"],
"55A":["sound","/usr/bin/xte 'key KP_Subtract'"],
"564":["ch-","/usr/bin/xte 'key Page_Down'"],
"563":["ch+","/usr/bin/xte 'key Page_Up'"],
"559":["text","/usr/bin/xte 'key t'"],
"562":["epg","/usr/bin/xte 'key s'"],
"552":["info","/usr/bin/xte 'key i'"],
"57A":["record","/usr/bin/xte 'key r'"],
"57B":["play","/usr/bin/xte 'key p'"],
"57C":["stop","/usr/bin/xte 'key space'"],
"554":["red","/usr/bin/xte 'keydown Alt_L' 'key r' 'keyup Alt_L'"],
"555":["green","/usr/bin/xte 'keydown Alt_L' 'key t' 'keyup Alt_L'"],
"556":["yellow","/usr/bin/xte 'keydown Alt_L' 'key v' 'keyup Alt_L'"],
"557":["blue","/usr/bin/xte 'keydown Alt_L' 'key s' 'keyup Alt_L'"],
}

def action(command,remote):
    pass


def main(argv):
    ser = serial.Serial('/dev/ttyACM0', 9600)
    last_command=""
    # i=0
    while 1:
        serial_line = ser.readline()
        # command= serial_line[:1]
        command= serial_line[:-2]
        if (command==last_command):
            new =False
        else:
            new=True
        last_command=command
        command="5"+command[1:]

        if (command in remote):
            # print(remote[command][0])
            if new:
                antwort = commands.getoutput(remote[command][1])
                print("\n Command received: %s" %(remote[command][0]))
            else :
                print("\n Repeating: %s" %(remote[command][0]))
            # action(command,remote)
        else:
            print (" Received String : %s" %(serial_line))
    ser.close() # O


if __name__ == "__main__":
   main(sys.argv[1:])
