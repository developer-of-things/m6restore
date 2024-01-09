Clone repository

```bash
git clone https://github.com/developer-of-things/m6restore
```

Change directory to the root of the project:
```bash
cd C:\Users\admin\Downloads\m6restore
```

Make script executable:
```bash
chmod +x setup\ macos.sh
```

Call the script:
```bash
./setup\ macos.sh
```
Open apn_builder.html in browser by double clicking on the file

Enter APN settings for your SIM card, these can often be found by first inserting the SIM card in an Android phone and checking the APN settings which you could enter into the form fields.
Often ',dun' is added to the end of the APN type field separated from other values by a comma.  This causes data to count as regular data instead of hotspot.

Telnet into router

```bash
telnet 192.168.1.1 23
```

Edit apns.xml file inserting your newly configured APN entries into apns element preserving other formatting using vi editor
```
vi ./mnt/userrw/ntgnv/apns.xml
```

``` xml
<?xml version="1.0"?>
<Root>
    <CmCfg>
        <DefaultAutoconnect>HomeOnly</DefaultAutoconnect>
        <DefaultProfile>apn-1</DefaultProfile>
        <ClientCfg client="0">
            <DataProfile>apn-3</DataProfile>
        </ClientCfg>
        <LteAttachProfile>apn-3</LteAttachProfile>
    </CmCfg>
    <apns version="8">
        <apn pid="apn-1" carrier="ATT NR Broadband" mcc="310" mnc="410" apn="nrbroadband" type="default,dun,supl,mms,fota" protocol="IPV4V6" mvno_type="gid" mvno_match_data="S" />
        <apn pid="apn-2" carrier="ATT Broadband" mcc="310" mnc="410" apn="broadband" type="default,dun,supl,mms,fota" protocol="IPV4V6" />
        <apn pid="apn-3" carrier="ATT nxtgenphone" mcc="310" mnc="410" apn="nxtgenphone" type="default,dun,supl,mms,fota" protocol="IPV4V6" />
        <apn pid="apn-4" carrier="Visible Legacy" mcc="310" mnc="480" apn="VSBLINTERNET" type="default,dun,supl,mms,fota" protocol="IPV4V6" mvno_type="gid"/>
        <apn pid="apn-5" carrier="Visible" mcc="310" mnc="480" apn="vzwinternet" type="default,dun,supl,mms,fota" protocol="IPV4V6" mvno_type="gid"/>
        <apn pid="apn-6" carrier="T-Mobile" mcc="310" mnc="260" apn="fast.t-mobile.com" type="default,dun,supl,mms,fota" protocol="IPv6" mvno_type="gid"/>
        <apn pid="apn-7" carrier="Verizon" mcc="310" mnc="260" apn="vzwinternet" type="default,dun,supl,mms,fota" protocol="IPv6" mvno_type="gid"/>
    </apns>
</Root>
```