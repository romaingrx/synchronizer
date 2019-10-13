#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 13:16:40 2019

@author: romaingraux
"""

from time import sleep, localtime, strftime, strptime, mktime
import os
import subprocess
import numpy as np

#################################### VARIABLES ####################################

ORIGINALPATH = ""
COPYPATH     = ""
TIMETOWAIT   = 3600*24*2

###################################################################################
BASE = os.path.dirname(os.path.realpath(__file__))
logo1 = BASE+"/res/logo1.png"
logo2 = BASE+"/res/logo2.png"
TIMEPATH     = BASE+"/time"
COMMAND = "open {}".format(COPYPATH)
PID = os.getpid()
TIMETOWAIT = 3600*24*2

def notify(message=None, title="Synchronizer", subtitle=None, logo=logo2, open=None, execute=None, group=PID, activate=None, sender=None, image=None, sound="default", remove=None):
    arg = ""
    if(message) : arg += "-message \"%s\" "      %message
    if(sound)   : arg += "-sound \"%s\" "        %sound
    if(title)   : arg += "-title \"%s\" "        %title
    if(subtitle): arg += "-subtitle \"%s\" "     %subtitle
    if(logo)    : arg += "-appIcon \"%s\" "      %logo
    if(image)   : arg += "-contentImage \"%s\" " %image
    if(open)    : arg += "-open \"%s\" "         %open
    if(execute) : arg += "-execute \"%s\" "      %execute
    if(activate): arg += "-activate \"%s\" "     %activate
    if(sender)  : arg += "-sender \"%s\" "       %sender
    if(group)   : arg += "-group \"%s\" "        %group
    if(remove)  : arg += "-remove \"%s\" "       %remove
    command = "terminal-notifier %s" %(arg)
    os.system(command)

def set_pid():
    with open("PID", "w") as fd:
        os.system("say hello")
        fd.write(str(PID))
        fd.close()

def set_time():
    with open(TIMEPATH, "w") as fd:
        fd.write(strftime('Last synchronization -> %Y/%m/%d %H:%M:%S', localtime()))
        fd.close()

def get_time():
    with open(TIMEPATH, "r") as fd:
        str = fd.read()
        fd.close()
    return strptime(str, 'Last synchronization -> %Y/%m/%d %H:%M:%S')

def delta_time(high, low):
    seconds  = (high.tm_year-low.tm_year)*365*24*3600
    seconds += (high.tm_yday-low.tm_yday)*24*3600
    seconds += (high.tm_hour-low.tm_hour)*3600
    return int(seconds/(3600*24))


def synchronize():
    return subprocess.call("rsync -au --delete %s %s" %(ORIGINALPATH, COPYPATH), shell=True)

if __name__=='__main__':
    set_pid()
    try :
        notify('Synchronisation activée', execute=COMMAND)
        sleep(5)
        while True:
            ret = synchronize()
            if(ret == 0):
                notify('Synchronisation réussie', execute=COMMAND)
                TIMER = TIMETOWAIT
                set_time()
            else:
                notify("Plus synchronisé depuis %d jours"%(delta_time(localtime(), get_time())), subtitle="Réessaye dans 1 jour", execute=COMMAND)
                TIMER = 3600*24
            sleep(TIMER)
    finally :
        notify(title=None, logo=None, sound=None, group=None, remove=PID)
