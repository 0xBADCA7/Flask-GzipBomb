from setuptools import setup
from flask_gzipbomb import (
    __version__ as version,
    __doc__ as long_description
)

setup(
    name='Flask-GzipBomb',
    version=version,
    license='MIT',
    author='Piotr Kuszaj',
    author_email='peterkuszaj@gmail.com',
    description='Gzip Bomb responses for Flask',
    long_description=long_description,
    packages=['flask_gzipbomb'],
    zip_safe=False,
    include_package_data=True,
    url='https://github.com/kuszaj/Flask-GzipBomb',
    download_url='https://github.com/kuszaj/Flask-GzipBomb/archive/v%s.tar.gz' % (version,),
    platforms='any',
    install_requires=[
        'Flask',
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
