import nmap

def scan_network(ip_rage):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_rage, arguments='-P 1-65535 -sS -T4') # Scan all ports
    for host in nm.all_hosts():
        print('Host: %s (%s)' % (host, nm[host].hostname()))
        print('State: %s' % nm[host].state())
        for proto in nm[host].all_protocols():
            print('Protocol: %s' % proto)
            lport = nm[host][proto].keys()
            for port in lport:
                print('port: %s\tstate: %s' % (port, nm[host][proto][port]['state']))
                
# IP range to scan. ex: '192.168.1.0/24'
ip_range = input('Enter the IP range to scan: ')

if __name__ == '__main__':
    scan_network(ip_range)