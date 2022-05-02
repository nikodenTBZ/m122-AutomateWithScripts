import file_handler
import ftp_handler
import mail_handler
from pathlib import Path
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    
    load_dotenv()
    #ftp_handler.download_file(ftp_handler.ftp_connect(os.getenv("FTP_URL"), 'schoolerinvoices', os.getenv("FTP_PASSWORD")))

    #file_handler.generate_files_with_content()

    #ftp_handler.upload_file(ftp_handler.ftp_connect('ftp.coinditorei.com', 'zahlungssystem', os.getenv("FTP_PASSWORD")))

    #ftp_handler.download_receipt(ftp_handler.ftp_connect('ftp.coinditorei.com', 'zahlungssystem', os.getenv("FTP_PASSWORD")))

    mail_handler.send_bill_txt_and_bill_xml_to_email("dennis.miceli@hotmail.ch")
    #ftp_handler.delete_files(ftp_handler.ftp_connect(os.getenv("FTP_URL"), 'schoolerinvoices', os.getenv("FTP_PASSWORD")))

