try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Generate diffs between multiple xunit xmlreports',
    'author': 'James McQuaid',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'jmmcquaid@yahoo.com',
    'version': '0.1',
    'install_requires': [],
    'packages': ['testreportdiffs'],
    'scripts': [],
    'name': 'test-report-diffs'
}

setup(**config)
