from distutils.core import setup
setup(
  name = 'cmdfns',
  packages = ['cmdfns'],
  package_data={"cmdfns": ["py.typed"]},
  version = '0.1',
  license = 'MIT',
  description = 'Make Python functions callable from the command-line',
  author = 'Marc Hull',
  author_email = 'aozine@gmail.com',
  url = 'https://github.com/aozine/cmdfns',
  download_url = 'https://github.com/Aozine/cmdfns/archive/refs/tags/v0.1.0.tar.gz',
  keywords = ['command-line'],
  install_requires=[],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.10',
  ],
)
