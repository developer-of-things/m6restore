# Nighthawk M6 Tutorial

<aside>
📄 This is a fork of the M5 Restore utility modified to support the M6 series.

</aside>

<aside>
❗ WARNING: I take no responsibility for what you do with this utility.

</aside>

Clone repository

```bash
git clone https://github.com/developer-of-things/m6restore
```

Get an IMEI number available 

> Have an IMEI that you know is not / won’t be used already
> IMEI should be of a 5G device that is supported on the carrier you are using

Install homebrew at brew.sh

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Install Telnet & nmap

```bash
brew install telnet nmap
```

```bash
python3 -m venv myVEnv
source myVEnv/bin/activate
pip install -r requirements.txt
```

<aside>
💡 Remove SIM card
Plug device into computer

</aside>

```bash
sudo nmap 192.168.1.1
```

Should see:

> PORT     STATE SERVICE
> 53/tcp   open  domain
> 80/tcp   open  http
> 5510/tcp open  secureidprop

M6 Restore

```bash
python m6restore.py <IMEI Number Here>
```

<aside>
💡 Device will restart, wait for restart to go on to next steps

</aside>

Should see:

> PORT     STATE SERVICE
> 23/tcp open telnet
> 53/tcp   open  domain
> 80/tcp   open  http
> 5510/tcp open  secureidprop

Telnet connect to device

```bash
telnet 192.168.1.1 23
```

Create script file

```bash
touch /usr/sbin/set-ttl.sh
chmod +x /usr/sbin/set-ttl.sh
vi /usr/sbin/set-ttl.sh
```

Add contents of script

```bash
#!/bin/bash
#!/usr/bin/env bash

iptables -t mangle -I POSTROUTING -j TTL --ttl-set 64
iptables -t mangle -I PREROUTING -j TTL --ttl-set 64
```

Create service at this location

/etc/systemd/system/set-ttl.service

```bash
[Unit]
Description=Set TTL in mangle iptables
After=multi-user.target

[Service]
ExecStart=/usr/sbin/set-ttl.sh
Type=simple

[Install]
WantedBy=multi-user.target
```

Enable script

> setenforce 0  \\ sets mode to permissive
> setenforce 1 \\ sets mode to enforcing
> getenforce \\ displays mode

Setting permissive mode is temporary and is only needed to make changes to processes.  It can be switched back after changes are made or will be set back once device reboots

start will start the service
enable will create sim link in /etc/systemd/system and will be called on boot

> 

```bash
setenforce 0

systemctl daemon-reload

systemctl start set-ttl

systemctl status set-ttl

systemctl enable set-ttl

systemctl list-unit-files | grep ttl
```

Validate that service is running

> Validate that service is running

```bash
iptables -t mangle -L POSTROUTING
iptables -t mangle -L PREROUTING
```

Configure APN

```bash
vi ./mnt/userrw/ntgnv/apns.xml
```

Example APN:

<aside>
💡 This APN will be specific to your SIM card and which APN it is meant to work with.  Generally you will change your APN by adding ‘dun’ to APN type
   I have added an example apns.xml file in this repository for some common carriers
</aside>

```bash
<apn pid="apn-1" carrier="ATT NR Broadband" mcc="310" mnc="280" apn="nrbroadband" type="default,supl,dun,mms,fota" protocol="IPV4V6" mvno_type="gid" mvno_match_data="S" />
<apn pid="apn-2" carrier="ATT Enhancedphone" mcc="310" mnc="280" apn="enhancedphone" type="default,supl,dun,mms,fota" protocol="IPV4V6" />
<!-- I'm not sure which part of the simplification would cause Cricket's APN to malfunction, so I'm writing down the version that works for me properly here. -->
<!-- Additionally, after booting up, one might need to manually toggle the airplane mode or switch the APN once to register on the network. The reason for this is unclear. -->
<apn pid="apn-3" carrier="Cricket internet" carrier_id = "10029" apn="endo" type="default,mms,supl,fota" mmsc="http://mmsc.aiowireless.net" mmsproxy="proxy.aiowireless.net" mmsport="80" protocol="IPV4V6" roaming_protocol="IPV4V6" user_editable="true" />
```

Default APN used by Android can be found at:

[etc/apns-full-conf.xml - device/sample - Git at Google](https://android.googlesource.com/device/sample/+/refs/heads/main/etc/apns-full-conf.xml)

reboot 

<aside>
💡 You can now insert your SIM card & select your APN in the admin panel
Now the IMEI, APN, and TTL service are setup and running
All data will be considered phone data and not hotspot

</aside>

<aside>
⚠️ If Device updates you will need to do this process again

</aside>

<aside>
📣 Shoutouts: MOB, HCH, tophat, techn0_logic, jouser, kf.
B.Kerler for the sierrakeygen code.

</aside>