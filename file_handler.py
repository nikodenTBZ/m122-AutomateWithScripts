#Read the filecontent of the .data file split by ; into variables and print those variables into the console and save the different variables into a list
file = "./files/rechnung21003.data"

def main(filename):
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


main(file)