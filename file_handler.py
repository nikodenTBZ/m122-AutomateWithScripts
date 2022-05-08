# Read the filecontent of the .data file split by ; into variables and print those variables into the console and
# save the different variables into a list
import os
import re
import log_handler
from datetime import datetime, timedelta

# debug = True
debug = False

def generate_files_with_content():
    
    # loop through files/raw data
    for file in os.listdir("files/raw"):

        billFileRaw = open(f"files/raw/{file}", "r")  # open file to read content
        lines = billFileRaw.readlines()
        data = []
        for line in lines:
            line = line.strip()
            line = line.split(";")
            data.append(line)
        billFileRaw.close()

        overview = data[0]
        data.pop(0)
        origin = data[0]
        data.pop(0)
        endcustomer = data[0]
        data.pop(0)
        if debug:
            print(overview)
            print(origin)
            print(endcustomer)
            print(data) 

        bill_name = overview[0]
        bill_number = bill_name.split("_")[1]

        if bill_number == "": 
            bill_number = file.replace(".data", "").replace("rechnung", "")
        #if no bill number exists do what?
        
        #create log file
        log_handler.create_log_file(bill_number)
        
#       Check for false Entries
        false_entries = False

        if len(overview) != 6: 
            log_handler.log(bill_number, 'Received corrupted data. Overview has {} entries instad of 6'.format( len(overview)))
            false_entries = True;
        if len(origin) != 8: 
            log_handler.log(bill_number, 'Received corrupted data. Origin has {} entries instad of 8'.format( len(origin)))
            false_entries = True;
        if len(endcustomer) != 5:
            log_handler.log(bill_number, 'Received corrupted data. Endcustomer has {} entries instad of 5'.format( len(endcustomer)))
            false_entries = True;
        if len(data) == 0: 
            log_handler.log(bill_number, 'Received corrupted data. Overview has 0 entries')
            false_entries = True;
        
        for entry in data:
            if len(entry) != 7:
                log_handler.log(bill_number, 'Received corrupted data. A data entry has {} entries instad of 7'.format( len(entry)))
                false_entries = True;
        
        if false_entries:
            continue;
        
        #If debug send logs to console
        log(debug, overview, origin, endcustomer, data)
        
        log_handler.log(bill_number, "Started generating txt bill for bill number: " + bill_number)
        create_txt_file(overview, origin, endcustomer, data)
        log_handler.log(bill_number, "Generated txt bill for bill number: " + bill_number)
        
        log_handler.log(bill_number, "Started generating xml bill for bill number: " + bill_number)
        create_xml_file(overview, origin, endcustomer, data)
        log_handler.log(bill_number, "Generated xml bill for bill number: " + bill_number)
        
        log_handler.log(bill_number, "Finished generating txt & xml bill for bill number: " + bill_number)
    
    return print("Finished generating all files")
    
def create_txt_file(overview, origin, endcustomer, data):

        bill_name = overview[0]
        bill_number = bill_name.split("_")[1]
        order_name = overview[1]
        order_number = order_name.split("_")[1]
        location = overview[2]
        date = overview[3]
        time = overview[4]
        pay_goal = overview[5]

        origin_number = origin[1]
        sender_number = origin[2]
        origin_name = origin[3]
        origin_address = origin[4]
        origin_postcode = origin[5]
        origin_vat_number = origin[6]
        origin_email = origin[7]

        receiver_number = endcustomer[1]
        customer_name = endcustomer[2]
        customer_address = endcustomer[3]
        customer_postcode = endcustomer[4]
        
        #Create txt file
        filePathTxtInvoice = "files/bill_txt/" + sender_number +"_"+ bill_number + "_invoice.txt"
        if debug: print("filePathTxtInvoice", filePathTxtInvoice)
        invoiceFileTxt = open(filePathTxtInvoice, "w")        
        
        #Write header
        invoiceFileTxt.write("\n\n\n\n\n")
        invoiceFileTxt.write("\n")
        invoiceFileTxt.write(origin_name + "\n")
        invoiceFileTxt.write(origin_address + "\n")
        invoiceFileTxt.write(origin_postcode + "\n")
        invoiceFileTxt.write("\n")
        invoiceFileTxt.write(origin_vat_number + "\n")
        invoiceFileTxt.write("\n\n\n\n\n")

        invoiceFileTxt.write(location + ", den " + date + "\t\t\t"+ customer_name +"\n")
        invoiceFileTxt.write("\t\t\t\t\t\t\t\t\t\t\t\t\t\t" + customer_address + "\n")
        invoiceFileTxt.write("\t\t\t\t\t\t\t\t\t\t\t\t\t\t" + customer_postcode + "\n")
        invoiceFileTxt.write("\n")

        #Write Details
        invoiceFileTxt.write("Kundennummer:\t\t" + sender_number + "\n")
        invoiceFileTxt.write("Auftragsnummer:\t\t" + order_number + "\n")
        invoiceFileTxt.write("\n")
        invoiceFileTxt.write("Rechnung Nr\t\t" + bill_number + "\n")
        invoiceFileTxt.write("-----------------------\n")
        
        full_amount = 0
        vat_amount = 0

        for d in data:
            bill_pos = d[1]
            topic = d[2]
            order_amount = d[3]
            price = d[4]
            end_sum = d[5]
            vat = remove_str(d[6], "MWST_")
            full_amount = full_amount + float(end_sum)
            vat_num = float(remove_str(vat, "%"))
            vat_amount = vat_amount + vat_num * float(end_sum) / 100
        #Generate Job Details
            invoiceFileTxt.write("  " + bill_pos + "\t\t" + topic + "\t\t\t" + order_amount + "\t\t" + price + "\t\t" + end_sum + "\t\t" + vat + "\n")
        
        full_sum = full_amount + vat_amount
        
        invoiceFileTxt.write(t(20) + "----------\n")
        invoiceFileTxt.write(t(20) + "Total CHF"+ t(6) + str(full_sum) + "\n")
        invoiceFileTxt.write("\n")
        invoiceFileTxt.write(t(20) + "MWST  CHF" + t(6) + str(vat_amount) + "\n")
        invoiceFileTxt.write("\n\n\n\n\n\n\n\n\n\n\n\n\n")
        
        #add payment goal +30 days
        pay_goal = remove_str(pay_goal, "ZahlungszielInTagen_")
        d = get_payment_day(date, pay_goal)
        
        invoiceFileTxt.write("Zahlungsziel ohne Abzug " + pay_goal +" Tage (" + d +")\n\n")
        
        #Print Einzahlungsschein
        
        invoiceFileTxt.write("Einzahlungsschein")
        invoiceFileTxt.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")  
        invoiceFileTxt.write("\t\t" + str(full_sum) + "\t\t\t\t\t\t\t\t\t\t\t\t" + str(full_sum) + "\t\t\t\t" + customer_name + "\n")  
        invoiceFileTxt.write("\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t" + customer_address + "\n")
        invoiceFileTxt.write("0 00000 00000 00000\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t" + customer_postcode + "\n")
        invoiceFileTxt.write("\n")
        invoiceFileTxt.write(customer_name + "\n")
        invoiceFileTxt.write(customer_address + "\n")
        invoiceFileTxt.write(customer_postcode + "\n")
        invoiceFileTxt.close()
        print("Invoice TXT created")

def create_xml_file(overview, origin, endcustomer, data):
    
        bill_name = overview[0]
        bill_number = bill_name.split("_")[1]
        order_name = overview[1]
        order_number = order_name.split("_")[1]
        location = overview[2]
        date = overview[3]
        time = overview[4]
        pay_goal = overview[5]

        origin_number = origin[1]
        sender_number = origin[2]
        origin_name = origin[3]
        origin_address = origin[4]
        origin_postcode = origin[5]
        origin_vat_number = origin[6]
        origin_email = origin[7]

        receiver_number = endcustomer[1]
        customer_name = endcustomer[2]
        customer_address = endcustomer[3]
        customer_postcode = endcustomer[4]

        filePathXmlInvoice = "files/bill_xml/" + sender_number +"_"+ bill_number + "_invoice.xml"
        invoiceFileXml = open(filePathXmlInvoice, "w")
        if debug: print("filePathXmlInvoice", filePathXmlInvoice)
    
        pay_goal = remove_str(pay_goal, "ZahlungszielInTagen_")
        d = get_payment_day(date, pay_goal)
        clean_date = get_clean_date(date)
        clean_payment_date = get_clean_date(d)
        date_tag = generate_xml_tag("date", clean_date)
        payment_date_tag = generate_xml_tag("date", clean_payment_date)
        
        full_amount = 0
        vat_amount = 0

        for d in data:
            order_amount = d[3]
            price = d[4]
            end_sum = d[5]
            vat = remove_str(d[6], "MWST_")
            full_amount = full_amount + float(end_sum)
            vat_num = float(remove_str(vat, "%"))
            vat_amount = vat_amount + vat_num * float(end_sum) / 100

        full_sum = full_amount + vat_amount
        
        ################################################ XML ################################################
        invoiceFileXml.write("<XML-FSCM-INVOICE-2003A>\n"+t(1)+"<INTERCHANGE>\n"+t(2)+"<IC-SENDER>\n")
        invoiceFileXml.write(t(3)+"<Pid>"+origin_number+"</Pid>\n")
        invoiceFileXml.write(t(2)+'</IC-SENDER>'+'\n'+ t(2)+'<IC-RECEIVER>\n')
        invoiceFileXml.write(t(3)+"<Pid>"+receiver_number+"</Pid>\n")
        invoiceFileXml.write(t(2)+'</IC-RECEIVER>\n'+t(2)+'<IR-Ref />\n'+t(1)+'</INTERCHANGE>\n'+t(1)+'<INVOICE>\n'+t(2)+'<HEADER>\n'+t(3)+'<FUNCTION-FLAGS>\n'+t(4)+'<Confirmation-Flag />\n'+t(4)+'<Canellation-Flag />\n'+t(3)+'</FUNCTION-FLAGS>\n'+t(3)+'<MESSAGE-REFERENCE>\n'+t(4)+'<REFERENCE-DATE>\n')
        invoiceFileXml.write(t(5)+'<Reference-No>202007164522001</Reference-No>\n')#TODO NOT LISTED
        invoiceFileXml.write(date_tag+'\n')
        invoiceFileXml.write(t(4)+'</REFERENCE-DATE>\n'+t(3)+'</MESSAGE-REFERENCE>\n'+t(3)+'<PRINT-DATE>\n')
        invoiceFileXml.write(date_tag+'\n')
        invoiceFileXml.write(t(3)+'</PRINT-DATE>\n'+t(3)+'<REFERENCE>\n'+t(4)+'<INVOICE-REFERENCE>\n'+t(5)+'<REFERENCE-DATE>\n')
        invoiceFileXml.write(t(6)+'<Reference-No>'+bill_number+'</Reference-No>\n')
        invoiceFileXml.write(date_tag+'\n')
        invoiceFileXml.write(t(5)+'</REFERENCE-DATE>\n'+t(4)+'</INVOICE-REFERENCE>\n'+t(4)+'<ORDER>\n'+t(3)+'<REFERENCE-DATE>\n')
        invoiceFileXml.write('<Reference-No>'+order_number+'</Reference-No>\n')
        invoiceFileXml.write(date_tag+'\n')
        invoiceFileXml.write('</REFERENCE-DATE>\n</ORDER>\n<REMINDER Which="MAH">\n<REFERENCE-DATE>\n<Reference-No>\n</Reference-No>\n<Date></Date>\n</REFERENCE-DATE>\n</REMINDER>\n<OTHER-REFERENCE Type="ADE">\n<REFERENCE-DATE>\n')
        invoiceFileXml.write('<Reference-No>12345678</Reference-No>\n')#TODO NOT LISTED
        invoiceFileXml.write(date_tag+'\n')
        invoiceFileXml.write('</REFERENCE-DATE>\n</OTHER-REFERENCE>\n</REFERENCE>\n<BILLER>\n')
        invoiceFileXml.write('<Tax-No>'+origin_vat_number+'</Tax-No>\n')
        invoiceFileXml.write('<Doc-Reference Type="ESR-ALT "></Doc-Reference>\n<PARTY-ID>\n')
        invoiceFileXml.write('<Pid>'+origin_number+'</Pid>\n')
        
        invoiceFileXml.write('</PARTY-ID>\n<NAME-ADDRESS Format="COM">\n<NAME>\n')
        invoiceFileXml.write('<Line-35>'+origin_name+'</Line-35>\n')
        invoiceFileXml.write('<Line-35>'+origin_address+'</Line-35>\n')
        invoiceFileXml.write('<Line-35>'+origin_postcode+'</Line-35>\n')
        invoiceFileXml.write('<Line-35></Line-35>\n<Line-35></Line-35>\n')
        
        invoiceFileXml.write('</NAME>\n')
        invoiceFileXml.write('<STREET>\n')
        invoiceFileXml.write('<Line-35></Line-35>\n')
        invoiceFileXml.write('<Line-35></Line-35>\n')
        invoiceFileXml.write('<Line-35></Line-35>\n')
        invoiceFileXml.write('</STREET>\n')
        invoiceFileXml.write('<City></City>\n')
        invoiceFileXml.write('<State></State>\n')
        invoiceFileXml.write('<Zip></Zip>\n')
        invoiceFileXml.write('<Country></Country>\n')
        invoiceFileXml.write('</NAME-ADDRESS>\n')
        invoiceFileXml.write('<BANK-INFO>\n')
        invoiceFileXml.write('<Acct-No></Acct-No>\n')
        invoiceFileXml.write('<Acct-Name></Acct-Name>\n')
        invoiceFileXml.write('<BankId Type="BCNr-nat" Country="CH">001996</BankId>\n')
        invoiceFileXml.write('</BANK-INFO>\n')
        invoiceFileXml.write('</BILLER>\n')
        
        invoiceFileXml.write('<PAYER>\n')
        invoiceFileXml.write('<PARTY-ID>\n')
        invoiceFileXml.write('<Pid>'+receiver_number+'</Pid>\n') 
        invoiceFileXml.write('</PARTY-ID>\n')
        invoiceFileXml.write('<NAME-ADDRESS Format="COM">\n')
        invoiceFileXml.write('<NAME>\n')
        invoiceFileXml.write('<Line-35>'+customer_name+'</Line-35>\n')
        invoiceFileXml.write('<Line-35>'+customer_address+'</Line-35>\n')
        invoiceFileXml.write('<Line-35>'+customer_postcode+'</Line-35>\n')
        invoiceFileXml.write('<Line-35></Line-35>\n')
        invoiceFileXml.write('<Line-35></Line-35>\n')
        invoiceFileXml.write('</NAME>\n')
        invoiceFileXml.write('<STREET>\n')
        invoiceFileXml.write('<Line-35></Line-35>\n')
        invoiceFileXml.write('<Line-35></Line-35>\n')
        invoiceFileXml.write('<Line-35></Line-35>\n')
        invoiceFileXml.write('</STREET>\n')
        invoiceFileXml.write('<City></City>\n')
        invoiceFileXml.write('<State></State>\n')
        invoiceFileXml.write('<Zip></Zip>\n')
        invoiceFileXml.write('<Country></Country>\n')
        invoiceFileXml.write('</NAME-ADDRESS>\n')
        
        invoiceFileXml.write('</PAYER>\n')
        invoiceFileXml.write('</HEADER>\n')
        invoiceFileXml.write('<LINE-ITEM />\n')
        invoiceFileXml.write('<SUMMARY>\n')
        invoiceFileXml.write('<INVOICE-AMOUNT>\n')
        long_amount = get_long_amount(full_sum)
        invoiceFileXml.write('<Amount>'+long_amount+'</Amount>\n')#FullAmount 
        invoiceFileXml.write('</INVOICE-AMOUNT>\n')
        invoiceFileXml.write('<VAT-AMOUNT>\n')
        invoiceFileXml.write('<Amount>' + str(vat_amount) + '</Amount>\n') #VAT AMOUNT HERE#TODO
        invoiceFileXml.write('</VAT-AMOUNT>\n')
        invoiceFileXml.write('<DEPOSIT-AMOUNT>\n')
        invoiceFileXml.write('<Amount></Amount>\n')
        invoiceFileXml.write('<REFERENCE-DATE>\n')
        invoiceFileXml.write('<Reference-No></Reference-No>\n')
        invoiceFileXml.write('<Date></Date>\n')
        invoiceFileXml.write('</REFERENCE-DATE>\n')
        invoiceFileXml.write('</DEPOSIT-AMOUNT>\n')
        invoiceFileXml.write('<EXTENDED-AMOUNT Type="79">\n')
        invoiceFileXml.write('<Amount></Amount>\n')
        invoiceFileXml.write('</EXTENDED-AMOUNT>\n')
        invoiceFileXml.write('<TAX>\n')
        invoiceFileXml.write('<TAX-BASIS>\n')
        invoiceFileXml.write('<Amount></Amount>\n')
        invoiceFileXml.write('</TAX-BASIS>\n')
        invoiceFileXml.write('<Rate Categorie="S">0</Rate>\n')
        invoiceFileXml.write('<Amount></Amount>\n')
        invoiceFileXml.write('</TAX>\n')
        invoiceFileXml.write('<PAYMENT-TERMS>\n')
        invoiceFileXml.write('<BASIC Payment-Type="ESR" Terms-Type="1">\n')
        invoiceFileXml.write('<TERMS>\n')
        invoiceFileXml.write('<Payment-Period Type="M" On-Or-After="1" Reference-Day="31">'+pay_goal+'</Payment-Period>\n') #PAYMENT DAY#TODO
        invoiceFileXml.write(payment_date_tag+'\n')
        invoiceFileXml.write('</TERMS>\n')
        invoiceFileXml.write('</BASIC>\n')
        invoiceFileXml.write('<DISCOUNT Terms-Type="22">\n')
        invoiceFileXml.write('<Discount-Percentage>0.0</Discount-Percentage>\n')
        invoiceFileXml.write('<TERMS>\n')
        invoiceFileXml.write('<Payment-Period Type="M" On-Or-After="1" Reference-Day="31"></Payment-Period>\n')
        invoiceFileXml.write('<Date></Date>\n')
        invoiceFileXml.write('</TERMS>\n')
        invoiceFileXml.write('<Back-Pack-Container Encode="Base64"> </Back-Pack-Container>\n')
        invoiceFileXml.write('</DISCOUNT>\n')
        invoiceFileXml.write('</PAYMENT-TERMS>\n')
        invoiceFileXml.write('</SUMMARY>\n')
        invoiceFileXml.write('</INVOICE>\n')
        invoiceFileXml.write('</XML-FSCM-INVOICE-2003A>')
        invoiceFileXml.close()
        print("Invoice XML created")
        
#Remove a specific string from a string
def remove_str(original, strToBeRemoved):
    str = original.replace(strToBeRemoved, "")
    if debug: print("NEW STRING", str)
    return str

#Calculate the new date from a specific date plus offset
def get_payment_day(date, offset):
    d = datetime.strptime(date, '%d.%m.%Y')
    d = d + timedelta(days=int(offset))
    d = d.strftime('%d.%m.%Y')
    return d

#Generate Tabs from amount
def t(amount):
    str = ""
    i = 0
    while(i < amount):
        i = i + 1
        str += "\t"
    return str

def generate_xml_tag(tag, value):
    #switch tag return tag
    
    if tag == "date": return "<Date>"+str(value)+"</Date>"
    if tag == "payment-day": return "<Payment-Day>"+str(value)+"</Payment-Day>"

def get_clean_date(date):
    d = datetime.strptime(date, '%d.%m.%Y')
    d = d.strftime('%Y%m%d')
    if debug: print("CLEAN DATE", d)
    return d
    
def get_long_amount(chf):
    chf = str(chf)
    x = chf.split(".")
    #check ig decimal [1] is 2 digits long if not make it 2 digits long
    if len(x[1]) == 1:
        x[1] = str(x[1])+"0"
    if debug: print("LONG AMOUNT", x[0]+x[1])
    chf = x[0]+x[1]
    
    length = len(chf)
    zeros_to_be_added = 10 - length
    correct_amount = ""
    i = 0
    while(i < zeros_to_be_added):
        i = i + 1
        correct_amount += "0"
        r = correct_amount+chf
    return r

def log(debug, overview, origin, endcustomer, data):
        bill_name = overview[0]
        bill_number = bill_name.split("_")[1]
        order_name = overview[1]
        order_number = order_name.split("_")[1]
        location = overview[2]
        date = overview[3]
        time = overview[4]
        pay_goal = overview[5]

        origin_number = origin[1]
        sender_number = origin[2]
        origin_name = origin[3]
        origin_address = origin[4]
        origin_postcode = origin[5]
        origin_vat_number = origin[6]
        origin_email = origin[7]

        receiver_number = endcustomer[1]
        customer_name = endcustomer[2]
        customer_address = endcustomer[3]
        customer_postcode = endcustomer[4]
        if debug:
            print("Bill Name:" + bill_name)
            print("Bill Number:" + bill_number)
            print("Order Name:" + order_name)
            print("Order Number:" + order_number)
            print("Location:" + location)
            print("Date:" + date)
            print("Time:" + time)
            print("Pay goal:" + pay_goal)

            print("Origin number:" + origin_number)
            print("Sender number:" + sender_number)
            print("Origin name:" + origin_name)
            print("Origin address:" + origin_address)
            print("Origin postcode:" + origin_postcode)
            print("Origin vat number:" + origin_vat_number)
            print("Origin vat number:" + origin_vat_number)
            print("Origin vat number:" + origin_vat_number)
            print("Origin email:" + origin_email)

            print("Receiver number:" + receiver_number)
            print("Customer name:" + customer_name)
            print("Customer address:" + customer_address)
            print("Customer postcode:" + customer_postcode)
            
            full_amount = 0
            vat_amount = 0
            
            for d in data:
                bill_pos = d[1]
                topic = d[2]
                order_amount = d[3]
                price = d[4]
                end_sum = d[5]
                vat = remove_str(d[6], "MWST_")
                full_amount = full_amount + float(end_sum)
                vat_num = float(remove_str(vat, "%"))
                vat_amount = vat_amount + vat_num * float(end_sum) / 100
            

                print("bill_pos:", bill_pos)
                print("topic:", topic)
                print("order_amount:", order_amount)
                print("price:", price)
                print("end_sum:", end_sum)
                print("vat:", vat)
                print("vat_num:", vat_num)
                
            full_sum = full_amount + vat_amount
            print("full_sum", full_sum)
            print("full_amount", full_amount)