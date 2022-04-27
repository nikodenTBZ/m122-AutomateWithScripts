import ftp_handler
import mail_handler
from pathlib import Path


if __name__ == '__main__':
    #ftp_handler.download_file(ftp_handler.ftp_connect('ftp.haraldmueller.ch', 'schoolerinvoices', 'Berufsschule8005!'))
    #ftp_handler.upload_file(ftp_handler.ftp_connect('ftp.coinditorei.com', 'zahlungssystem', 'Berufsschule8005!'))

    mail_handler.send_bill_txt_and_bill_xml_to_email("files/bill_txt/K123_11111_invoice.txt", "files/bill_xml/K123_11111_invoice.xml", "dennis.miceli@hotmail.ch")


