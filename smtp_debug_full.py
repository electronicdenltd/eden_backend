import smtplib, ssl, socket, time
from decouple import config

HOST = config('EMAIL_HOST', default='smtp.gmail.com')
IP = "64.233.167.108"         # IPv4 you saw earlier
PORT = int(config('EMAIL_PORT', 587))
USER = config('EMAIL_HOST_USER')
PWD = config('EMAIL_HOST_PASSWORD').replace(" ", "")

def now(): return time.strftime("%H:%M:%S")

print(now(), "Connecting to host:", HOST, "port:", PORT)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(20)
try:
    print(now(), "socket.connect ->", IP, PORT)
    s.connect((IP, PORT))
    print(now(), "connected; recv banner...")
    banner = s.recv(4096)
    print(now(), "banner:", banner.decode(errors='replace'))
except Exception as e:
    print(now(), "SOCKET ERROR:", type(e), e)
    s.close()
    raise SystemExit(1)

# Now try STARTTLS via smtplib using file descriptor
try:
    s.close()
    smtp = smtplib.SMTP(IP, PORT, timeout=20)
    smtp.set_debuglevel(1)
    print(now(), "SMTP: ehlo/starttls/login")
    smtp.ehlo()
    smtp.starttls(context=ssl.create_default_context())
    smtp.ehlo()
    smtp.login(USER, PWD)
    print(now(), "AUTH OK")
    smtp.quit()
except Exception as e:
    print(now(), "SMTP ERROR:", type(e), e)
