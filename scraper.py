#!/usr/bin/env python3
import requests
import json

base_url = 'http://datos.chubut.gov.ar/api/3'
urls = {
    'package_list': ''.join([base_url, '/action/package_list']),
    'package_show': ''.join([base_url, '/action/package_show']),
}

s = requests.Session()
response = s.get(urls['package_list'])

package_list = response.json()['result']

for package in package_list:
    package_data = s.get(''.join([urls['package_show'], '?id=', package]))
    recursos = package_data.json()['result']['resources']
    for recurso in recursos:
        folder = 'data/'
        filename = ''.join([folder, recurso['name']])
        
        if(recurso['format'].lower() not in recurso['name'].lower()):
            filename = ''.join([filename, ".", recurso['format'].lower()])
        
        r = s.get(recurso['url'])
        with open(filename, 'xb') as f:
            for chunk in r.iter_content(chunk_size=512*1024):
                if chunk:
                    f.write(chunk)
