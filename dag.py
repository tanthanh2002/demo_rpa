import os
from RPA.Email.ImapSmtp import ImapSmtp
from dotenv import load_dotenv
import json

load_dotenv()

mail = ImapSmtp(smtp_server=os.getenv("SMTP_SERVER"), smtp_port=os.getenv("SMTP_PORT"))
mail.authorize(account=os.getenv("GMAIL_ACCOUNT"), password=os.getenv("GMAIL_PASSWORD"))

for i in range(10):
    mail.send_message(
    sender=os.getenv("GMAIL_ACCOUNT"),
    recipients="codewary@gmail.com",
    subject="Message from RPA Python"+str(i),
    body="RPA Python message body",
    attachments="./test.txt"
    )



# criterion = "gmail:'Message from RPA Python' after:15-12-2023"
# mails = mail.list_messages(criterion=criterion)

# for m in mails:
#     uid = m["uid"]
#     sender = m["Message"].get("From")
#     subject = m["Message"].get("Subject")
#     attachment = mail.save_attachment(message=m["Message"], target_folder="./attachments/", overwrite=False)
    
#     info = { "uid": uid, "sender": sender, "subject": subject, "attachment": attachment }
#     print(json.dumps(info))

    
