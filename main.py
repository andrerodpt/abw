import datetime as dt
from random import choice
import pandas as pd
import glob
import smtplib
from credentials import my_email, password, smtp
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --------------- Get Current Day and Month ---------------------- # 
def send_email(email, msg):
    with smtplib.SMTP(smtp) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)

        email_message = MIMEMultipart()
        email_message['Subject'] = 'HAPPY BIRTHDAY!'
        email_message['From'] = my_email
        email_message['To'] = email

        text_body = MIMEText(msg, 'plain', 'utf-8')
        email_message.attach(text_body)

        connection.sendmail(
            from_addr=my_email, 
            to_addrs=email, 
            msg=email_message.as_string()
        )

# --------------- Get Current Day and Month ---------------------- # 
current_day = dt.datetime.now().day
current_month = dt.datetime.now().month

# ------------- Get Data from birthdays.csv ---------------------- #
# Read the CSV file into a DataFrame
df = pd.read_csv('birthdays.csv')

# Create a dictionary with (month, day) as keys and lists of people as values
birthdays_dict = {}
for index, row in df.iterrows():
    birthday_key = (row['month'], row['day'])
    if birthday_key not in birthdays_dict:
        birthdays_dict[birthday_key] = []
    birthdays_dict[birthday_key].append({'name': row['name'], 'email': row['email']})

if (current_month, current_day) in birthdays_dict:
    # Get the list of people celebrating their birthday today
    people_celebrating = birthdays_dict[(current_month, current_day)]
    
    for person in people_celebrating:
        name = person['name']
        email = person['email']
        # ---------- Pick a random letter template ------------- #
        matching_files = glob.glob("letter_templates/letter_*.txt")
        template_chosen = choice(matching_files)
        # ----------- Read the template ----------------- #
        with open(template_chosen, 'r', encoding='utf-8') as template:
            template_msg = template.read()
            msg = template_msg.replace('[NAME]', name)
            send_email(email, msg)
