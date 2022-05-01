import os

from dotenv import load_dotenv

load_dotenv()


def send_bill_txt_and_bill_xml_to_email(email_address):
    """
    Sends bill_txt and bill_xml to email_address.
    """
    import smtplib
    from email.message import EmailMessage

    msg = EmailMessage()
    msg["From"] = "Nikoden@gmail.com"
    msg["Subject"] = "Bestätigung der Rechnung"
    msg["To"] = email_address
    msg.set_content("Hallo,\n\nIm Anhang befindet sich Ihre Rechnung.")

    for directory in os.listdir("files"):
        for file in os.listdir(f"files/{directory}"):
            #Add file to email and check if it is xml or txt
            if file.endswith(".txt"):
                with open(f"files/{directory}/{file}", "rb") as f:
                    file_data = f.read()
                    file_name = file
                    msg.add_attachment(file_data, maintype="text", subtype="plain", filename=file_name)
            elif file.endswith(".xml"):
                with open(f"files/{directory}/{file}", "rb") as f:
                    file_data = f.read()
                    file_name = file
                    msg.add_attachment(file_data, maintype="text", subtype="xml", filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
        smtp.send_message(msg)
    print('Mail Sent to %s' % email_address)


