from driver import ParserFactory

_factory = ParserFactory()


# This is the public API. It will keep an internal cache of the parsers.
def get_metadata (url):
    parser = _factory.get (url)
    return parser.get()


def get_metadata_as_json (url):
    parser = _factory.get (url)
    return parser.get_as_json()
