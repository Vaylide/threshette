"""
The irc module of Threshette powers the bot by defining a series of basic
functions the `Threshette` class (a generic bot class) performs: these are less
to do with actual commands it can perform and more to do with the bare
necessities of IRC connection.

TODO: Reformat this code in an Actor-based format.
"""

import json
import socket

class Threshette:
    def __init__(self, config_path):
        """
        Reads the config file at `config_path` for the information needed by the
        bot, and initialises it.
        """

        self.authed = False
        self.config = json.load(open(config_path))

        self.host = self.config["host"]
        self.port = self.config["port"]
        self.nick = self.config["nick"]
        self.ident = self.config["ident"]
        self.realname = self.config["realname"]
        self.registered = self.config["registered"]

        self.channels = self.config["channels"]

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Convenience Functions

    def send(self, message):
        """
        Accepts a `str` argument and turns it into a properly formatted raw IRC
        message by appending carriage returns, encoding `str` to `bytes`, etc.
        """
        self.sock.send((message + "\r\n").encode())

    def privmsg(self, target, message):
        """
        Convenience function that eliminates a lot of the boilerplate of sending
        PRIVMSGs -- seeing as this is a bot we're going to be doing a lot of
        that, so may as well refactor repetition before it sets in.
        """
        self.send("PRIVMSG {} {}".format(target, message))

    # Event Handlers

    def on_connect(self):
        """
        Whatever needs to be performed after you've successfully authed with the
        network. This includes things like PRIVMSGs, which won't work until you
        get a message beginning with 001 (at least on SynIRC.)
        """
        if self.registered:
            self.privmsg("NickServ", "IDENTIFY {}".format(self.PASSWORD))

        for channel in self.channels:
            print("Joining {}".format(channel))
            self.send("JOIN {}".format(channel))

    def on_message(self, message):

        if message.find("PING") != -1:
            self.send("PONG {}".format(message.split(" ")[1]))

    # Initialise Actor

    def connect(self):
        """
        Performs the bare minimum needed to successfully connect to IRC, i.e.
        sending a NICK and USER message.
        """
        print("Connecting to {} at port {}.".format(self.host, self.port))

        if self.registered:
            self.PASSWORD = ""
            while not self.PASSWORD:
                self.PASSWORD = input("Nick is registered. Password: ")
        else:
            print("WARNING: Unregistered nick may lead to clashes.")

        self.sock.connect((self.host, self.port))
        self.send("USER {} {} {} {}".format(
            self.nick,
            self.host,
            self.ident,
            self.realname
        ))
        self.send("NICK {}".format(self.nick))

    # Listen to Events

    def get_message(self):
        """
        Reads a message from the server, up to 2040 bytes in length and
        interpreted as UTF-8-encoded data. Also handles `initialise` and
        returning PINGs where necessary.
        """
        text = self.sock.recv(2040).decode()

        if not self.authed and text.find("001") != -1:
            self.initialise()
            self.authed = True

        on_message()

        return text
