#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Demonstration of a custom completer class and the possibility of styling
completions independently by passing formatted text objects to the "display"
and "display_meta" arguments of "Completion".
"""
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import CompleteStyle, prompt
import os, subprocess, signal
from autocomplete.completeClasses import SDKCompleter, AVDCompleter, APKCompleter
import time

def createAVD():
    image = prompt("[] Please enter the SDK image name (type system for suggestions): ", completer=SDKCompleter())
    name = prompt("[] Enter the name of your virtual device: ")
    os.system("echo 'no' | avdmanager create avd -n {} -k '{}'".format(name, image))
    print("\n [] Your AVD has been created!")

def startEmulator():
    autocompleter = AVDCompleter()
    print("\n[] Please wait, populating available AVD list for suggestions")
    autocompleter.populateList()
    avdDevice = prompt("[] Please select the AVD to start : ", completer=autocompleter)
    os.system("emulator @{} -writable-system -qemu -enable-kvm &".format(avdDevice))
    time.sleep(10)
    os.system("adb root")
    print("\n [] Emulator boot signal has been sent!")
    return avdDevice

def selectAPK():
    autocompleter = APKCompleter()
    print("\n[] Please wait, populating available APKs for suggestion")
    autocompleter.populateList()
    apk = prompt("[] Please selecte the APK to install: ", completer=autocompleter)
    exit()
    APK_BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.join(os.path.realpath(__file__)))), 'apks')
    APK_PATH = "{}/{}".format(APK_BASE, apk)

    print("[] Picked : {}".format(apk))
    os.system("adb shell pm install {}".format(APK_PATH))
    print("[] Installation completed!")
    return apk, autocompleter.data.get(apk)[0]

def startApp(packageName, apk):
    print("[] Please wait, starting {} apk in the emulator!".format(apk))
    os.system("adb shell monkey -p {} -c android.intent.category.LAUNCHER 1".format(packageName))
    print("[] Run command has been sent.")

def killProcess(pName):
    command = "ps -aux | grep {}".format(pName)
    p = subprocess.check_output(command, shell=True).decode("utf-8")
    for line in p.splitlines():
        pid = line.split()[1]
        process = line.split()[10:]
        processString = ' '.join(str(x) for x in process)
        if 'emulatorKiller' in process:
           continue
        if 'qemu' in processString:
            os.system('kill -9 {}'.format(pid))

# selectAPK()
while True:
    print("[]Welcome to mini emulator demonstration!\nWhat do you wanna do today?\
           1. [] Create a new AVD Device\n\
           2. [] Run an AVD and install + run an app on it\n\
           3. [] Say sayonara.")
    choice = input()
    if choice == '1':
        createAVD()
    else if choice == '2':
        avd = startEmulator()
        apk, package = selectAPK()
        startApp(package, apk)
        time.sleep(10)
        killProcess(avd)
    else:
        exit()
