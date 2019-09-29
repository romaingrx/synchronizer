#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 13:16:40 2019

@author: romaingraux
"""


import time
import os
from pync import Notifier
import pync

DRIVEPATH = "/Users/romaingraux/Library/Mobile Documents/com~apple~CloudDocs/"
COMMAND = "open {}".format(DRIVEPATH)
PID = os.getpid()
TIMETOWAIT = 30

PASTENAME = 'copy'
ORIGINALPATH = '/Users/romaingraux/Documents/starting\ progs/res/original/'
# ORIGINALPATH = '/Users/romaingraux/Library/Mobile\ Documents/com~apple~CloudDocs/Romain\ GRAUX/Place\ du\ Puddleur/Proximus/'
PASTEPATH = '/Users/romaingraux/Documents/starting\ progs/res/{}/'.format(PASTENAME)

try:
    def synchronize():
        os.system('rsync -au --delete {} {}'.format(ORIGINALPATH, PASTEPATH))
        Notifier.notify("Synchronized", title='Synchro iCloud Drive', group=0)
    
    
    Notifier.notify('Synchronisation du iCloud Drive sur le RackStation activitée', title='Synchro iCloud Drive', execute='kill {}'.format(PID), group=PID)
    
    while True:
        TIMETOWAIT = 10
        synchronize()
        while TIMETOWAIT!=0:
            time.sleep(1)
            TIMETOWAIT -= 1

finally:
    Notifier.remove(PID)
    Notifier.remove(0)






