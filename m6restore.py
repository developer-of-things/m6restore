import telnetlib
import time
import re
import sierrakeygen2
import luhn
import sys

HOST = "192.168.1.1"
PORT = 5510
TIMEOUT = 3

# Verify supplied IMEI is valid
newimei = sys.argv[1]
if len(sys.argv) > 2 and re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', sys.argv[2]):
    HOST = sys.argv[2]

imeiverification = luhn.verify(newimei)

if imeiverification is False:
    print('Not a valid IMEI Number!')
    sys.exit()

# Connect to device
tn = telnetlib.Telnet(HOST, PORT, TIMEOUT)

# Function to read and print the response after a command
def read_response():
    time.sleep(10)
    response = tn.read_very_eager().decode('utf-8')
    print(response)
    return response

# Grab some information about the device
tn.write(b"ATI\r\n")
atiresponse = read_response()
print("ATI Response: " + atiresponse)

# Grab the starting IMEI
imeipattern = r"\r\nIMEI: (.*?)\r\nIMEI SV:"
imei = re.search(imeipattern, atiresponse).group(1)
print("Device Current IMEI: " + imei)

# Grab the openlock hash
tn.write(b"AT!OPENLOCK?\r\n")
openlockresponse = read_response()
print("Open Lock Response: " + openlockresponse)

# Parse the response to a challenge
challenge = openlockresponse[15:-8]
print("Open Lock Challenge: " + challenge)

# Keygen openlock hash
keygen = sierrakeygen2.SierraGenerator()
devicegeneration = "SDX65"
resp = keygen.run(devicegeneration, challenge, 0)
print("Key Generator Response: " + resp)

# Send the openlock hash
print("Disabling Open Lock")
openlockwrite = "AT!OPENLOCK=\"" + resp + "\"\r\n"
tn.write(openlockwrite.encode('ascii'))
read_response()

# Unlock IMEI
print("Unlocking IMEI")
tn.write(b"AT!NVIMEIUNLOCK\r\n")
read_response()

# Parse new IMEI with checksum
print("Updating IMEI")
fullimei = luhn.append(newimei)
encryptimei = ','.join(fullimei[i:i + 2] for i in range(0, len(fullimei), 2))
encryptimeiwrite = "AT!NVENCRYPTIMEI=" + encryptimei + "\r\n"
tn.write(encryptimeiwrite.encode('ascii'))
read_response()

print("Issuing AT!TELEN=1")
tn.write(b"AT!TELEN=1\r\n")
read_response()

print("Issuing AT!CUSTOM=\"RDENABLE\",1")
tn.write(b"AT!CUSTOM=\"RDENABLE\",1\r\n")
read_response()

print("Issuing AT!CUSTOM=\"TELNETENABLE\",1")
tn.write(b"AT!CUSTOM=\"TELNETENABLE\",1\r\n")
read_response()

# Reset router
print("IMEI Restored. Rebooting Router")
tn.write(b"AT!RESET\r\n")
read_response()

tn.close()
