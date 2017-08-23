"""
The core module of Threshette is what initialises IRC from the "config.json"
file and actually starts the bot up.
"""

import irc

import os
import random

threshette = irc.Threshette("config.json")
threshette.start()

while 1:
    threshette.get_message()

    if "PRIVMSG #()" in threshette.mailbox:
        if "hello" in threshette.mailbox:
            threshette.privmsg("#()", "Hello!")
        if "!quit" in threshette.mailbox:
            threshette.stop()
