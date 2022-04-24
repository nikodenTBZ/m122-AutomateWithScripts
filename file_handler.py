#Read the filecontent of the .data file split by ; into variables and print those variables into the console and save the different variables into a list
file = "./files/raw/rechnung21003.data"

def main(filename):
    invoice_txt = ""
    file = open(filename, "r")
    lines = file.readlines()
    data = []
    for line in lines:
        line = line.strip()
        line = line.split(";")
        data.append(line)
        # print(line)
    file.close()
    
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
    
    #
    # for pos in data:
    #     print(pos)

    # print(data)
    

    bill_number = overview[0]
    order_number = overview[1]
    location = overview[2]
    date = overview[3]
    time = overview[4]
    pay_goal = overview[5]
    
    print("Bill number:\t" + bill_number)
    print("Order number:\t" + order_number)
    print("Location:\t" + location)
    print("Date:\t" + date)
    print("Time:\t" + time)
    print("Pay goal:\t" + pay_goal)
    
    origin_number = origin[1]
    sender_number = origin[2]
    origin_name = origin[3]
    origin_address = origin[4]
    origin_postcode = origin[5]
    origin_vat_number = origin[6]
    origin_email = origin[7]
    
    print("Origin number:\t" + origin_number)
    print("Sender number:\t" + sender_number)
    print("Origin name:\t" + origin_name)
    print("Origin address:\t" + origin_address)
    print("Origin postcode:\t" + origin_postcode)
    print("Origin vat number:\t" + origin_vat_number)
    print("Origin email:\t" + origin_email)
    
    receiver_number = endcustomer[1]
    customer_name = endcustomer[2]
    customer_address = endcustomer[3]
    customer_postcode = endcustomer[4]
    
    print("Receiver number:\t" + receiver_number)
    print("Customer name:\t" + customer_name)
    print("Customer adress:\t" + customer_address)
    print("Customer postcode:\t" + customer_postcode)

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
        # print(d)
        
main(file)