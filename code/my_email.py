

import json
import smtplib
import ssl
from email.mime.text import MIMEText

class email:

    def __init__(self, config_json):

        with open(config_json) as fp:
            data = json.load(fp)

        self.user_name = data['email_user_name']
        self.password = data['email_password']
        self.server = data['mail_server']
        self.port = data['port']



    def send(self, address, subject, message):

        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['To'] = address
        msg['From'] = self.user_name

        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        connection = smtplib.SMTP(self.server, 587)
        connection.ehlo()
        connection.starttls(context=context)
        connection.ehlo()
        connection.login(self.user_name, self.password)
        connection.send_message(msg)
        connection.quit()

