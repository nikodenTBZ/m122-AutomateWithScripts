import ftp_handler

if __name__ == '__main__':
    ftp_handler.download_file(ftp_handler.ftp_connect('ftp.haraldmueller.ch', 'schoolerinvoices', 'Berufsschule8005!'))
    ftp_handler.upload_file(ftp_handler.ftp_connect('ftp.coinditorei.com', 'zahlungssystem', 'Berufsschule8005!'))



