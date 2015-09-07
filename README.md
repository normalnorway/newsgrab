Norwegian news grabber
======================

[![Code Health](https://landscape.io/github/normalnorway/normal.no/master/landscape.svg?style=flat)](https://landscape.io/github/normalnorway/normal.no/master)
[![Build Status](https://travis-ci.org/normalnorway/normal.no.svg?branch=master)](https://travis-ci.org/normalnorway/normal.no)

*Note: This is work in progress, but usable.*

Fetches meta-data for Norwegian news articles. It uses a combination of
an OpenGraph parser and manual scraping using xpath (python-lxml).


## Example

    $ /cli.py http://www.aftenposten.no/nyheter/uriks/The-New-York-Times-krever-cannabislegalisering-i-hele-USA-7649727.html

    DATE    2014-07-27 10:59:00
    TITLE   The New York Times krever cannabislegalisering i hele USA
    URL     http://www.aftenposten.no/share/article-7649727.html
    IMAGE   http://ap.mnocdn.no/incoming/article7632698.ece/ALTERNATES/w480c169/afp000742852.jpg?updated=090720141324

    SUMMARY:
    Den amerikanske storavisen tar i bruk storsleggen på lederplass. De
    mener konsekvensene av forbudet er «rasistisk».


## Usage

```python
from newsgrab import get_metadata, get_metadata_as_json
print get_metadata (url)            # dict
print get_metadata_as_json (url)    # str
```


## Howto add a new parser

Use the `probe.py` script to check which OpenGraph features are supported:

    $ ./probe.py <url>

If you see `datePublished` then you are lucky, because almost no manual
work is required.

1. Create `newsgrab/parsers/<example_no>.py`

```python
# If you are lucky, this is enough:
from . import OpenGraphParser
class Parser (OpenGraphParser):
    pass
```

(And in this simple case a custom parser is not needed, since the
default is to try `OpenGraphParser`.)

2. Add a test url to `urls_to_test` in `tests.py`

3. `python tests.py init`

4. `python tests.py -v`

5. Commit your changes:
   `git add newsgrab/parser/<example_no>.py`
   `git add fixture/<example_no>.json`
   `git commit -m 'new parser: <example_no>`
   `git push`

```bash
git add newsgrab/parser/<example_no>.py
git add fixture/<example_no>.json
git commit -m 'new parser: <example_no>
git push
```

Step 2-4 is only needed to detect when the parser breaks in the future;
and it will some day, so don't be lazy and skip it!
