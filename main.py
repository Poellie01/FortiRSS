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
fortisiem = "FortiSIEM"

# fortidict = set('FortiOS','FortiWeb','FortiGate','FortiAnalyzer','FortiMail','FortiSandbox')
aa = "email@email.com"
pp = "password"

#Set outlook SMTP settings
s = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)

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
message_template = read_template('message.txt')

def send_mail():
	s.starttls()
	s.login(aa, pp)
	for name, email in zip(names, emails):
		msg = MIMEMultipart()
		message = message_template.substitute(NEW_UPDATE=entry.title,)
		msg['From']=aa
		msg['To']=email
		msg['Subject']="Test123"
		msg.attach(MIMEText(message, 'plain'))
		s.send_message(msg)
		del msg


if fortisiem in entry.title:
	print("Found:", entry.title)	
	send_mail()
else: 
	print("No update for FortiOS")

if fortiweb in entry.title:
	print("Found:", entry.title)
	send_mail()
else: 
	print("No update for FortiWeb")

if fortigate in entry.title:
	print("Found:", entry.title)
	send_mail()
else: 
	print("No update for FortiGate")

if fortian in entry.title:
	print("Found:", entry.title)
	send_mail()
else: 
	print("No update for FortiAnalyzer")

if fortimail in entry.title:
	print("Found:", entry.title)
	send_mail()
else: 
	print("No update for FortiMail")

if fortisand in entry.title:
	print("Found:", entry.title)
	send_mail()
else: 
	print("No update for FortiSandbox")

if fortisiem in entry.title:
	print("Found:", entry.title)
	print("Summary:", entry.summary)
	send_mail()
else: 
	print("No update for FortiSIEM")


