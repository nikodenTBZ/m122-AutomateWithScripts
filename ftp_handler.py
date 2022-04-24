import ftplib
import os
import re


def upload_file(ftp):
    # change directory
    ftp.cwd('/in/AP19aMiceli')

    # loop through files_to_upload folder and upload each file
    for filename in os.listdir("files_to_upload"):
        print("Uploading: " + filename)
        ftp.storbinary("STOR " + filename, open("files_to_upload/" + filename, 'rb'))


def download_file(ftp):
    # change directory
    ftp.cwd('/out/AP19aMiceli')

    pattern = r"rechnung" + r"[0-9]+" + r"\.data"
    files = ftp.nlst()

    # download file
    for file in files:
        # check if file matches pattern
        if re.search(pattern, file):
            print("Downloading: " + file)
            ftp.retrbinary("RETR " + file, open("files/" + file, 'wb').write)
            # delete file
            ftp.delete(file)
    ftp.close()


def ftp_close(ftp):
    ftp.quit()


# connect to ftp server
def ftp_connect(host, user, password):
    ftp = ftplib.FTP(host)
    ftp.login(user, password)
    return ftp
