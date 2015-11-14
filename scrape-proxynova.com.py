#!/usr/bin/python

import re
import urllib2

USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/6.0)'

def get(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', USER_AGENT)]

    data = opener.open(url).read()
    return data

def main():
    html = get('http://www.proxynova.com/proxy-server-list/')
    country_urls = re.findall('<a href="(//www.proxynova.com/proxy-server-list/country-.*?/)', html)

    for url in country_urls:
        url = 'http:{}'.format(url)
        html = get(url)
        data = re.findall('<tr>.*?class="row_proxy_ip">(.*?)</span></td>.*?/port-[0-9]+">([0-9]+)</a>.*?<span class="proxy_.*?".*?>(.*?)</span>', html, re.DOTALL | re.MULTILINE)
        for row in data:
            print ','.join(row)

if __name__=='__main__':
    main()
