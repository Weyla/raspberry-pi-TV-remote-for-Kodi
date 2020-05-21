import RPi.GPIO as GPIO
import os
from time import sleep
from datetime import datetime
from socket import *
import sys
try:
    from xbmcclient import *
except:
    sys.path.append('../../lib/python')
    from xbmcclient import *
    print("Except clause")
#the ip address where kodi is, can be localhost
ip = "localhost"
port = 9777
addr = (ip, port)
sock = socket(AF_INET,SOCK_DGRAM)

#The hex code of the buttons
Buttons = [0x320df02fd, 0x320df827d, 0x320dfe01f, 0x320df609f, 0x320df22dd, 0x320df0df2, 0x320df5da2,
           0x320df4eb1, 0x320dff10e, 0x320df718e, 0x320df8d72, 0x320dfda25, 0x320df14eb]
#Name of the buttons
ButtonsNames = ["up", "down", "left", "right", "OK", "play", "pause", "rec", "bw", "fw", "stop", "exit", "back"]

#Set signal pin for the IR reciever
pin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN)


while True:
    # Waiting for a signal
    GPIO.wait_for_edge(pin, GPIO.BOTH)

    n = 0
    binary = 1
    signal = []
    previousValue = 0
    startTime = datetime.now()
    startpulse = datetime.now()
    value = GPIO.input(pin)


    while True:
        # If change detected in signal
        if previousValue != value:
            now = datetime.now()
            pulseTime = now - startTime  # Calculate the time of pulse
            startTime = now  # Reset start time
            signal.append((previousValue, pulseTime.microseconds))  # Store recorded data

        # Updates consecutive 1s variable
        if value:
            n += 1
        else:
            n = 0

        # Breaks program when the amount of 1s surpasses 10000
        if n > 10000:
            break

        # Re-reads pin
        previousValue = value
        value = GPIO.input(pin)

    # Converts times to binary
    for (typ, tme) in signal:
        if typ == 1:  # If looking at rest period
            if tme > 1000:  # If pulse greater than 1000us
                binary = binary * 10 + 1  # Must be 1
            else:
                binary *= 10  # Must be 0

    if len(str(binary)) > 34:  # Sometimes, there is some stray characters
        binary = int(str(binary)[:34])
    hex_code = hex(int(str(binary), 2))


    for button in range(len(Buttons)):  # Runs through every value in list
        if hex(Buttons[button]) == hex_code:  # checks if the signal is recorded in the lest
            pressed_button = ButtonsNames[button]  # If the signal is recorded it will return the name of the button
#
#The commands for kodi goes after actionmessage
#
            if pressed_button == "up":
                pack_select = PacketACTION(actionmessage="up", actiontype=ACTION_BUTTON)
                pack_select.send(sock, addr)
            elif pressed_button == "down":
                pack_select = PacketACTION(actionmessage="down", actiontype=ACTION_BUTTON)
                pack_select.send(sock, addr)
            elif pressed_button == "exit":
                pack_select = PacketACTION(actionmessage="select", actiontype=ACTION_BUTTON)
                pack_select.send(sock, addr)
            elif pressed_button == "back":
                pack_select = PacketACTION(actionmessage="back", actiontype=ACTION_BUTTON)
                pack_select.send(sock, addr)
            elif pressed_button == "left":
                pack_select = PacketACTION(actionmessage="left", actiontype=ACTION_BUTTON)
                pack_select.send(sock, addr)
            elif pressed_button == "right":
                pack_select = PacketACTION(actionmessage="right", actiontype=ACTION_BUTTON)
                pack_select.send(sock, addr)
            elif pressed_button == "play":
                pack_select = PacketACTION(actionmessage="play", actiontype=ACTION_BUTTON)
                pack_select.send(sock, addr)
            elif pressed_button == "pause":
                pack_select = PacketACTION(actionmessage="pause", actiontype=ACTION_BUTTON)
                pack_select.send(sock, addr)
    sleep(0.1) # sleep after every command, it works without sleep, but its too fast.



