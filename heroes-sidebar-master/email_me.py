from email.mime.text import MIMEText
from datetime import date
import smtplib
from env import env

class email_me():

    def __init__(self):
        self.env = env()
        self.SMTP_SERVER = "smtp.gmail.com"
        self.SMTP_PORT = 587
        self.SMTP_USERNAME = self.env.sending_email
        self.SMTP_PASSWORD = self.env.email_pass
        self.EMAIL_TO = [self.env.revieving_email]
        self.EMAIL_FROM = self.env.sending_email
        self.EMAIL_SUBJECT = ""
        self.DATE_FORMAT = "%d/%m/%Y"
        self.EMAIL_SPACE = ", "
        self.DATA = ""

    def populate_email(self, subject, data):
        self.EMAIL_SUBJECT = subject;
        self.DATA = data;

    def send_email(self):
        msg = MIMEText(self.DATA)
        msg['Subject'] = self.EMAIL_SUBJECT + " %s" % (date.today().strftime(self.DATE_FORMAT))
        msg['To'] = self.EMAIL_SPACE.join(self.EMAIL_TO)
        msg['From'] = self.EMAIL_FROM
        mail = smtplib.SMTP(self.SMTP_SERVER, self.SMTP_PORT)
        mail.starttls()
        mail.login(self.SMTP_USERNAME, self.SMTP_PASSWORD)
        mail.sendmail(self.EMAIL_FROM, self.EMAIL_TO, msg.as_string())
        mail.quit()

    # if __name__=='__main__':
    #     send_email()