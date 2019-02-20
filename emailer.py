import requests
import re
import os
import smtplib

from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from email import encoders
from bs4 import BeautifulSoup
from urllib.parse import unquote

class Emailer():
    def __init__(self):
        self.query_list = []
        self.duckduckgo_uri = 'https://duckduckgo.com/html?q='

        # Gmail config
        self.mail_server = 'smtp.gmail.com'
        self.port = 587
        self.user = 'clemmingsam@gmail.com'
        self.pword = 'hazehack9856'

    def get_search_results(self, uri):
        html_doc = requests.get(uri, timeout=(5, 5))
        soup = BeautifulSoup(html_doc.content, 'lxml')
        encoded_urls = soup.find_all('a')
        urls = []

        for url in encoded_urls:
            try:
                decoded_url = unquote(unquote(url.get('href').split('=')[2]))
                urls.append(decoded_url)

            except Exception as ex:
                print("[*] Error -> " + str(ex))

        return list(set(urls))

    def mail(self, sender, to, subject, text, files):
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = COMMASPACE.join(to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        if files is not None:
            for f in files or []:
                with open(f, "rb") as fil:
                    part = MIMEApplication(fil.read(), Name=basename(f))
                # After the file is closed
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
                msg.attach(part)

        try:
            smtp = smtplib.SMTP(self.mail_server, self.port)

            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(self.user, self.pword)
            response = smtp.sendmail(sender, to, msg.as_string())

        except Exception as ex:
            print("[*] Error -> " + str(ex))

        finally:
            smtp.close()

    def get_email_address(self, url):
        try:
            html_doc = requests.get(url, timeout=(5, 5))
            result = []

            for email in re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[com]{2,4}", html_doc.text):
                if email is not None:
                    result.append(email)

            return list(set(result))

        except Exception as ex:
            print("[*] Error -> " + str(ex))

            return []


if __name__ is '__main__':
    emailer = Emailer()

    query = 'mn+software+recruiter'

    email_list = []
    urls = emailer.get_search_results(emailer.duckduckgo_uri + query)

    for url in urls:
        email_list += emailer.get_email_addresses(url)

    for email in email_list:
        emailer.mail('clemmingsam@gmail.com', email, '<NEED TO PICK A GOOD SUBJECT>', '<THINK ABOUT BODY>', None) #[COVER LETTER, RESUME])
