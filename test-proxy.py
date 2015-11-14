#!/usr/bin/python

import argparse
import re
import urllib2

def test_proxy(proxy_ip, proxy_port):
    proxy = urllib2.ProxyHandler({'http': '{}:{}'.format(proxy_ip, proxy_port)})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    res = urllib2.urlopen('http://http-echo.jgate.de/').read()

    ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    ips = set(re.findall(ip_regex, res))
    print 'Known IPs:', ' '.join(ips)

    ip_regex = '<h4>Client IP.*?<p>(.*?) '
    fw_regex = '<li class="header">X-Forwarded-For=(.*?)<'
    via_regex = '<li class="header">V[iI][aA]=(.*?)<'
    
    ip_res = re.search(ip_regex, res, re.MULTILINE | re.DOTALL)
    fw_res = re.search(fw_regex, res, re.MULTILINE | re.DOTALL)
    via_res = re.search(via_regex, res, re.MULTILINE | re.DOTALL)

    if ip_res:
        print 'External IP:', ip_res.group(1)

    if via_res:
        print 'VIA:', via_res.group(1)

    if fw_res:
        print 'Forwarded for:', fw_res.group(1)

def main():
    parser = argparse.ArgumentParser(description='Prints proxy info')
    parser.add_argument('ip')
    parser.add_argument('port', default='8080')

    args = parser.parse_args()

    test_proxy(args.ip, args.port)

if __name__=='__main__':
    main()
