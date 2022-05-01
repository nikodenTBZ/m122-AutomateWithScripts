import file_handler
import ftp_handler
import mail_handler
from pathlib import Path


if __name__ == '__main__':
    #ftp_handler.download_file(ftp_handler.ftp_connect('ftp.haraldmueller.ch', 'schoolerinvoices', 'Berufsschule8005!'))

    file_handler.generate_files_with_content()

    #ftp_handler.upload_file(ftp_handler.ftp_connect('ftp.coinditorei.com', 'zahlungssystem', 'Berufsschule8005!'))

    #mail_handler.send_bill_txt_and_bill_xml_to_email("dennis.miceli@hotmail.ch")
    #ftp_handler.delete_files(ftp_handler.ftp_connect('ftp.haraldmueller.ch', 'schoolerinvoices', 'Berufsschule8005!'))

