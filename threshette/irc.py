"""This module defines the main Threshette class, which is used to create a bot.
"""

import getpass
import json
import socket

class Threshette:
    def __init__(self, config_path):
        """
        Reads the config file stored at `config_path` for the information needed
        to configure the bot, and initialises it.
        """

        # Defines the mailbox of the Actor
        self.mailbox = ""

        # Defines the starting state of the Actor
        self.authed = False
        with open(config_path) as f:
            self.config = json.load(f)

        # Uses the `config` file to provide start values
        self.host = self.config['host']
        self.port = self.config['port']
        self.nick = self.config['nick']
        self.ident = self.config['ident']
        self.realname = self.config['realname']
        self.registered = self.config['registered']

        self.channels = self.config['channels']

        # Stop values
        self.quit = self.config['quit']

        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, message):
        """
        Accepts a `str` argument and turns it into a properly formatted raw IRC
        message by appending carriage returns, encoding `str` to `bytes`, etc.
        """
        self.irc.send((message + '\r\n').encode())

    def privmsg(self, target, message):
        """
        A convenience function that makes it easier to send PRIVMSGs without
        having to type out the corresponding `send` instrunction.
        """
        self.send('PRIVMSG {} {}'.format(target, message))

    def start(self):
        """
        Performs the bare minimum to start up the bot actor, i.e. sending a USER
        and NICK message.
        """
        print("Connecting to {} at port {}".format(self.host, self.port))

        if self.registered:
            self.PASSWORD = ''
            while not self.PASSWORD:
                self.PASSWORD = getpass.getpass()
        else:
            print('WARNING: Unregistered nick may lead to clashes.')

        self.irc.connect((self.host, self.port))
        self.send('USER {} {} {} {}'.format(
            self.nick,
            self.host,
            self.ident,
            self.realname
        ))
        self.send('NICK {}'.format(self.nick))

    def on_start(self):
        """
        Defines a set of actions to be taken when the bot has successfully
        connected to IRC, here defined as "has received an 001 message from the
        server".
        """
        if self.registered:
            self.privmsg('NickServ', 'IDENTIFY {}'.format(self.PASSWORD))

        for channel in self.channels:
            self.send('JOIN {}'.format(channel))

    def stop(self):
        """
        Stops the bot actor, by sending a QUIT message to the IRC server and
        then ending the program.
        """
        print('Quitting from {}'.format(self.host))

        self.send('QUIT {}'.format(self.quit))
        self.irc.shutdown(SHUT_RDWR)
        self.irc.close()

    def get_message(self):
        """
        Reads a message from the server, up to 2040 bytes in length and
        interpreted as UTF-8-encoded data. Also handles `initialise` and
        returning PINGs where necessary.
        """
        self.mailbox = self.irc.recv(2040).decode()

        if not self.authed and self.mailbox.find('001') != -1:
            self.on_start()
            self.authed = True

        self.on_message()

    def on_message(self):
        """
        Defines the actions that the bot object should take when it receives
        a message.
        """
        if self.mailbox.find('PING') != -1:
            self.send('PONG {}'.format(self.mailbox.split(' ')[1]))
