#!/usr/bin/python

# for testing:  
# https://api.telegram.org/bot111111111:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/getUpdates

import telegram
import logging
from optparse import OptionParser


optp = OptionParser()

# Output verbosity options.
optp.add_option('-q', '--quiet', help='set logging to ERROR',
                    action='store_const', dest='loglevel',
                    const=logging.ERROR, default=logging.INFO)
optp.add_option('-d', '--debug', help='set logging to DEBUG',
                    action='store_const', dest='loglevel',
                    const=logging.DEBUG, default=logging.INFO)
optp.add_option('-v', '--verbose', help='set logging to COMM',
                    action='store_const', dest='loglevel',
                    const=5, default=logging.INFO)

optp.add_option("-m", "--message", dest="message",
                    help="message to send")

opts, args = optp.parse_args()

# Setup logging.
logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

if opts.message is None:
    opts.message = raw_input("Message: ")



bot = telegram.Bot(token='1111111111:xxxxxxxxxxxxxxx')

bot.sendMessage(chat_id=-11111111, text=opts.message)
bot.sendMessage(chat_id=-11111111, text=opts.message)
