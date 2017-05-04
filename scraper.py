import requests
import json

s = requests.Session()
response = s.get('http://datos.chubut.gov.ar/api/3/action/package_list')

package_list = response.json()['result']

for package in package_list:
    package_data = s.get(''.join(['http://datos.chubut.gov.ar/api/3/action/package_show?id=', package]))
    recursos = package_data.json()['result']['resources']
    for recurso in recursos:
        filename = 'data/'
        if(recurso['format'].lower() in recurso['name'].lower()):
            filename += recurso['name']
        else:
            filename += ''.join([recurso['name'], '.', recurso['format'].lower()])
        r = s.get(recurso['url'])
        with open(filename, 'xb')  as f:
            for chunk in r.iter_content(chunk_size=512*1024):
                if chunk:
                    f.write(chunk)
