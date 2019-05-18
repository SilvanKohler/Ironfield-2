import datetime
import os
import sys
import time
from random import randint

from asciimatics.event import MouseEvent
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.widgets import (Background, Button, CheckBox, DatePicker,
                                 Divider, DropdownList, Frame, Label, Layout,
                                 PopUpDialog, PopupMenu, RadioButtons, Text,
                                 TextBox, TimePicker)

import game


if len(sys.argv) >= 2:
    wholeName = sys.argv[1]
else:
    wholeName = ''
strichli = '_'
nix = ' '
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ :_*/=&%+\\<>?!^~`´|#@¦¬¢$£,.}][{-1234567890'
cursor = 0
def start():
    game.__init__(wholeName)
def menu(screen):
    screen.set_title('Ironfield 2 - Menü')
    global wholeName
    global cursor
    # time = datetime.datetime.now()
    # time = str(time).split('-')
    # time = time[2].split(':')
    # time = time[2].split('.')
    # time = int(time)
    while True:
        global nameWithCursor # sehr wichtig!, nicht unbenutzt, seriously. TODO: get rid of that...
        if cursor < 0:
            cursor = 0
        elif cursor > len(wholeName):
            cursor = len(wholeName)

        if len(wholeName) > 0:
            if cursor == len(wholeName):
                nameWithCursor = f'{wholeName[:cursor]}{strichli if int(time.time()) % 2 == 0 else nix}'
            else:
                # print(cursor)
                nameWithCursor = f'{wholeName[:cursor]}{strichli if int(time.time()) % 2 == 0 else wholeName[cursor]}{wholeName[cursor + 1:]}'
        else:
            nameWithCursor = f'{strichli if int(time.time()) % 2 == 0 else nix}'
        screen.print_at(f'C:\\users\\{nameWithCursor} ', 0, 0)
        screen.refresh()
        event = screen.get_key()
        if event == -300:
            wholeName = f'{wholeName[:cursor-1]}{wholeName[cursor:]}'
            cursor -= 1
        if event == 13:
            screen.clear()
            break
        if event == -203:
            cursor -= 1
        if event == -205:
            cursor += 1
        # print(event)

        for char in chars:
            if event == ord(char):
                wholeName = f'{wholeName[:cursor]}{char}{wholeName[cursor:]}'
                cursor += 1
                break
    screen.clear()
    screen.close()
    start()
Screen.wrapper(menu)
