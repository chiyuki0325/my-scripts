#!/usr/bin/python
import evdev,subprocess, sys
device = evdev.InputDevice(sys.argv[1])
print(device)
X=1;Y=1
for event in device.read_loop():
    if event.type == 1 and event.value == 0:
        subprocess.Popen(['xdotool','mouseup','1'])
    if event.type == 1 and event.value == 1:
        subprocess.Popen(['xdotool','mousedown','1'])
    if event.type == 3 and event.code == 53:
        X=int(event.value/3520*1920)
    if event.type == 3 and event.code == 1:
        Y=int(event.value/1780*1080)
    print(X,Y)
    subprocess.Popen(['xdotool','mousemove',str(X),str(Y)])