from setuptools import setup, find_packages
from skyamqp import __version__ as skyamqp_version
with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()

setup(
  name='skyamqp',
  version=skyamqp_version,
  author='Minh Vuong',
  author_email='dmvuong95@gmail.com',
  description='AMQP client connection tool for python',
  long_description=long_description,
  long_description_content_type="text/markdown",
  install_requires=['pika'],
  packages=['skyamqp', 'skyamqp.rpc', 'skyamqp.queue']
)
