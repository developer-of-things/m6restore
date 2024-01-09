#!/bin/bash

echo "Please ensure that the Nighthawk is unplugged before starting the script to allow for the installation of dependencies."
read -p "'y' or 'yes' to continue"$'\n'"" UNPLUG_CONFIRM
if [ "$UNPLUG_CONFIRM" = "y" ] || [ "$UNPLUG_CONFIRM" = "yes" ]; then
    echo "Proceeding with the script..."
fi


# Check for Homebrew, install if we don't have it
if test ! $(which brew); then
  echo "Installing homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  (echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/admin/.zprofile
  eval "$(/opt/homebrew/bin/brew shellenv)"
else
    echo "Brew Already Installed!"
fi

# Update homebrew recipes
brew update

# Install nmap and telnet
if test ! $(which nmap); then
    echo "Installing nmap..."
    brew install nmap 
else
    echo "nmap Already Installed!"
fi
if test ! $(which telnet); then
    brew install telnet
else
    echo "telnet Already Installed!"
fi

# Setup python virtual environment
python3 -m venv myVEnv

# Activate virtual environment
source myVEnv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "1) Time to remove SIM card if not already done."
echo "2) Enable USB tethering."
echo "3) Plug-in USB to Nighthawk"
# SIM card removal warning before proceeding
SIM_WARN=""
while [ "$SIM_WARN" != "y" ] && [ "$SIM_WARN" != "yes" ]; do
    read -p "1) Make sure SIM card is removed from Nighthawk before proceeding and that the Nighthawk is connected via USB with USB tethering enabled"$'\n'"'y' or 'yes' to continue"$'\n'"" SIM_WARN
    if [ "$SIM_WARN" = "y" ] || [ "$SIM_WARN" = "yes" ]; then
        echo "WARNING: Proceeding to IMEI validation. Ensure that SIM card is removed to avoid any issues."
    else
        echo "Please confirm that the SIM card is removed and try again."
    fi
done

# Perform an arp scan and grep for "mywebui.net" to retrieve the IP address
ip_address=""
while [ -z "$ip_address" ]; do
    arp_scan_output=$(arp -a | grep "mywebui.net")
    ip_address=$(echo $arp_scan_output | awk '{print $2}' | sed 's/[()]//g')
    if [ -n "$ip_address" ]; then
        echo "IP address retrieved: $ip_address"
        if [ "$ip_address" = "192.168.1.1" ]; then
            echo "IP address is $ip_address. We are ok to proceed."
        else
            echo "IP address is $ip_address. The m6restore.py should be updated to reflect actual IP address before continuing."
        fi
    else
        read -p "Failed to retrieve IP address. If device was just connected it might take a few seconds to recognize"$'\n'"Would you like to try again? "$'\n'"(y/n) y to try again n to exit script: " retry
        if [ "$retry" != "y" ] && [ "$retry" != "yes" ]; then
            break
        fi
    fi
done

# Validate IMEI number to avoid writting a bad IMEI
imei=""
while [ -z "$imei" ]; do
  read -p "Enter IMEI number: " input
  if python validate_imei.py "$input" >/dev/null 2>&1; then
    imei=$input
    echo "IMEI number is valid."
  else
    echo "IMEI number failed validation. Please try again."
  fi
done

python m6restore.py $imei $ip_address

reboot_confirm=""
while [ "$reboot_confirm" != "y" ] && [ "$reboot_confirm" != "yes" ]; do
    read -p "Please confirm that the device has \"fully\" rebooted. Then press 'y' or 'yes' to continue: " reboot_confirm
    if [ "$reboot_confirm" = "y" ] || [ "$reboot_confirm" = "yes" ]; then
        echo "Proceeding with the next steps."
    else
        echo "Please confirm that the device has fully rebooted and try again."
    fi
done


if [ -z "$ip_address" ]; then
    echo "No IP address found. Exiting script."
    exit 1
fi

# echo "Running sudo nmap, will require user password"
# port_check=$(sudo nmap $ip_address | grep "23")
# if [ -z "$port_check" ]; then
#     echo "Port 23 not found in nmap scan.  Port can be checked with command: sudo nmap <ip-address>"$'\n'"Proceeding anyway incase of false reading"
#     exit 1
# else
#     echo "Port 23 is open, proceeding with telnet."
# fi

setupTtl() {
    nc $ip_address 8888 < scripts/set-ttl.sh
}

(sleep 2; setupTtl)&

setupTtlService(){
    nc $ip_address 8889 < scripts/set-ttl.service
}

(sleep 6; setupTtlService)&

expect scripts/tn_script.exp

echo "Setup APN using instructions in YouTube Video and apn_builder.html"
echo "Disconnect Nighthawk to watch video or have connected to establish telnet connection for APN edits"
open apn_builder.html



