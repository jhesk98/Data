#define encrypt function and pass the filename and key through
def Encrypt(filename, key):

    #open the file and give it permisions
    #reading in byte-by-byte data to fix encoding issues
    file= open(filename, "rb" )
    data=file.read()
    file.close()

    data = bytearray(data)
    for index, value in enumerate(data):
#access the value of the data array at whatever index im on and set it equal to
#my value and take the
    #changin the value in the data array to be whatever my value is when XOR is
    #used on the key passed in
        data[index] = value ^ key

    file = open("CC - " + filename, "wb")
    file.write(data)
    file.close()

def Decrypt(filename, key):
    file=open(filename, "rb")
    data = file.read()
    file.close()

    data = bytearray(data)
    for index, value in enumerate(data):
        data[index] = value ^ key


    file = open(filename, "wb")
    file.write(data)
    file.close()
#key to encrypt the file

choice = ""
while choice != "3":
    print("Select an option:")
    print("1. Encrypt a file.")
    print("2. Decrypt a file.")
    choice = input()
    if choice == "1" or choice == "2":
        key = int(input("Enter a key as int:\n"))
        filename = input ("Enter filename and extension of the file you want encrypted: ")
    if choice == "1":
        Encrypt(filename, key)
    if choice == "2":
        Decrypt(filename, key)