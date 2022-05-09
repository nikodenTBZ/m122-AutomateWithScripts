import os

from dotenv import load_dotenv

load_dotenv()

def send_zips_to_emails():
    """
    Sends bill_txt and bill_xml to email_address.
    """

    # create zip file for each receipts
    import zipfile

    for file in os.listdir("files/receipts"):
        import smtplib
        from email.message import EmailMessage

        # get number from file for second line and open file
        f = open(f"files/receipts/{file}", "r")
        lines = f.readlines()
        invoice_str = lines[0].split(" ")[2].split(".")[0]

        bill_number = invoice_str.split("_")[1]
        log_file = open(f"files/logs/{bill_number}_log.txt", "r")
        log_lines = log_file.readlines()
        mail = log_lines[0].split(" ")[4]
        email_reciever_first_name = log_lines[0].split(" ")[2]
        email_reciever_last_name = log_lines[0].split(" ")[3]
        email_reciever = f"{email_reciever_first_name} {email_reciever_last_name}"

        msg = EmailMessage()
        print("msg: ", msg)
        msg["From"] = "Nikoden@gmail.com"
        msg["To"] = mail
        # msg["Subject"] = f"Bestaetigung der Rechnung: {invoice_str}"
        msg["Subject"] = "Bestaetigung der Rechnung"
        msg.set_content(f"Hallo {email_reciever},\n\nIm Anhang befindet sich Ihre Rechnung: {invoice_str}")

        print(email_reciever)
        print(mail)

        zip_file = zipfile.ZipFile(f"files/zips/bill_{bill_number}.zip", "w")
        zip_file.write(f"files/receipts/{file}", file)
        # loop through all files in bill_txt and bill_xml starting with invoice_str
        for directory in os.listdir("files"):
            # check if directory is bill_txt or bill_xml
            if directory == "bill_txt" or directory == "bill_xml":
                for file2 in os.listdir(f"files/{directory}"):
                    # check if file starts with invoice_str
                    if file2.startswith(invoice_str):
                        # add file2 to zip file
                        zip_file.write(f"files/{directory}/{file2}", file2)
                        # delete file2 from directory
                        os.remove(f"files/{directory}/{file2}")
        zip_file.close()

        # attach zip file to email
        with open(f"files/zips/bill_{bill_number}.zip", "rb") as file_zip:
            file_data = file_zip.read()
            file_name = f"bill_{bill_number}.zip"
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
            smtp.send_message(msg)
            smtp.quit()
        print('Mail Sent to %s' % mail)

        # delete file
        os.remove("files/receipts/%s" % file)
        # Deleted zip file in location files/zips/bill.zip
        os.remove(f"files/zips/bill_{bill_number}.zip")
        os.remove(f"files/logs/{bill_number}_log.txt")
