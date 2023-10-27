`#Enter email and password upon first use
#finaly go to https://myaccount.google.com/lesssecureapps and turn on less secure apps
#you are set to go ;)

import imaplib
import datetime
from email.utils import parsedate_tz, mktime_tz

# your email address
email = 'test@gmail.com'
# your email password
password = '************'
# the sender you want to delete messages from, usaly someones name, not an email
sender = 'bob'
# the IMAP server to connect to Gmail
imap_server = 'imap.gmail.com'

# create an IMAP4 object and login
mail = imaplib.IMAP4_SSL (imap_server)
mail.login (email, password)
print("Logged in successfully")

# select the inbox folder
mail.select ('inbox')
print("Selected inbox folder")

# search for messages from the sender in the last week
today = datetime.date.today ()
#change days to whatever
week_ago = today - datetime.timedelta (days=7)
date_str = week_ago.strftime ('%d-%b-%Y')
typ, data = mail.search (None, f'(FROM "{sender}" SENTSINCE {date_str})')
print(f"Found {len(data[0].split())} messages from {sender} since {date_str}")

# loop through the message ids and mark them as deleted
deleted_count = 0 # keep track of how many messages are deleted
for num in data [0].split (): 
  # fetch the message date
  typ, msg_data = mail.fetch (num, '(BODY.PEEK[HEADER.FIELDS (DATE)])')
  msg_date = msg_data [0] [1].decode ().strip ()
  # parse the date and convert it to a timestamp
  date_tuple = parsedate_tz (msg_date [5:])
  timestamp = mktime_tz (date_tuple)
  # check if the message is within the last week
  if datetime.datetime.now ().timestamp () - timestamp < 604800:
    # mark the message as deleted
    mail.store (num, '+FLAGS', '\\Deleted')
    deleted_count += 1 # increment the deleted count
    print(f"Marked message {num.decode()} as deleted")

# expunge the deleted messages
mail.expunge ()
print(f"Expunged {deleted_count} messages")

# close the mailbox and logout
mail.close ()
mail.logout ()
print("Closed mailbox and logged out")
print("done")
