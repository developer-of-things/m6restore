# # Check if the script is running as an administrator
# # Get the ID and security principal of the current user account
# $currentUser = New-Object System.Security.Principal.WindowsPrincipal([System.Security.Principal.WindowsIdentity]::GetCurrent())

# # Check if the user is an administrator
# if (-not ($currentUser.IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)))
# {
#     # Get the file path of the current script
#     $scriptPath = $MyInvocation.MyCommand.Definition

#     # Start the script again as an administrator
#     Start-Process PowerShell.exe -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`"" -Verb RunAs

#     # Exit the current script
#     exit
# }



# # Prompt user to ensure that the Nighthawk is unplugged before starting the script
# Write-Host "Please ensure that the Nighthawk is unplugged before starting the script to allow for the installation of dependencies."
# $UNPLUG_CONFIRM = Read-Host "'y' or 'yes' to continue"
# if ($UNPLUG_CONFIRM -eq "y" -or $UNPLUG_CONFIRM -eq "yes") {
#     Write-Host "Proceeding with the script..."
# }


# # TODO: Confirm that chocolatey gets installed correctly
# # Check for Chocolatey, install if we don't have it
# if (-not (Test-Path -Path "$env:ProgramData\chocolatey")) {
#     if ((Get-ChildItem -Path "$env:ProgramData\chocolatey" | Measure-Object).Count -eq 0) {
#         Remove-Item -Recurse -Force "$env:ProgramData\chocolatey"
#     }
#     Write-Host "Installing Chocolatey..."
#     Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
#     # Add Chocolatey to PATH for the current session
#     $env:Path += ";C:\ProgramData\chocolatey\bin"
# } else {
#     Write-Host "Chocolatey Already Installed!"
# }

# # Update Chocolatey packages
# & 'C:\ProgramData\chocolatey\bin\choco' upgrade all -y

# # TODO: validate that telnet and nmap work the same as in MacOS 
# # Install nmap and telnet
# Write-Host ("Check - nmap not installed: " + -not (Get-Command "C:\Program Files (x86)\Nmap\nmap.exe" -ErrorAction SilentlyContinue))

# if ( -not (Get-Command "C:\Program Files (x86)\Nmap\nmap.exe" -ErrorAction SilentlyContinue)) {
#     Write-Host "Installing nmap..."
#     & 'C:\ProgramData\chocolatey\bin\choco' install nmap -y
# } else {
#     Write-Host "nmap Already Installed!"
# }

# Write-Host ("Check - telnet not installed: " + -not (Get-Command "C:\Windows\System32\telnet.exe" -ErrorAction SilentlyContinue))
# if (-not (Get-Command telnet -ErrorAction SilentlyContinue)) {
#     & 'C:\ProgramData\chocolatey\bin\choco' install telnet -y
# } else {
#     Write-Host "telnet Already Installed!"
# }


# $pythonPath = "$env:USERPROFILE\AppData\Local\Programs\Python\Python312-arm64\python.exe"


# # TODO: Validate that python environment is activated and provides all needed dependencies
# & $pythonPath -m venv myVEnv

# # Activate virtual environment
# & .\myVEnv\Scripts\Activate.ps1

# # Install dependencies
# pip install -r requirements.txt

# Write-Host "1) Time to remove SIM card if not already done."
# Write-Host "2) Enable USB tethering."
# Write-Host "3) Plug-in USB to Nighthawk"

# # SIM card removal warning before proceeding
# $SIM_WARN = ""
# while ($SIM_WARN -ne "y" -and $SIM_WARN -ne "yes") {
#     Write-Host "1) Make sure SIM card is removed from Nighthawk before proceeding and that the Nighthawk is connected via USB with USB tethering enabled"
#     Write-Host "'y' or 'yes' to continue"
#     $SIM_WARN = Read-Host
#     if ($SIM_WARN -eq "y" -or $SIM_WARN -eq "yes") {
#         Write-Host "WARNING: Proceeding to IMEI validation. Ensure that SIM card is removed to avoid any issues."
#     } else {
#         Write-Host "Please confirm that the SIM card is removed and try again."
#     }
# }

# #TODO: Validate that string exists that can be used to retrieve IP address
# # Perform an arp scan and grep for "mywebui.net" to retrieve the IP address
# $arpTable = arp -a
# $arpTable = $arpTable | Where-Object { $_ -notmatch "255" }
# $arpTable | ForEach-Object {
    
#     if ($_ -match "\b(?:\d{1,3}\.){3}\d{1,3}\b") {
#         try {
#             $hostname = [System.Net.Dns]::GetHostEntry($Matches[0]).HostName
#             if ($hostname -eq "mywebui.net") {
#                 $ip_address = $Matches[0]
#                 Write-Host "IP address of mywebui.net: $ip_address"
#             }
#         } catch {
#             "$($Matches[0]) - Has no hostname"
#         }
#     }
# }


# Write-Host "Validate IMEI"
# # TODO: validate that success condition and error conditions are met
# # Validate IMEI number to avoid writing a bad IMEI
# $imei = ""
# while ($imei -eq "") {
#     Write-Host "Enter IMEI number: "
#     $input = Read-Host
#     python validate_imei.py $input
#     if ($LASTEXITCODE -eq 0) {
#         $imei = $input
#         Write-Host "IMEI number is valid."
#     } else {
#         Write-Host "IMEI number failed validation. Please try again."
#     }
# }

# # TODO: Validate that script completes and waits for user input
# python m6restore.py $imei $ip_address

# $reboot_confirm = ""
# while ($reboot_confirm -ne "y" -and $reboot_confirm -ne "yes") {
#     Write-Host "Please confirm that the device has 'fully' rebooted. Then press 'y' or 'yes' to continue: "
#     $reboot_confirm = Read-Host
#     if ($reboot_confirm -eq "y" -or $reboot_confirm -eq "yes") {
#         Write-Host "Proceeding with the next steps."
#     } else {
#         Write-Host "Please confirm that the device has fully rebooted and try again."
#     }
# }

# if ($ip_address -eq "") {
#     Write-Host "No IP address found. Exiting script."
#     exit
# }





function SetupTtl {
    Get-Content scripts/set-ttl.sh | ncat $ip_address 8888
}

Start-Job -ScriptBlock {
    Start-Sleep -Seconds 2
    SetupTtl
}

function SetupTtlService {
    Get-Content scripts/set-ttl.service | ncat $ip_address 8889
}

Start-Job -ScriptBlock {
    Start-Sleep -Seconds 6
    SetupTtlService
}

# Calling pexpect script
python scripts\tn_script.py $ip_address


# Write-Host "Setup APN using instructions in YouTube Video and apn_builder.html"
# Write-Host "Disconnect Nighthawk to watch video or have connected to establish telnet connection for APN edits"

# if (Test-Path "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe") {
#     Start-Process "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" "$pwd\apn_builder.html"
# } elseif (Test-Path "C:\Program Files\Mozilla Firefox\firefox.exe") {
#     Start-Process "C:\Program Files\Mozilla Firefox\firefox.exe" "$pwd\apn_builder.html"
# } elseif (Test-Path "C:\Program Files\Google\Chrome\Application\chrome.exe") {
#     Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" "$pwd\apn_builder.html"
# } else {
#     Write-Host "No supported browser found. Please manually open apn_builder.html in your web browser."
# }
