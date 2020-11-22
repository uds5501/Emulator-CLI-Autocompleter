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
    image = prompt("🏁 Please enter the SDK image name (type system for suggestions): ", completer=SDKCompleter())
    name = prompt("👉 Enter the name of your virtual device: ")
    os.system("echo 'no' | avdmanager create avd -n {} -k '{}'".format(name, image))
    print("\n✅ Your AVD has been created!")

def startEmulator():
    autocompleter = AVDCompleter()
    print("\n🕑 Please wait, populating available AVD list for suggestions")
    autocompleter.populateList()
    avdDevice = prompt("💁‍ Please select the AVD to start : ", completer=autocompleter)
    os.system("emulator @{} -writable-system -qemu -enable-kvm &".format(avdDevice))
    time.sleep(10)
    os.system("adb root")
    print("\n✅ Emulator boot signal has been sent!\n\n")
    return avdDevice

def selectAPK():
    autocompleter = APKCompleter()
    print("\n🕑 Please wait, populating available APKs for suggestion")
    autocompleter.populateList()
    apk = prompt("\n📦 Please selecte the APK to install: ", completer=autocompleter)
    APK_BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.join(os.path.realpath(__file__)))), 'apks')
    APK_PATH = "{}/{}".format(APK_BASE, apk)

    print("📦 Picked : {}\n".format(apk))
    os.system("adb push '{}' '/data/local/tmp/{}'".format(APK_PATH, apk))
    time.sleep(3)
    os.system("adb shell pm install /data/local/tmp/{}".format(apk))
    print("✅ Installation completed!\n\n")
    return apk, autocompleter.data.get(apk)[0]

def startApp(packageName, apk):
    print("🕑 Please wait, starting {} apk in the emulator!".format(apk))
    os.system("adb shell monkey -p {} -c android.intent.category.LAUNCHER 1".format(packageName))
    time.sleep(3)
    print("✅ Run command has been sent.\n\n")

def killProcess(apk, pName, package):
    print("🥱 Uninstalling {}".format(apk))
    os.system("adb uninstall {}".format(package))
    print("🔪 Killing the AVD, standby comrade!\n")
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
    print("🙇‍ Welcome to mini emulator demonstration!\nWhat do you wanna do today?")
    print("1. 🔧 Create a new AVD Device\n2. 🏃 Run an AVD and install + run an app on it\n3. 👋 Say sayonara.")
    choice = input(">")
    if choice == '1':
        createAVD()
    elif choice == '2':
        avd = startEmulator()
        time.sleep(40)
        apk, package = selectAPK()
        time.sleep(10)
        startApp(package, apk)
        time.sleep(10)
        killProcess(apk, avd, package)
    else:
        print("👋 Sayonara!!")
        exit()
