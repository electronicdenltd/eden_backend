import smtplib, ssl, os
from decouple import config

HOST = config('EMAIL_HOST', default='smtp.gmail.com')
PORT = int(config('EMAIL_PORT', 587))
USER = config('EMAIL_HOST_USER')
PASSWORD = config('EMAIL_HOST_PASSWORD').replace(" ", "")

print("HOST, PORT, USER:", HOST, PORT, USER)

try:
    # connect
    smtp = smtplib.SMTP(HOST, PORT, timeout=30)
    smtp.set_debuglevel(1)   # <-- this prints the SMTP trace to stdout

    smtp.ehlo()
    smtp.starttls(context=ssl.create_default_context())
    smtp.ehlo()
    smtp.login(USER, PASSWORD)
    smtp.quit()
    print("login succeeded")
except Exception as e:
    print("EXCEPTION:", type(e), e)
