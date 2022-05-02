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

    # create zip file
    import zipfile
    zip_file = zipfile.ZipFile("files/zips/bill.zip", "w")

    for directory in os.listdir("files"):
        for file in os.listdir(f"files/{directory}"):
            #Add file to email and check if it is xml or txt
            if file.endswith(".txt"):
                zip_file.write(f"files/{directory}/{file}", file)
            elif file.endswith(".xml"):
                zip_file.write(f"files/{directory}/{file}", file)

    zip_file.close()

    #attach zip file to email
    with open("files/zips/bill.zip", "rb") as f:
        file_data = f.read()
        file_name = f.name

    msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
        smtp.send_message(msg)
    print('Mail Sent to %s' % email_address)


