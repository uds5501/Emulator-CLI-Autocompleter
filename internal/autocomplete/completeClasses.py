#!/usr/bin/env python3
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import CompleteStyle, prompt
from .listBuilder import buildAVDList

import os
import subprocess, signal

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
                )


class AVDCompleter(Completer):
    def __init__(self):
        self.avdList = []
        self.info = []
        self.meta = {}
        self.count = 0
    def refresh(self):
        if (self.count % 15 == 0):
            self.info = buildAVDList()
            if len(self.info) == len(self.avdList):
                return
            for element in self.info:
                self.avdList.append(element['name'])
                self.meta[element['name']] = element['arch'] + " | " + element['sdcard']
        self.count += 1
    
    def get_completions(self, document, complete_event):
        self.refresh()
        word = document.get_word_before_cursor()
        for avd in self.avdList:
            if avd.startswith(word):
                display = avd

                yield Completion(
                    avd,
                    start_position=-len(word),
                    display=display,
                    display_meta=self.meta.get(avd),
                )
