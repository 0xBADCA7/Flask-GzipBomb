"""
Gzip Bomb responses for Flask.

This package provides an extension to flask.Response class,
**GzipBombResponse**, which can be used as a defensive measure for various
vuln scans, dictionary attacks etc. It creates a response containing a gzipped
data block filled with null characters with varying number of rounds (to
achieve minimal size of response's content).

Example:

    >>> from flask import Flask
    >>> from flask_gzipbomb import GzipBombResponse
    >>>
    >>> app = Flask(__name__)
    >>>
    >>> @app.route('/tiny-bomb')
    ... def gzipped():
    ...     return GzipBombResponse(size='1M')
    >>>
    >>> app.run()

    >>> import gzip
    >>> import requests
    >>>
    >>> r = requests.get('http://localhost:5000/tiny-bomb')
    >>> r.headers['content-encoding']
    'gzip,gzip'
    >>> len(r.content) # gzipped content length in bytes
    64
    >>> data = gzip.decompress(r.content)
    >>> data = gzip.decompress(data)
    >>> len(data) # decompressed content length in bytes
    1048576

GzipBombResponse accepts all arguments accepted by Response class with
additional *size* parameter, describing response content length in bytes
after decompression. Possible values:

    '1k', '10k', '100k', '1M', '10M', '100M', '1G', '10G'

with k, M and G denoting kilobyte, megabyte and gigabyte. Any other value
will result raise a KeyError. By default *size* is set to '10M', however
it is recommended to use '10G' for achieving desired effect.

**This package is for protection and educational purposes only. Using it
for any malicious purpose is strictly prohibited.**
"""
from flask import Response
from ._rawdata import rawdata


__version__ = '0.1.0'


class GzipBombResponse(Response):
    """Response containing GzipBomb."""

    #: Accaptable content sizes (rounds, data)
    _gzipData = {
        #: 1 kB
        '1k':   (1, rawdata['1k']),
        #: 10 kB
        '10k':  (1, rawdata['10k']),
        #: 100 kB
        '100k': (2, rawdata['100k']),
        #: 1 MB
        '1M':   (2, rawdata['1M']),
        #: 10 MB
        '10M':  (2, rawdata['10M']),
        #: 100 MB
        '100M': (3, rawdata['100M']),
        #: 1 GB
        '1G':   (3, rawdata['1G']),
        #: 10 GB
        '10G':  (4, rawdata['10G']),
    }

    def __init__(self, *args, **kwargs):
        """
        GzipBombResponse initializer.

        Accepts the same arguments as flask.Response class with the
        addition of *size* parameter with predefined possible values:

            '1k', '10k', '100k', '1M', '10M', '100M', '1G', '10G'

        with *k*, *M* and *G* denoting kilobyte, megabyte and gigabyte.
        Passing any other value will raise a KeyError.
        """
        size = kwargs.pop('size', '10M')

        super(Response, self).__init__(*args, **kwargs)
        self.size = size

    @property
    def size(self):
        """Get decompressed content size."""
        return self._size

    @size.setter
    def size(self, size):
        """Set decompressed content size."""
        self._size = size

        rounds, self.data = self._gzipData[self._size]

        self.headers['Content-Encoding'] = ','.join(['gzip'] * rounds)
        self.headers['Content-Length'] = len(self.data)
