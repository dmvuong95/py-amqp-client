from setuptools import setup, find_packages

setup(
  name='skyamqp',
  version='0.0.1',
  author='Minh Vuong',
  author_email='dmvuong95@gmail.com',
  description='AMQP client connection tool for python',
  install_requires=['pika'],
  packages=['skyamqp', 'skyamqp.rpc']
)