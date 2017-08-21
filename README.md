# threshette

An extensible, modular IRC bot written in Python.

The core body of the bot in question is implemented in an Actor pattern, chosen
because it transfers almost stupidly well to the function of an IRC bot --
an IRC bot has to accept messages and make state changes depending on the
messages it receives from the socket.
