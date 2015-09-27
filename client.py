#!/usr/bin/env python2

import sopel.module
import socket
import time

master = '69.255.29.32'
masterport = 31337

# .scroll #target scrollfile
@sopel.module.commands('scroll')
def scroll(bot, trigger):
    chan = trigger.group(2).split()[0]
    text = trigger.group(2).split()[1]
    msg = ''
    time.sleep(1.0)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((master,masterport))
    meta = s.recv(1024)
    bot.say(meta)
    if not meta:
        meta = s.recv(1024)
        bot.say('didn\'t get anything the first time...')
        bot.say(meta)
    botno = meta.split()[0]
    numlines = meta.split()[1]
    bot.say('I\'m bot #%s, and I will shit out %s lines' % (botno, numlines))
    print 'I\'m bot %s' % botno
    for x in range(0,int(numlines)):
        msg = s.recv(1024)
        s.send('ack')
        # bot.say('Shitting out: %s' % msg)
        bot.msg(chan, msg)
        print 'barfed %s' % msg
    bot.say('done.')
