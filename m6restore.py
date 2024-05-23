import telnetlib  # Import the telnetlib module for telnet communication
import time  # Import the time module for delays
import re  # Import the re module for regular expressions
import sierrakeygen2  # Import the sierrakeygen2 module for key generation
import luhn  # Import the luhn module for IMEI validation
import sys  # Import the sys module for command line arguments

HOST = "192.168.1.3"  # IP address of the device to connect to
PORT = 5510  # Port number for telnet communication
TIMEOUT = 3  # Timeout value for telnet connection

# Verify supplied IMEI is valid
newimei = sys.argv[1]  # Get the new IMEI from command line arguments
if len(sys.argv) > 2 and re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', sys.argv[2]):
    HOST = sys.argv[2]  # If a second command line argument is provided and it matches an IP address pattern, update the HOST variable

imeiverification = luhn.verify(newimei)  # Validate the new IMEI using the luhn module

if imeiverification is False:
    print('Not a valid IMEI Number!')  # If the new IMEI is not valid, print an error message
    sys.exit()  # Exit the program

# Connect to device
tn = telnetlib.Telnet(HOST, PORT, TIMEOUT)  # Create a telnet connection to the device

# Function to read and print the response after a command
def read_response():
    time.sleep(10)  # Delay for 10 seconds to allow time for the response
    response = tn.read_very_eager().decode('utf-8')  # Read the response from the telnet connection and decode it
    return response  # Return the response



# Grab some information about the device
tn.write(b"ATI\r\n")  # Send the "ATI" command to get device information
read_response()  # Read and print the response

# Grab the starting IMEI
imeipattern = r"\r\nIMEI: (.*?)\r\nIMEI SV:"  # Define a regular expression pattern to extract the IMEI from the response
imei = re.search(imeipattern, atiresponse).group(1)  # Use the regular expression pattern to extract the IMEI
print("Device Current IMEI: " + imei)  # Print the current IMEI

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


# Grab some information about the device
print("AT+CMEE=2")  
tn.write(b"AT+CMEE=2\r\n")  
read_response()  


# Send the openlock hash
print("Disabling Open Lock")
openlockwrite = "AT!OPENLOCK=\"" + resp + "\"\r\n"  # Create the command to send the openlock hash
tn.write(openlockwrite.encode('ascii'))  # Send the command
read_response()  # Read and print the response

# Unlock IMEI
print("Unlocking IMEI")
tn.write(b"AT!NVIMEIUNLOCK\r\n")  # Send the "AT!NVIMEIUNLOCK" command to unlock the IMEI
read_response()  # Read and print the response

# Parse new IMEI with checksum
print("Updating IMEI")
fullimei = luhn.append(newimei)  # Append the checksum to the new IMEI using the luhn module
encryptimei = ','.join(fullimei[i:i + 2] for i in range(0, len(fullimei), 2))  # Split the IMEI into pairs of characters separated by commas
encryptimeiwrite = "AT!NVENCRYPTIMEI=" + encryptimei + "\r\n"  # Create the command to update the IMEI
tn.write(encryptimeiwrite.encode('ascii'))  # Send the command
read_response()  # Read and print the response

print("Issuing AT!TELEN=1")
tn.write(b"AT!TELEN=1\r\n")  # Send the "AT!TELEN=1" command
read_response()  # Read and print the response

print("Issuing AT!CUSTOM=\"RDENABLE\",1")
tn.write(b"AT!CUSTOM=\"RDENABLE\",1\r\n")  # Send the "AT!CUSTOM=\"RDENABLE\",1" command
read_response()  # Read and print the response

print("Issuing AT!CUSTOM=\"TELNETENABLE\",1")
tn.write(b"AT!CUSTOM=\"TELNETENABLE\",1\r\n")  # Send the "AT!CUSTOM=\"TELNETENABLE\",1" command
read_response()  # Read and print the response

# Reset router
print("IMEI Restored. Rebooting Router")
# tn.write(b"AT!RESET\r\n")  # Send the "AT!RESET" command to reboot the router
# read_response()  # Read and print the response

tn.close()  # Close the telnet connection
