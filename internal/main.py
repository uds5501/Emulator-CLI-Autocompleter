#!/usr/bin/env python3
"""
Demonstration of a custom completer class and the possibility of styling
completions independently by passing formatted text objects to the "display"
and "display_meta" arguments of "Completion".
"""
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import CompleteStyle, prompt
import os
from autocomplete.completeClasses import SDKCompleter, AVDCompleter

def createAVD():
    image = prompt("[] Please enter the SDK image name (type system for suggestions): ", completer=SDKCompleter())
    name = prompt("[] Enter the name of your virtual device: ")
    os.system("echo 'no' | avdmanager create avd -n {} -k '{}'".format(name, image))
    print("\n [] Your AVD has been created!")

def startEmulator():
    avdDevice = prompt("[] Please select the AVD to start : ", completer=AVDCompleter())
    os.system("\n [] emulator @{} -writable-system -qemu -enable-kvm > /dev/null 2> /tmp/emulator_error &".format(avdDevice))
    print("\n [] Emulator boot signal has been sent!")
startEmulator()