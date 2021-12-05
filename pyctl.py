#!/usr/bin/python3
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton,  QPlainTextEdit
from PyQt5 import uic
import subprocess


def cbDisplayChange():
    if (mainw.ui.cbDisplay.isChecked()):
        sub = subprocess.Popen("yes | optimus-manager --switch nvidia",
                               shell=True, stdout=subprocess.PIPE)
    else:
        sub = subprocess.Popen("yes | optimus-manager --switch intel",
                               shell=True, stdout=subprocess.PIPE)

def cbApacheChange():
    if (mainw.ui.cbApache.isChecked()):
        mainw.ui.cbApache.setText("开启")
        sub = subprocess.Popen("sudo apachectl start",
                               shell=True, stdout=subprocess.PIPE)
    else:
        mainw.ui.cbApache.setText("关闭")
        sub = subprocess.Popen("sudo apachectl stop",
                               shell=True, stdout=subprocess.PIPE)

def cbCameraChange():
    if (mainw.ui.cbCamera.isChecked()):
        mainw.ui.cbCamera.setText("启用")
        sub = subprocess.Popen("echo '1-5' | sudo tee /sys/bus/usb/drivers/usb/bind",
                               shell=True, stdout=subprocess.PIPE)
    else:
        mainw.ui.cbCamera.setText("禁用")
        sub = subprocess.Popen("echo '1-5' | sudo tee /sys/bus/usb/drivers/usb/unbind",
                               shell=True, stdout=subprocess.PIPE)

def cbCPUChange():
    if (mainw.ui.cbCPU.isChecked()):
        mainw.ui.cbCPU.setText("性能模式")
        sub = subprocess.Popen("sudo cpupower -c all frequency-set -g performance",
                               shell=True, stdout=subprocess.PIPE)
    else:
        mainw.ui.cbCPU.setText("节能模式")
        sub = subprocess.Popen("sudo cpupower -c all frequency-set -g powersave",
                               shell=True, stdout=subprocess.PIPE)

def cbMIDIChange():
    if (mainw.ui.cbMIDI.isChecked()):
        mainw.ui.cbMIDI.setText("开启")
        soundfont_name=mainw.ui.txtMIDI.toPlainText()[0:4]
        with open("/home/yidaozhan/Apps/pyctl.txt","r+") as f:
            f.write(soundfont_name)
        sub = subprocess.Popen("fluidsynth -apulseaudio /home/yidaozhan/Apps/" + soundfont_name + ".sf2 -r 44100 -s -i &",
                               shell=True, stdout=subprocess.PIPE)
    else:
        mainw.ui.cbMIDI.setText("关闭")
        sub = subprocess.Popen("killall fluidsynth",
                               shell=True, stdout=subprocess.PIPE)

def KWinClicked():
    sub = subprocess.Popen("bash -c \"killall kwin_x11 && kwin_x11 &\"",
                           shell=True, stdout=subprocess.PIPE)

def WineClicked():
    sub = subprocess.Popen("bash -c \"WINEPREFIX=$HOME/.deepinwine/Spark-TIM /usr/lib/i386-linux-gnu/deepin-wine5/wineserver -k\"",
                           shell=True, stdout=subprocess.PIPE)


class UIClass:
    def __init__(self):
        # 从文件中加载UI定义
        self.ui = uic.loadUi("/home/yidaozhan/Apps/pyctl.ui")


app = QApplication([])

mainw = UIClass()

sub = subprocess.Popen("optimus-manager --status",
                       shell=True, stdout=subprocess.PIPE)
sub.wait()
if ("nvidia" in str(sub.stdout.read()).split("\\n")[2]):
    mainw.ui.cbDisplay.setText("NVIDIA")
    mainw.ui.cbDisplay.setChecked(True)
else:
    mainw.ui.cbDisplay.setText("Intel")
    mainw.ui.cbDisplay.setChecked(False)

sub = subprocess.Popen("ps -e|grep httpd",
                       shell=True, stdout=subprocess.PIPE)
sub.wait()
if ("httpd" in str(sub.stdout.read())):
    mainw.ui.cbApache.setText("开启")
    mainw.ui.cbApache.setChecked(True)
else:
    mainw.ui.cbApache.setText("关闭")
    mainw.ui.cbApache.setChecked(False)

sub = subprocess.Popen("lsusb -t",
                       shell=True, stdout=subprocess.PIPE)
sub.wait()
if ("Driver=uvcvideo" in str(sub.stdout.read())):
    mainw.ui.cbCamera.setText("启用")
    mainw.ui.cbCamera.setChecked(True)
else:
    mainw.ui.cbCamera.setText("禁用")
    mainw.ui.cbCamera.setChecked(False)

sub = subprocess.Popen("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor",
                       shell=True, stdout=subprocess.PIPE)
sub.wait()
if ("performance" in str(sub.stdout.read())):
    mainw.ui.cbCPU.setText("性能模式")
    mainw.ui.cbCPU.setChecked(True)
else:
    mainw.ui.cbCPU.setText("节能模式")
    mainw.ui.cbCPU.setChecked(False)

sub = subprocess.Popen("ps -e|grep fluidsynth",
                       shell=True, stdout=subprocess.PIPE)
sub.wait()
if ("fluid" in str(sub.stdout.read())):
    mainw.ui.cbMIDI.setText("开启")
    mainw.ui.cbMIDI.setChecked(True)
else:
    mainw.ui.cbMIDI.setText("关闭")
    mainw.ui.cbMIDI.setChecked(False)

with open("/home/yidaozhan/Apps/pyctl.txt","r") as f:
    soundfont_name=f.readline()
    mainw.ui.txtMIDI.setPlainText(soundfont_name)

mainw.ui.cbDisplay.stateChanged.connect(cbDisplayChange)
mainw.ui.cbApache.stateChanged.connect(cbApacheChange)
mainw.ui.cbCamera.stateChanged.connect(cbCameraChange)
mainw.ui.cbCPU.stateChanged.connect(cbCPUChange)
mainw.ui.cbMIDI.stateChanged.connect(cbMIDIChange)
mainw.ui.btnKWin.clicked.connect(KWinClicked)
mainw.ui.btnWine.clicked.connect(WineClicked)
mainw.ui.show()

app.exec_()