#Read the filecontent of the .data file split by ; into variables and print those variables into the console and save the different variables into a list
fileLocation = "./files/raw/rechnung21003.data"

def generateFilesWithContent(filename):
    invoice_txt = ""
    billFileRaw = open(filename, "r") #open file to read content
    lines = billFileRaw.readlines()
    data = []
    for line in lines:
        line = line.strip()
        line = line.split(";")
        data.append(line)
        # print(line)
    billFileRaw.close()
    
    overview = data[0]
    data.pop(0)
    origin = data[0]
    data.pop(0)
    endcustomer = data[0]
    data.pop(0)
    
    print(overview)
    print(origin)
    print(endcustomer)
    print(data)
    
    # for pos in data:
    #     print(pos)
    # print(data)

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
    
    print("Bill Name:\t" + bill_name)
    print("Bill Number:\t" + bill_number)
    print("Order Name:\t" + order_name)
    print("Order Number:\t" + order_number)
    print("Location:\t" + location)
    print("Date:\t" + date)
    print("Time:\t" + time)
    print("Pay goal:\t" + pay_goal)
    
    print("Origin number:\t" + origin_number)
    print("Sender number:\t" + sender_number)
    print("Origin name:\t" + origin_name)
    print("Origin address:\t" + origin_address)
    print("Origin postcode:\t" + origin_postcode)
    print("Origin vat number:\t" + origin_vat_number)
    print("Origin email:\t" + origin_email)
    
    print("Receiver number:\t" + receiver_number)
    print("Customer name:\t" + customer_name)
    print("Customer address:\t" + customer_address)
    print("Customer postcode:\t" + customer_postcode)
    
    filePathTxtInvoice = "./files/bill_txt/" + sender_number +"_"+ bill_number + "_invoice.txt"
    filePathXmlInvoice = "./files/bill_xml/" + sender_number +"_"+ bill_number + "_invoice.xml"
    # print("filePathTxtInvoice", filePathTxtInvoice)
    # print("filePathXmlInvoice", filePathXmlInvoice)
    invoiceFileTxt = open(filePathTxtInvoice, "w")
    invoiceFileXml = open(filePathXmlInvoice, "w")
    # invoiceFileTxt = open(filePathTxtInvoice, "a", encoding='utf-8')
    # invoiceFileTxt = open(filePathXmlInvoice, "a", encoding='utf-8') 
    
    invoiceFileTxt.write("\n\n\n\n\n")
    invoiceFileTxt.write("\n")
    invoiceFileTxt.write(origin_name + "\n")
    invoiceFileTxt.write(origin_address + "\n")
    invoiceFileTxt.write(origin_postcode + "\n")
    invoiceFileTxt.write("\n")
    invoiceFileTxt.write(origin_vat_number + "\n")
    invoiceFileTxt.write("\n\n\n\n\n")

    invoiceFileTxt.write(location + ", den " + date + "\t\t\t"+ customer_name +"\n")
    invoiceFileTxt.write("\t\t\t\t\t\t\t\t" + customer_address + "\n")
    invoiceFileTxt.write("\t\t\t\t\t\t\t\t" + customer_postcode + "\n")
    invoiceFileTxt.write("\n")
    
    invoiceFileTxt.write("Kundennummer:\t" + sender_number + "\n")
    invoiceFileTxt.write("Auftragsnummer:\t" + order_number + "\n")
    invoiceFileTxt.write("\n")
    invoiceFileTxt.write("Rechnung Nr\t" + bill_number + "\n")
    invoiceFileTxt.write("-----------------------\n")
    
    for d in data:
        bill_pos = d[1]
        topic = d[2]
        order_amount = d[3]
        price = d[4]
        end_sum = d[5]
        vat = d[6]
        
        print("bill_pos:\t", bill_pos)
        print("topic:\t\t", topic)
        print("order_amount:\t", order_amount)
        print("price:\t\t", price)
        print("end_sum:\t", end_sum)
        print("vat:\t\t", vat)
        
        invoiceFileTxt.write("  " + bill_pos + "\t" + topic + "\t\t" + order_amount + "\t\t" + price + "\t\t" + end_sum + "\t\t" + vat + "\n")
            
    invoiceFileTxt.write("\n\n\n\n\n\n\n\n\n\n-----------")
    invoiceFileTxt.close()
    
# def readFile(filepath):
#     f = open(filepath, "r")
#     print(f.read())  
#     f.close()