
from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
  name="cmdfns",
  packages=["cmdfns"],
  package_data={"cmdfns": ["py.typed"]},
  version="0.3.0",
  license="MIT",
  description="Make Python functions callable from the command-line",
  long_description=long_description,
  long_description_content_type="text/markdown",
  author="Marc Hull",
  author_email="aozine@gmail.com",
  url="https://github.com/aozine/cmdfns",
  keywords=["command-line"],
  python_requires=">=3.7",
  install_requires=[],
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
  ],
)
