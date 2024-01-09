import pexpect
import sys

# Default IP address
ip_address = '192.168.1.1'

# Check if any argument is passed
if len(sys.argv) > 1:
    ip_address = sys.argv[1]

child = pexpect.spawn(f'telnet {ip_address} 23')

child.expect('#')
child.sendline('ls -l')
child.expect('#')
child.sendline('rm /usr/sbin/set-ttl.sh')
child.expect('/ # ')
child.sendline('touch /usr/sbin/set-ttl.sh')
child.expect('/ # ')
child.sendline('cd /usr/sbin/')
child.expect('#')
child.sendline('pwd')
child.expect('#')
child.sendline('nc -l -p 8888 -w 100000 > set-ttl.sh')
child.expect('#')
child.sendline('chmod +x /usr/sbin/set-ttl.sh')
child.expect('#')
child.sendline('rm /etc/systemd/system/set-ttl.service')
child.expect('# ')
child.sendline('touch /etc/systemd/system/set-ttl.service')
child.expect('# ')
child.sendline('cd /etc/systemd/system')
child.expect('#')
child.sendline('pwd')
child.expect('#')
child.sendline('nc -l -p 8889 -w 100000 > set-ttl.service')
child.expect('#')
child.sendline('setenforce 0')
child.expect('#')
child.sendline('systemctl daemon-reload')
child.expect('#')
child.sendline('systemctl start set-ttl')
child.expect('#')
child.sendline('systemctl status set-ttl')
child.expect('#')
child.sendline('systemctl enable set-ttl')
child.expect('#')
child.sendline('systemctl list-unit-files | grep ttl')
child.expect('#')
child.sendline('iptables -t mangle -L POSTROUTING')
child.expect('#')
child.sendline('iptables -t mangle -L PREROUTING')
child.expect('#')
