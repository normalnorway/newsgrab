import os
import argparse
from urlparse import urlsplit
from urllib import urlretrieve
from driver import domain_to_pyid as domain_to_pyton_id
from driver import load_parser
from __init__ import get_metadata_as_json

# @todo fix so don't have to be run for current directory
# @todo fix so this can be imported and used from tests.py

#import locale
#locale.setlocale (locale.LC_TIME, 'nb_NO.utf8')

# Arguments
argp = argparse.ArgumentParser (description='Download and build test data.')
argp.add_argument ('-f', '--full', action='store_true', default=False,
                   help='don\'t only download non-existing data')
args = argp.parse_args()
del argp


BASE = os.path.dirname (__file__)
datadir = os.path.join (BASE, 'testdata')
if not os.path.exists (datadir):
    os.mkdir (datadir)


with open('test-urls') as fp:
    urls = fp.readlines()
    urls = map (str.strip, urls)

for url in urls:
    urlobj = urlsplit (url)
    pyid = domain_to_pyton_id (urlobj.hostname)
    filebase = 'testdata/' + pyid
    htmlname = filebase + '.html'
    jsonname = filebase + '.json'

    # q: what about jsonname?
    if not args.full and os.path.exists (htmlname):
        print 'Skipping: %s.{html,json}' % filebase
        continue
    else:
        print 'Creating: %s.{html,json}' % filebase

    urlretrieve (url, htmlname) # @todo better to read into string
    with open(htmlname) as fp:
        htmldata = fp.read()

    parser = load_parser (pyid)()
    parser.set_html (htmldata)
    with open(jsonname, 'w') as fp:
        fp.write (parser.get_json())
