#!/usr/bin/env python3

import os
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
    return avds
