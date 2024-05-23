import telnetlib
import time
import sys
import sierrakeygen2  

HOST = "192.168.1.1"
PORT = 5510
TIMEOUT = 3

# Connect to device
tn = telnetlib.Telnet(HOST, PORT, TIMEOUT)

def print_response():
    time.sleep(1)
    response = tn.read_very_eager().decode('utf-8')
    print(response)

# Function to read and print the response after a command
def read_response():
    time.sleep(1)
    response = tn.read_very_eager().decode('utf-8')
    return response

def unlockLock():
    # Grab the openlock hash
    tn.write(b"AT!OPENLOCK?\r\n")  # Send the "AT!OPENLOCK?" command to get the openlock hash
    openlockresponse = read_response()  # Read and print the response
    print("Open Lock Response: " + openlockresponse)  # Print the response with a label

    # Parse the response to a challenge
    challenge = openlockresponse[15:-8]  # Extract the challenge from the response
    print("Open Lock Challenge: " + challenge)  # Print the challenge
    # Keygen openlock hash
    keygen = sierrakeygen2.SierraGenerator()  # Create an instance of the SierraGenerator class
    devicegeneration = "SDX65"  # Set the device generation
    resp = keygen.run(devicegeneration, challenge, 0)  # Generate the key using the device generation, challenge, and 0 as arguments
    print("Key Generator Response: " + resp)  # Print the key generator response
    # Send the openlock hash
    print("Disabling Open Lock")
    openlockwrite = "AT!OPENLOCK=\"" + resp + "\"\r\n"  # Create the command to send the openlock hash
    tn.write(openlockwrite.encode('ascii'))  # Send the command
    resp=read_response()  # Read and print the response
    print(resp)
    
def unlockMep():
    # Grab the openlock hash
    tn.write(b"AT!OPENMEP?\r\n")  # Send the "AT!OPENLOCK?" command to get the openlock hash
    openlockresponse = read_response()  # Read and print the response
    print("Open OPENMEP Response: " + openlockresponse)  # Print the response with a label

    # Parse the response to a challenge
    challenge = openlockresponse[15:-8]  # Extract the challenge from the response
    print("Open Lock Challenge: " + challenge)  # Print the challenge
    # Keygen openlock hash
    keygen = sierrakeygen2.SierraGenerator()  # Create an instance of the SierraGenerator class
    devicegeneration = "SDX65"  # Set the device generation
    resp = keygen.run(devicegeneration, challenge, 1)  # Generate the key using the device generation, challenge, and 0 as arguments
    print("Key Generator Response: " + resp)  # Print the key generator response
    # Send the openlock hash
    print("Disabling Open OPENMEP")
    openlockwrite = "AT!OPENMEP=\"" + resp + "\"\r\n"  # Create the command to send the openlock hash
    tn.write(openlockwrite.encode('ascii'))  # Send the command
    resp=read_response()  # Read and print the response
    print(resp)

print("Sending command: ATI")
tn.write(b"ATI\r\n")
print_response()

unlockLock()
unlockMep()

print("Sending command: AT+CMEE=2")
tn.write(b"AT+CMEE=2\r\n")
print_response()

print("Sending command: AT!CUSTOM?")
tn.write(b"AT!CUSTOM?\r\n")
print_response()

print("Sending command AT!TELEN=1")
tn.write(b"AT!TELEN=1\r\n")
print_response()

print("Issuing AT!CUSTOM=\"RDENABLE\",1")
tn.write(b"AT!CUSTOM=\"RDENABLE\",1\r\n") 
print_response()

print("Issuing AT!CUSTOM=\"TELNETENABLE\",1")
tn.write(b"AT!CUSTOM=\"TELNETENABLE\",1\r\n") 
print_response()

# # Reboot the device to apply changes
# print("Rebooting the device")
# tn.write(b"AT!RESET\r\n")
# # print_response()


# Close the connection
tn.close()
