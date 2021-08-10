import time
import pygetwindow as gw
import win32api
import win32process
import win32con
import win32gui
from XInput import *
import pywintypes
import psutil as p
from rich import print
import pyautogui
import keyboard as k
from rich.console import Console
from rich.table import Table
import os
import PySimpleGUI as sg

resolution = []
try:
    f = open("resolution.txt", "r", encoding='utf-8')
    resolutionstring = f.read()
    resolution = resolutionstring.split(",")
    f.close()
    devmode = pywintypes.DEVMODEType()
    devmode.PelsWidth = int(resolution[0])
    devmode.PelsHeight = int(resolution[1])
    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
    win32api.ChangeDisplaySettings(devmode, 0)
except Exception:
    print("resolution.txt not found. the program will crash without it")
    print("Create a text file named resolution.txt with your desired resolution")
    print("example = 1920,1080,")
    print("The comma at the end is important")
    time.sleep(50000)
    devmode = pywintypes.DEVMODEType()
    devmode.PelsWidth = int(pyautogui.size().width)
    devmode.PelsHeight = int(pyautogui.size().height)
    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
    win32api.ChangeDisplaySettings(devmode, 0)
os.system("mode con: cols=100 lines=25")
suspended = []
owd = os.getcwd()
active = "Activated"


class WindowManagement:
    """This contains code relating to minimizing maximizing etc."""

    def __init__(self, handle):
        """Only windowhandle needed."""
        self.handle = handle

    def minimize(self, string1, string2):
        """Minimize and update the text file."""
        try:
            hwnd = int(string2.rsplit("=", 1)[1])
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        except Exception:
            print("Failed to minimize, trying again")
            windowtominimize = gw.getActiveWindow()
            windowtominimize.minimize()
        FileManagement("suspendedprocesses.txt").update_suspended_processes_file(string1, string2)
        FileManagement("suspendedprocesses.txt").update_suspended_list()

    def maximize(self, string1, string2):
        """Maximize and update the text file."""
        try:
            hwnd = int(string1.rsplit("=", 1)[1])
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            win32gui.SetForegroundWindow(hwnd)

        except Exception:
            hwnd = int(string1.rsplit("=", 1)[1])
            win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)


        string1 = str(string1)
        FileManagement("suspendedprocesses.txt").update_suspended_processes_file(string1, string2)
        FileManagement("suspendedprocesses.txt").update_suspended_list()

    def destroy(self):
        """Destroy function is used to destroy the foreground application."""
        win32gui.PostMessage(self.handle, win32con.WM_CLOSE, 0, 0)
        time.sleep(4)

    # def borderless():
        '''hwnd = win32gui.GetForegroundWindow()
        style = win32api.GetWindowLong(hwnd, -16, )
        win32api.SetWindowLong(hwnd, -16, (style & 0x00800000 | 0x00400000))'''
        # print("not ready")
        '''os.system(tasklist)
        if "BorderlessGaming" in output:
            pyautogui.hotkey('win', 'f6')
        else:
            try:
                path = "C:/Users/aryan/Desktop/Organised project files/ReXume/github/Rexume/Borderless Gaming/BorderlessGaming.exe".replace("/", "\\").rsplit("\\", 1)[0]
                os.chdir(path)
                exename = "C:/Users/aryan/Desktop/Organised project files/ReXume/github/Rexume/Borderless Gaming/BorderlessGaming.exe".replace("/", "\\").rsplit("\\", 1)[1]
                os.startfile(exename)
                os.chdir(owd)
                time.sleep(7)
                pyautogui.hotkey('win', 'f6')
            except Exception:
                pass'''


class ProcessManagement:
    """suspending and resuming code."""

    def __init__(self, handle):
        """Takes a window handle."""
        self.handle = handle

    @staticmethod
    def processname_from_handle(hwnd):
        """Gets process name."""
        pid = win32process.GetWindowThreadProcessId(hwnd)
        handle = win32api.OpenProcess(
                    win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ,
                    False,
                    pid[1])
        proc_name_path = win32process.GetModuleFileNameEx(handle, 0)
        proc_name = proc_name = proc_name_path.rsplit("\\", 1)[1]
        return proc_name

    def suspend(self):
        hwnd = int(self.handle.rsplit("=", 1)[1])
        try:
            p.Process(pid=win32process.GetWindowThreadProcessId(hwnd)[1]).suspend()
        except Exception as e:
            print(e)

    def resume(self):
        hwnd = int(self.handle.split("=", 1)[1])
        try:
            p.Process(pid=win32process.GetWindowThreadProcessId(hwnd)[1]).resume()
        except Exception as e:
            print(e)


class FileManagement:
    """contains functions to read and update the file."""

    def __init__(self, filename):
        """Takes the filename of the text file."""
        self.filename = filename

    def update_suspended_processes_file(self, string1, string2):
        """Finds string 1 and replaces it with string 2."""
        a_file = open(self.filename, "r", encoding='utf-8')
        lines = a_file.readlines()
        a_file.close()
        string = lines[0]
        modstring = string.replace(string1, string2)
        new_file = open(self.filename, "w+", encoding='utf-8')
        for line in lines:
            new_file.write(modstring)
            new_file.close()

    def update_suspended_list(self):
        f = open(self.filename, "r", encoding='utf-8')
        suspendedstring = f.read()
        global suspended
        suspended = suspendedstring.split(",")
        f.close()
        table()


class Slot(WindowManagement, ProcessManagement, FileManagement):
    @staticmethod
    def suspendsequence(slot):
        try:
            global recent
            if active == "Activated":
                if "one" in slot.name:
                    i = 0
                if "two" in slot.name:
                    i = 1
                if "three" in slot.name:
                    i = 2
                if "four" in slot.name:
                    i = 3
                if "five" in slot.name:
                    i = 4
                if "six" in slot.name:
                    i = 5
                if "seven" in slot.name:
                    i = 6
                if "eight" in slot.name:
                    i = 7
                if suspended[i] == slot.name:
                    slot.get_handle()
                    if slot.handle in suspended:
                        print("already suspended")
                    else:
                        recent = slot
                        slot.minimize(slot.name, slot.handle)
                        slot.suspend()
                else:
                    print('occupied')
        except Exception:
            print("failed to suspend")

    @staticmethod
    def resumesequence(slot):
        if active == "Activated":
            if "one" in slot.name:
                i = 0
            if "two" in slot.name:
                i = 1
            if "three" in slot.name:
                i = 2
            if "four" in slot.name:
                i = 3
            if "five" in slot.name:
                i = 4
            if "six" in slot.name:
                i = 5
            if "seven" in slot.name:
                i = 6
            if "eight" in slot.name:
                i = 7
            if suspended[i] != slot.name:
                slot.resume()
                slot.maximize(slot.handle, slot.name)
            else:
                print('empty')

    @staticmethod
    def slotname_to_object(string):
        try:
            if string in "slotone,slottwo,slotthree,slotfour,slotfive,slotsix,slotseven,sloteight,hiddenhwnd,":
                if slotone.name == string:
                    result = slotone
                if slottwo.name == string:
                    result = slottwo
                if slotthree.name == string:
                    result = slotthree
                if slotfour.name == string:
                    result = slotfour
                if slotfive.name == string:
                    result = slotfive
                if slotsix.name == string:
                    result = slotsix
                if slotseven.name == string:
                    result = slotseven
                if sloteight.name == string:
                    result = sloteight
                return result
        except Exception:
            # print(e)
            return "Nothing"

    def __init__(self, handle, name):
        """To initialize, need handle, name."""
        self.name = name
        self.handle = handle

    def get_handle(self):
        title = gw.getActiveWindow().title
        self.handle = title + "=" + str(win32gui.GetForegroundWindow())


def toggleonoffkeyboard():
    global active
    if active == "Activated":
        win32api.ChangeDisplaySettings(None, 0)
        active = "Deactivated"
        table()
        return "Deactivated"

    elif active == "Deactivated":
        win32api.ChangeDisplaySettings(devmode, 0)
        active = "Activated"
        table()
        return "Activated"


def toggleonoff(st,bk,ls,rs):
    global active
    if st == "Yes" and bk == "Yes" and ls == "Yes" and rs == "Yes":
        # print('toggling :')
        # print('RAM memory % used:', p.virtual_memory()[2])
        # print('The CPU usage is: ', p.cpu_percent(1))
        if active == "Activated":
            win32api.ChangeDisplaySettings(None, 0)
            active = "Deactivated"
            st = "No"
            bk = "No"
            rs = "No"
            ls = "No"
            table()
            # print(active)
            return "Deactivated"
        elif active == "Deactivated":
            win32api.ChangeDisplaySettings(devmode, 0)
            active = "Activated"
            # print(active)
            st = "No"
            bk = "No"
            rs = "No"
            ls = "No"
            table()
            return "Activated"


def togglehide():
    if active == "Activated":
        def HideWindow():
            global hiddenhwnd
            hiddenhwnd = win32gui.GetForegroundWindow()
            try:
                win32gui.ShowWindow(hiddenhwnd, win32con.SW_HIDE)
                FileManagement("suspendedprocesses.txt").update_suspended_processes_file("hiddenhwnd", str(hiddenhwnd))
                FileManagement("suspendedprocesses.txt").update_suspended_list()
            except Exception:
                print("no window selected")

        def ShowWindow():
            global hiddenhwnd
            try:
                FileManagement("suspendedprocesses.txt").update_suspended_processes_file(str(hiddenhwnd), "hiddenhwnd")
                FileManagement("suspendedprocesses.txt").update_suspended_list()
                win32gui.ShowWindow(hiddenhwnd, win32con.SW_SHOW)
            except Exception:
                print("No window is hidden")
            table()

        if suspended[8] == "hiddenhwnd":
            HideWindow()
        else:
            ShowWindow()


def findfreeslot():
    for i in suspended:
        if i in "slotone,slottwo,slotthree,slotfour,slotfive,slotsix,slotseven,sloteight,hiddenhwnd,":
            if slotone.name == i:
                result = slotone
                break
            if slottwo.name == i:
                result = slottwo
                break
            if slotthree.name == i:
                result = slotthree
                break
            if slotfour.name == i:
                result = slotfour
                break
            if slotfive.name == i:
                result = slotfive
                break
            if slotsix.name == i:
                result = slotsix
                break
            if slotseven.name == i:
                result = slotseven
                break
            if sloteight.name == i:
                result = sloteight
                break
    return result


def guiresume():
    if active == "Activated":
        def removeslotname(string):
            if string in "slotone,slottwo,slotthree,slotfour,slotfive,slotsix,slotseven,sloteight,hiddenhwnd,":
                return "empty"
            else:
                return string

        sg.ChangeLookAndFeel('black')
        col = [[sg.Button(slotone.name), sg.Text(removeslotname(suspended[0]), text_color='white')],
               [sg.Button(slottwo.name), sg.Text(removeslotname(suspended[1]), text_color='white')],
               [sg.Button(slotthree.name), sg.Text(removeslotname(suspended[2]), text_color='white')],
               [sg.Button(slotfour.name), sg.Text(removeslotname(suspended[3]), text_color='white')],
               [sg.Button(slotfive.name), sg.Text(removeslotname(suspended[4]), text_color='white')],
               [sg.Button(slotsix.name), sg.Text(removeslotname(suspended[5]), text_color='white')],
               [sg.Button(slotseven.name), sg.Text(removeslotname(suspended[6]), text_color='white')],
               [sg.Button(sloteight.name), sg.Text(removeslotname(suspended[7]), text_color='white')],
               [sg.Button("Cancel"), sg.Text("Don't resume anything.", text_color='white')]]

        layout = [[sg.Column(col)]]

        try:
            window = sg.Window('Resume', layout)
            event, values = window.read()
            window.close()

            if event != "Cancel":
                result = Slot.slotname_to_object(event)
                Slot.resumesequence(result)
        except Exception:
            pass


def table():
    f = open("suspendedprocesses.txt", "r", encoding='utf-8')
    suspendedstring = f.read()
    global suspended
    suspended = suspendedstring.split(",")
    f.close()

    table = Table(title="All suspended programs")
    table.add_column("Slot Number", justify="center", style="cyan", no_wrap=True)
    table.add_column("Title", style="Green", justify="center", no_wrap=True)
    table.add_column("Suspend Shortcut", style="Yellow", justify="center", no_wrap=True)
    table.add_column("Resume Shortcut", style="Yellow", justify="center", no_wrap=True)


    for ind in range(0, len(suspended) - 2):
        if suspended[ind].rsplit(" ", 1)[0] in "slotone,slottwo,slotthree,slotfour,slotfive,slotsix,slotseven,sloteight,hiddenhwnd,":
            slotname = "Slot " + str(ind + 1)
            shortcutnum = ind + 1
            shortcut = "ctrl + tab"
            shortcut2 = "shift + tab + " + str(shortcutnum)
            table.add_row(slotname, "--", shortcut, shortcut2)
        else:
            slotname = "Slot " + str(ind + 1)
            shortcutnum = ind + 1
            shortcut = "ctrl + tab"
            shortcut2 = "shift + tab + " + str(shortcutnum)
            table.add_row(slotname, suspended[ind].rsplit("=", 1)[0], shortcut, shortcut2)


    table.add_row("", "")

    if suspended[8].rsplit(" ", 1)[0] == "hiddenhwnd":
        table.add_row("Hidden window (toggle)", "--", "ctrl + shift + h", "BACK + RIGHT_THUMB + LEFT_SHOULDER")
    else:
        table.add_row("Hidden ", suspended[8].rsplit(" ", 1)[0], "ctrl + shift + h")

    table.add_row("Controller", "Back + LB + ..", "..A", "..X or ..B")
    table.add_row("", "")

    table.add_row("Status", active)

    os.system('cls')
    console = Console()
    console.print(table)


def suspendtofreeslot():
    while k.is_pressed("ctrl+tab") is True:
        time.sleep(0.2)
    if k.is_pressed("ctrl+tab") is False:
        Slot.suspendsequence(findfreeslot())


def resumerecent():
    while k.is_pressed("shift+tab") is True:
        time.sleep(0.2)
    if k.is_pressed("shift+tab") is False:
        Slot.resumesequence(recent)


try:
    FileManagement("suspendedprocesses.txt").update_suspended_list()
except Exception:
    print("text file containing processes/slot names not found")
    print("Put the suspendedprocesses.txt file in the same folder.")
    while True:
        time.sleep(10)

slotone = Slot(suspended[0], "slotone")
slottwo = Slot(suspended[1], "slottwo")
slotthree = Slot(suspended[2], "slotthree")
slotfour = Slot(suspended[3], "slotfour")
slotfive = Slot(suspended[4], "slotfive")
slotsix = Slot(suspended[5], "slotsix")
slotseven = Slot(suspended[6], "slotseven")
sloteight = Slot(suspended[7], "sloteight")
hiddenhwnd = suspended[8]
recent = slotone


k.add_hotkey("ctrl+tab",lambda: suspendtofreeslot())
k.add_hotkey("shift+tab",lambda: resumerecent())
k.add_hotkey("shift+alt",lambda: guiresume())

k.add_hotkey("shift+`+1",lambda: Slot.resumesequence(slotone))
k.add_hotkey("shift+`+2",lambda: Slot.resumesequence(slottwo))
k.add_hotkey("shift+`+3",lambda: Slot.resumesequence(slotthree))
k.add_hotkey("shift+`+4",lambda: Slot.resumesequence(slotfour))
k.add_hotkey("shift+`+5",lambda: Slot.resumesequence(slotfive))
k.add_hotkey("shift+`+6",lambda: Slot.resumesequence(slotsix))
k.add_hotkey("shift+`+7",lambda: Slot.resumesequence(slotseven))
k.add_hotkey("shift+`+8",lambda: Slot.resumesequence(sloteight))

k.add_hotkey("shift+ctrl+o",lambda: toggleonoffkeyboard())
k.add_hotkey("shift+ctrl+h",lambda: togglehide())


table()


def main():
    ls = "No"
    rs = "No"
    bk = "No"
    st = "No"
    a = "No"
    b = "No"
    x = "No"
    y = "No"
    left = "No"
    right = "No"
    up = "No"
    down = "No"
    leftthumb = "No"
    rightthumb = "No"
    while 1:
        toggleonoff(st,bk,ls,rs)
        if active == "Activated":
            if bk == "Yes" and a == "Yes" and ls == "Yes":
                while True:
                    events = get_events()
                    for event in events:
                        if event.type == EVENT_BUTTON_RELEASED:
                            if event.button == "A":
                                a = "No"
                            elif event.button == "BACK":
                                bk = "No"
                            elif event.button == "LEFT_SHOULDER":
                                ls = "No"
                    if a == "No" and bk == "No" and ls == "No":
                        Slot.suspendsequence(findfreeslot())
                        break

            elif bk == "Yes" and x == "Yes" and ls == "Yes":
                while True:
                    events = get_events()
                    for event in events:
                        if event.type == EVENT_BUTTON_RELEASED:
                            if event.button == "X":
                                x = "No"
                            elif event.button == "BACK":
                                bk = "No"
                            elif event.button == "LEFT_SHOULDER":
                                ls = "No"
                    if x == "No" and bk == "No" and ls == "No":
                        Slot.resumesequence(recent)
                        break

            elif bk == "Yes" and b == "Yes" and ls == "Yes":
                while True:
                    events = get_events()
                    for event in events:
                        if event.type == EVENT_BUTTON_RELEASED:
                            if event.button == "B":
                                b = "No"
                            elif event.button == "BACK":
                                bk = "No"
                            elif event.button == "LEFT_SHOULDER":
                                ls = "No"
                    if b == "No" and bk == "No" and ls == "No":
                        guiresume()
                        break

            elif rs == "Yes" and bk == "Yes" and a == "Yes":
                print('resume slotone')
                Slot.resumesequence(slotone)
                rs = "No"
                bk = "No"
                a = "No"

            elif rs == "Yes" and bk == "Yes" and b == "Yes":
                print('slottwo')
                Slot.resumesequence(slottwo)
                rs = "No"
                bk = "No"
                b = "No"

            elif rs == "Yes" and bk == "Yes" and x == "Yes":
                print('slotthree')
                Slot.resumesequence(slotthree)
                rs = "No"
                bk = "No"
                x = "No"

            elif rs == "Yes" and bk == "Yes" and y == "Yes":
                print('resume slotfour')
                Slot.resumesequence(slotfour)
                rs = "No"
                bk = "No"
                y = "No"

            elif rs == "Yes" and st == "Yes" and up == "Yes":
                print('resume slotfive')
                Slot.resumesequence(slotfive)
                rs = "No"
                st = "No"
                up = "No"

            elif rs == "Yes" and st == "Yes" and down == "Yes":
                print('slot DPAD_DOWN')
                Slot.resumesequence(slotsix)
                rs = "No"
                st = "No"
                down = "No"

            elif rs == "Yes" and st == "Yes" and left == "Yes":
                print('slot DPAD_LEFT')
                Slot.resumesequence(slotseven)
                rs = "No"
                st = "No"
                left = "No"

            elif rs == "Yes" and st == "Yes" and right == "Yes":
                print('slot DPAD_RIGHT')
                Slot.resumesequence(sloteight)
                rs = "No"
                st = "No"
                right = "No"

            elif rs == "Yes" and ls == "Yes" and rightthumb == "Yes" and leftthumb == "Yes":
                # pyautogui.hotkey('shift', 'ctrl', 'f')
                # pyautogui.hotkey('ctrl', 'shift', 'f')
                pyautogui.hotkey('win', 'f6')
                leftthumb = "No"
                rightthumb = "No"
                rs = "No"
                ls = "No"

            elif st == "Yes" and bk == "Yes" and x == "Yes":
                print("You pressed back + start + X. Closing application")
                WindowManagement(win32gui.GetForegroundWindow()).destroy()
                time.sleep(3)
                st = "No"
                bk = "No"
                x = "No"

            elif bk == "Yes" and rightthumb == "Yes" and rs == "Yes":
                # alt tab
                pyautogui.keyDown('alt')
                time.sleep(.2)
                pyautogui.press('tab')
                time.sleep(.2)
                pyautogui.keyUp('alt')
                bk = "No"
                rightthumb = "No"
                rs = "No"

            elif bk == "Yes" and rightthumb == "Yes" and ls == "Yes":
                # hide or show window
                togglehide()
                bk = "No"
                rightthumb = "No"
                ls = "No"
                time.sleep(1)

        events = get_events()
        for event in events:
            if event.type == EVENT_BUTTON_PRESSED:
                if event.button == "LEFT_SHOULDER":
                    ls = "Yes"
                elif event.button == "RIGHT_SHOULDER":
                    rs = "Yes"

                if event.button == "LEFT_THUMB":
                    leftthumb = "Yes"
                elif event.button == "RIGHT_THUMB":
                    rightthumb = "Yes"

                elif event.button == "BACK":
                    bk = "Yes"
                elif event.button == "START":
                    st = "Yes"

                elif event.button == "A":
                    a = "Yes"
                elif event.button == "B":
                    b = "Yes"
                elif event.button == "Y":
                    y = "Yes"
                elif event.button == "X":
                    x = "Yes"

                elif event.button == "DPAD_LEFT":
                    left = "Yes"
                elif event.button == "DPAD_RIGHT":
                    right = "Yes"
                elif event.button == "DPAD_UP":
                    up = "Yes"
                elif event.button == "DPAD_DOWN":
                    down = "Yes"

            elif event.type == EVENT_BUTTON_RELEASED:
                if event.button == "LEFT_SHOULDER":
                    ls = "No"
                elif event.button == "RIGHT_SHOULDER":
                    rs = "No"

                if event.button == "LEFT_THUMB":
                    leftthumb = "No"
                elif event.button == "RIGHT_THUMB":
                    rightthumb = "No"

                elif event.button == "BACK":
                    bk = "No"
                elif event.button == "START":
                    st = "No"

                elif event.button == "A":
                    a = "No"
                elif event.button == "B":
                    b = "No"
                elif event.button == "Y":
                    y = "No"
                elif event.button == "X":
                    x = "No"

                elif event.button == "DPAD_LEFT":
                    left = "No"
                elif event.button == "DPAD_RIGHT":
                    right = "No"
                elif event.button == "DPAD_UP":
                    up = "No"
                elif event.button == "DPAD_DOWN":
                    down = "No"
        time.sleep(0.01)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        print("program crashed, restarting in 10 seconds")
        for i in range(0, 10):
            print(i)
            time.sleep(1)
        main()
