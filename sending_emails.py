import os
import smtplib
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')


# with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    # smtp.ehlo()
    # smtp.starttls()
    # smtp.ehlo()

    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    subject = 'Grab dinner this weekend?'
    body = 'How about dinner at 6pm this Saturday?'

    msg = f'Subject: {subject}\n\n{body}'

    smtp.sendmail(EMAIL_ADDRESS, 'arijeetde@gmail.com', msg)
