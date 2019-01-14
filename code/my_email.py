

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



    def send(self, address, subject, message):
        port = 465

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(self.user_name, self.password)
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['To'] = address
            msg['From'] = "bigboxnoc@gmail.com"

            #message = f"Subject: {subject}\n\n{message}"

            #server.sendmail(self.user_name, address, message)
            server.send_message(msg)

