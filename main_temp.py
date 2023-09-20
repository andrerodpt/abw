import smtplib
import datetime as dt
from random import choice
from credentials import my_email, password, smtp

with open('quotes.txt') as f:
    quotes = f.readlines()

def send_email():
    with smtplib.SMTP(smtp) as connection:
        quote = choice(quotes)
        msg = f'Subject:Motivational Monday!\n\n{quote}'
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email, 
            to_addrs="andresilvarodrigues.temp@hotmail.com", 
            msg=msg
        )

now = dt.datetime.now()
day_of_week = now.weekday()

if day_of_week == 1:
    send_email()
