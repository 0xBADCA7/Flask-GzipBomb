"""
Gzip Bomb responses for Flask.

This package provides an extension to Response class, **GzipBombResponse**,
which can be used as a defensive measure for various vuln scanners, dictionary
attacks etc. It creates a response containing a gzipped stream of zeroes with
varying number of rounds (to achieve minimal size of response's content).

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

    class _GzipData(object):
        """
        Helper class for GzipBombResponse.

        Contains raw gzipped data and number of compression rounds.
        """

        def __init__(self, rounds, data):
            self.rounds = rounds
            self.data = data

    #: Accaptable content sizes
    _gzipData = {
        #: 1 kB
        '1k':   _GzipData(rounds=1, data=rawdata['1k']),
        #: 10 kB
        '10k':  _GzipData(rounds=1, data=rawdata['10k']),
        #: 100 kB
        '100k': _GzipData(rounds=2, data=rawdata['100k']),
        #: 1 MB
        '1M':   _GzipData(rounds=2, data=rawdata['1M']),
        #: 10 MB
        '10M':  _GzipData(rounds=2, data=rawdata['10M']),
        #: 100 MB
        '100M': _GzipData(rounds=3, data=rawdata['100M']),
        #: 1 GB
        '1G':   _GzipData(rounds=3, data=rawdata['1G']),
        #: 10 GB
        '10G':  _GzipData(rounds=4, data=rawdata['10G']),
    }

    def __init__(self, *args, **kwargs):
        """
        GzipBombResponse initializer.

        Accepts the same arguments as Flask.Response class with the
        addition of *size* parameter with predefined possible values:

            '1k', '10k', '100k', '1M', '10M', '100M', '1G', '10G'

        with *k*, *M* and *G* denoting kilobyte, megabyte and gigabyte.
        Passing any other value will raise a KeyError.
        """
        size = kwargs.pop('size', '10M')
        super(Response, self).__init__(*args, **kwargs)

        gzip = self._gzipData[size]
        self.data = gzip.data

        self.headers['Content-Encoding'] = ','.join(['gzip'] * gzip.rounds)
        self.headers['Content-Length'] = len(self.data)
