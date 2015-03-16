News grabber
============

*Note: This is work in progress, but usable*

Fetches meta-data for Norwegian news articles.


## Requirements

   apt-get install python-lxml

Or use pip:

   pip install lxml


## Usage

    from newsgrab import get_metadata
    print get_metadata (url)


## Howto add a new parser

Use the `probe.py` script to check which OpenGraph features are supported:

    $ ./probe.py <url>

If you see `datePublished` then you are lucky, 'cause almost no manual
work is required.

1. Create `parsers/<example_no>.py`

<!--
XXX: Make probe.py tell if it got all data. Then don't need parser.
-->

If you are lucky, this is enough:

    from . import OpenGraphParser
    class Parser (OpenGraphParser):
        pass

2. Add a test url to `test-urls`

3. Add a test method to `tests.py`

4. `make tests`

Step 2-4 is only needed to detect when the parser breaks in the future;
and it will some day, so don't be lazy and skip it!
