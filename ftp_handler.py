import ftplib
import os
import re


def upload_file(ftp):
    # change directory
    ftp.cwd('/in/AP19aMiceli')

    # loop through files_to_upload folder and upload each file
    for directory in os.listdir("files"):
        # check if directory is bill_txt or bill_xml
        if directory == "bill_txt" or directory == "bill_xml":
            for file in os.listdir(f"files/{directory}"):
                print("Uploading: " + file)
                ftp.storbinary("STOR " + file, open(f"files/{directory}/" + file, 'rb'))
    ftp.quit()


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
            ftp.retrbinary("RETR " + file, open("files/raw/" + file, 'wb').write)
    ftp.quit()


def download_receipt(ftp):
    # change directory
    ftp.cwd('/out/AP19aMiceli')

    # download all files ending with .txt in ftp directory which start with quittung
    files = ftp.nlst()
    for file in files:
        if file.endswith(".txt") and file.startswith("quittung"):
            print("Downloading: " + file)
            ftp.retrbinary("RETR " + file, open("files/receipts" + file, 'wb').write)
    ftp.quit()


# connect to ftp server
def ftp_connect(host, user, password):
    ftp = ftplib.FTP(host)
    ftp.login(user, password)
    return ftp


def delete_files(ftp):
    # change directory
    ftp.cwd('/out/AP19aMiceli')

    # loop through files_to_upload folder and upload each file
    for filename in os.listdir("files/raw"):
        print("Deleting: " + filename)
        ftp.delete(filename)
    ftp.quit()
