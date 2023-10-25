#Enter email and password upon first use
#finaly go to https://myaccount.google.com/lesssecureapps and turn on less secure apps
#you are set to go ;)

import imaplib
import datetime
from email.utils import parsedate_tz, mktime_tz

# your email address
email = 'test@gmail.com'
# your email password
password = '************'
# the sender you want to delete messages from
sender = 'spam@example.com'
# the IMAP server to connect to Gmail
imap_server = 'imap.gmail.com'

# create an IMAP4 object and login
mail = imaplib.IMAP4_SSL (imap_server)
mail.login (email, password)

# select the inbox folder
mail.select ('inbox')

# search for messages from the sender in the last 24 hours
today = datetime.date.today ()
yesterday = today - datetime.timedelta (days=1)
date_str = yesterday.strftime ('%d-%b-%Y')
typ, data = mail.search (None, f'(FROM "{sender}" SENTSINCE {date_str})')

# loop through the message ids and mark them as deleted
for num in data [0].split (): 
  # fetch the message date
  typ, msg_data = mail.fetch (num, '(BODY.PEEK[HEADER.FIELDS (DATE)])')
  msg_date = msg_data [0] [1].decode ().strip ()
  # parse the date and convert it to a timestamp
  date_tuple = parsedate_tz (msg_date [5:])
  timestamp = mktime_tz (date_tuple)
  # check if the message is within the last 24 hours
  if datetime.datetime.now ().timestamp () - timestamp < 86400:
    # mark the message as deleted
    mail.store (num, '+FLAGS', '\\Deleted')

# expunge the deleted messages
mail.expunge ()

# close the mailbox and logout
mail.close ()
mail.logout ()
