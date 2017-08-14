"""
The core module of Threshette is what initialises IRC from the "config.json" file and actually starts the bot up.
"""

import irc

import os
import random

threshette = irc.Threshette("config.json")
threshette.connect()

while 1:
    text = threshette.get_message()
    print(text)
 
    if "PRIVMSG #()" in text and "hello" in text:
        threshette.privmsg("#()", "Hello!")
