from distutils.core import setup
setup(
  name = 'helmpythonclient',
  packages = ['helmpythonclient'],
  version = 'v1.0',
  license= 'MIT',
  description = 'An Helm 3 Python client',
  author = 'Giovanni Baggio',
  author_email = 'g.baggio@fbk.eu',
  url = 'https://github.com/joncnet/helmpythonclient',
  download_url = 'https://github.com/joncnet/helmpythonclient/archive/v_1.0.tar.gz',
  keywords = ['Helm', '3', 'Client'],
  install_requires=[],
  classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
  ],
)
