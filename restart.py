#!/usr/bin/env python3

import concurrent.futures, glob, json, os, re

def exec_ipynb(filename_or_url):
    nb = (requests.get(filename_or_url).json() if re.match(r'https?:', filename_or_url) else json.load(open(filename_or_url)))
    if(nb['nbformat'] >= 4):
        src = [''.join(cell['source']) for cell in nb['cells'] if cell['cell_type'] == 'code']
    else:
        src = [''.join(cell['input']) for cell in nb['worksheets'][0]['cells'] if cell['cell_type'] == 'code']
    exec('\n'.join(src), globals())


os.chdir(os.path.dirname(__file__))
exec_ipynb('python-utils/utils.ipynb')
exec(open('python-utils/config-utils.py').read(), globals())

for service in get_services():
    subprocess_check('systemctl restart %s' % service, verbose=True)
