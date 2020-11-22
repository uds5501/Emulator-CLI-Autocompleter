#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os, pathlib
import subprocess, signal

def buildAVDList():
    command = "avdmanager list avd"
    p = subprocess.check_output(command, shell=True).decode("utf-8")
    avds = []
    current = {}
    for line in p.splitlines():
        cleaned = line.strip()
        if "Available Android Virtual Devices:" in cleaned:
            continue
        if "---------" in cleaned:
            avds.append(current)
            current = {}
            continue

        splitString = cleaned.split(":")

        if len(splitString) == 2:
            if splitString[0] == "Name":
                current["name"] = splitString[1].strip()
            elif splitString[0] == "Path":
                current["path"] = splitString[1].strip()
            elif splitString[0] == "Target":
                current["target"] = splitString[1].strip()
            else:
                current["sdcard"] = splitString[1].strip()
        elif len(splitString) == 3:
            current["arch"] = splitString[1][:-7] + splitString[2].strip() 
    
    avds.append(current)
    print("[] Found {} suggestions!".format(len(avds)))
    return avds

def buildAPKList():
    dir_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.join(os.path.realpath(__file__))))), 'apks')
    apks = [i for i in os.listdir(dir_path) if '.apk' in i]
    data = {}
    for apk in apks:
        apkPath = "{}/{}".format(dir_path, apk)
        command = "apkanalyzer -h apk summary {}".format(apkPath)
        p = subprocess.check_output(command, shell=True).decode("utf-8")
        for line in p.splitlines():
            cleaned = line.strip().split()
            data[apk] = [cleaned[0], int(cleaned[1]), cleaned[2]]
            cnt += 1
    print("[] Found {} suggestions".format(len(apks)))
    return apks, data

# print(buildAPKList())