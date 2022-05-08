import log_handler
#Create log file in files/logs/
def create_log_file(file_name):
        #Create txt file
        filePathLogFile = "files/logs/" + str(file_name) +"_log.txt"
        logFile = open(filePathLogFile, "w")
        close_log_file(logFile)
        logFile.close()
        
def open_log_file(filename):
        #Open txt file
        filePathLogFile = "files/logs/" + str(filename) +"_log.txt"
        logFile = open(filePathLogFile, "a")
        return logFile

def log(filename, content):
        logFile = open_log_file(filename)
        logFile.write(content + "\n")
        close_log_file(logFile)
        return logFile

def close_log_file(logFile):
        logFile.close()