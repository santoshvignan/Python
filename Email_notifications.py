
from email import message
import smtplib
from datetime import datetime,date

today = date.today()
current_time = datetime.now()

email_id = "xyz@xyz.com"
email_password = "blahblah"

try:
    smtp = smtplib.SMTP("smtp.gmail.com",587)
    smtp.starttls()
    smtp.login(email_id,email_password)
    SUBJECT = "IPSEC-Rekey " + str(today)
    text = "Performed a rekey at " + str(current_time)
    message = 'Subject: {}\n\n{}'.format(SUBJECT,text)
    smtp.sendmail(email_id,email_id,message)
    smtp.quit()
        
except Exception as ex:

    print ("Something went wrong",ex)