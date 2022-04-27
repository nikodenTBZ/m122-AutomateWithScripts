import os

from dotenv import load_dotenv

load_dotenv()

def send_bill_txt_and_bill_xml_to_email(bill_txt, bill_xml, email_address):
    """
    Sends bill_txt and bill_xml to email_address.
    """
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    from_address = "nikoden@gmail.com"
    to_address = email_address
    subject = "Your bill from the internet"
    body = "Your bill from the internet"

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    attach_file_name = bill_txt
    attach_file = open(attach_file_name, 'rb')  # Open the file as binary mode
    payload = MIMEBase('application', 'octate-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload)  # encode the attachment
    # add payload header with filename
    payload.add_header('Content-Decomposition', 'attachment', filename=attach_file_name)
    msg.attach(payload)

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))  # login with mail_id and password
    text = msg.as_string()
    session.sendmail(from_address, to_address, text)
    session.quit()
    print('Mail Sent to %s' % to_address)


