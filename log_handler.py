import log_handler
#Create log file in files/logs/
def create_new_log_file(filename):
        #Create txt file
        filePathLogFile = "files/logs/" + filename +"_log.txt"
        print("filePathTxtInvoice", filePathLogFile)
        logFile = open(filePathLogFile, "w")
        logFile.close()
        
def open_log_file(filename):
        #Open txt file
        filePathLogFile = "files/logs/" + filename +"_log.txt"
        print("filePathTxtInvoice", filePathLogFile)
        logFile = open(filePathLogFile, "a")
        return logFile

def write_log(filename, content):
        logFile = open_log_file(filename)
        logFile.write(content + "\n")
        return logFile
    
def close_log_file(logFile):
        logFile.close()