#!/usr/bin/env python2

import sopel.module
import socket

linelimit = 4
bots = []

# .test #target text
@sopel.module.commands('test')
def test(bot, trigger):
    global bots
    chan = trigger.group(2).split()[0]
    text = trigger.group(2).split()[1]
    bot.say('msging %s on %s' % (text, chan))
    bot.msg(chan, text)
    bots.append({'ip':'bspar.org', 'user':'asdf', 'pass':'fdsa', 'port':'13337'})

# .scroll #target scrollfile
@sopel.module.commands('scroll')
def scroll(bot, trigger):
    chan = trigger.group(2).split()[0]
    text = trigger.group(2).split()[1]
    bot.say('Scrolling %s on %s' % (text, chan))
    lines = []
    numlines = 0
    with open('scrolls/' + text, 'rb') as f:
        for line in f:
            lines.append(line)
            numlines += 1
    numbots = numlines // linelimit
    numbots += 1 if (numlines % linelimit) else 0
    bot.say('Provisioning %d bots for this task' % numbots)
    # 'scroll protocol':
    #   line containing bot number, <space>, number of lines (e.g. '4 2\n')
    #   lines (e.g. '-----\n####\n')
    if numbots > 5:
        bot.say('> 5 bots might not work because I can\'t python and/or I\'m lazy')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 31337))
    if numbots < len(bots):
        bot.say('Not enough bots for scroll :( bailing')
    s.listen(numbots)
    for i in range(0,numbots):
        client,addr = s.accept()
        linestosend = 0
        if numlines > 4:
            linestosend = 4
            numlines -= 4
        else:
            linestosend = numlines
            numlines = 0
        client.send(str(i) + ' ' + str(linestosend) + '\n')
        bot.say(str(lines))
        for x in range(0,linestosend):
            client.send(lines[0])
            lines.remove(lines[0])
            print lines
            while not client.recv(1024) == 'ack':
                pass
            print 'barfed'
        client.close()
    bot.say('Scroll (should be) completed')
    s.close()
    return 


# .deploy <ip addr> <user> <pass> <port?>
@sopel.module.commands('deploy')
def deploy(bot, trigger):
    global bots
    ip = trigger.group(2).split()[0]
    user = trigger.group(2).split()[1]
    password = trigger.group(2).split()[2]
    port = '1337'
    try:
        port = trigger.group(2).split()[3]
    except:
        print 'No port specified for %s, assuming 1337' % ip
    bots.append({'ip':ip, 'user':user, 'pass':password, 'port':port})
