"""
The irc module of Threshette powers the bot by defining a series of basic functions the `Threshette` class (a generic bot class) performs: these are
less to do with actual commands it can perform and more to do with the bare
necessities of IRC connection.
"""

import json
import socket

class Threshette:
    def __init__(self, config_path: str):
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
        
    def send(self, message):
        self.sock.send((message + "\r\n").encode())
        
    def privmsg(self, target, message):
        self.send("PRIVMSG {} {}".format(target, message))
    
    def connect(self):
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

    def get_message(self):
        text = self.sock.recv(2040).decode()
        
        if not self.authed and text.find("001") != -1:
            if self.registered:
                self.privmsg("NickServ", "IDENTIFY {}".format(self.PASSWORD))
            
            for channel in self.channels:
                print("Joining {}".format(channel))
                self.send("JOIN {}".format(channel))
                
            self.authed = True
        
        if text.find("PING") != -1:
            self.send("PONG {}".format(text.split(" ")[1]))
        
        return text
