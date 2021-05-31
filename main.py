#Install required modules
import feedparser
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Set the link to fortinet rss feed:
url = feedparser.parse("http://pub.kb.fortinet.com/rss/firmware.xml")
entry = url.entries[1]
entrystr = str(entry)

#Set strings to check for
fortios = "FortiOS"
fortiweb = "FortiWeb"
fortigate = "FortiGate"
fortian = "FortiAnalyzer"
fortimail = "FortiMail"
fortisand = "FortiSandbox"
fortisiem = "FortiDeceptor"

latest_update = "" #Empty string to put latest update in

aa = "email@email.com"
pp = "Password"

#Set outlook SMTP settings
s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)

def save_entries():
	with open("latest.txt", "w") as myfile:
		myfile.write(entry.title)
# save_entries()
#reads the template file
def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

#get's contacts from contacts.txt
def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

names, emails = get_contacts('contacts.txt')  # read contacts
message_template = read_template('message.txt') # read message
title_template = "Nieuwe update: " + entry.title

def send_mail():
	s.starttls()
	s.login(aa, pp)
	for name, email in zip(names, emails):
		msg = MIMEMultipart()
		message = message_template.substitute(NEW_UPDATE=entry.title,DESCRIPT=entry.description)
		msg['From']=aa
		msg['To']=email
		msg['Subject']=title_template
		msg.attach(MIMEText(message, 'plain'))
		s.send_message(msg)
		del msg

def check_update():
	with open("latest.txt") as myfile:
		value = myfile.read()
		value = value.replace("[]", "")
		# print(value)
		if entry.title == value:
			print("Already found")
		else:
			send_mail()
			save_entries()
			print("mail send")

check_update()
