#!/usr/bin/env python3
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.styles import Style
from prompt_toolkit import print_formatted_text
from prompt_toolkit.shortcuts import CompleteStyle, prompt
from .listBuilder import buildAVDList, buildAPKList

import os
import subprocess, signal

style = Style.from_dict({
    'maroon' : '#000000'
})
sdkList = [
    "system-images;android-23;default;x86_64",
    "system-images;android-28;default;x86_64",
    "system-images;android-28;google_apis;x86_64"
]

sdkListMeta = {
    "system-images;android-23;default;x86_64" : HTML(
        "<ansired>Android-23 Api</ansired> ,default version, intel x86 64 bit architecture"
    ),
    "system-images;android-28;default;x86_64" : HTML(
        "<ansired>Android-28 Api</ansired> ,default version, intel x86 64 bit architecture"
    ),
    "system-images;android-28;google_apis;x86_64" : HTML(
        "<ansired>Android-28 Api</ansired> ,Google Api built In, intel x86 64 bit architecture"
    )
}

class SDKCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        for sdk in sdkList:
            if sdk.startswith(word):
                display = sdk

                yield Completion(
                    sdk,
                    start_position=-len(word),
                    display=display,
                    display_meta=sdkListMeta.get(sdk),
                    selected_style="fg:white bg:green"
                )


class AVDCompleter(Completer):
    def __init__(self):
        self.avdList = []
        self.info = []
        self.meta = {}
        self.count = 0

    def populateList(self):
        self.info = buildAVDList()
        if len(self.info) == len(self.avdList):
            return
        for element in self.info:
            self.avdList.append(element['name'])
            self.meta[element['name']] = element['arch'] + " | " + element['sdcard']

    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        for avd in self.avdList:
            if avd.startswith(word):
                display = avd

                yield Completion(
                    avd,
                    start_position=-len(word),
                    display=display,
                    display_meta=self.meta.get(avd),
                    selected_style="fg:white bg:blue"
                )

class APKCompleter(Completer):
    def __init__(self):
        self.apkList = []
        self.info = []
        self.meta = {}
        self.data = {}

    def populateList(self):
        self.apkList, self.data = buildAPKList()
        for data in self.data:
            package, size, version = self.data[data]
            self.meta[data] = HTML("<maroon>{}</maroon> | {} B | {}" .format(package, size, version))
        
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor()
        for apk in self.apkList:
            if apk.startswith(word):
                display = apk

                yield Completion(
                    apk,
                    start_position=-len(word),
                    display=display,
                    display_meta=self.meta.get(apk),
                    selected_style="fg:black bg:red"
                )