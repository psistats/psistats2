from setuptools import setup, find_packages
import py2exe


setup(name='psistats2',
      version='0.0.1-develop',
      description='Basic computer health monitor',
      author='Alex Dow',
      author_email='adow@psikon.com',
      url='https://github.com/psistats/psistats2',
      packages=find_packages(exclude=('env')),
      console=['psistats.py']
)
