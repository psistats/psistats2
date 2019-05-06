from setuptools import setup, find_packages

setup(name='psistats2',
      version='0.0.1-develop',
      description='Basic computer health monitor',
      author='Alex Dow',
      author_email='adow@psikon.com',
      url='https://github.com/psistats/psistats2',
      packages=find_packages(exclude=('env')),
      entry_points = {
          'console_scripts': ['psistats2=psistats2.cli:main']
      },
      python_requires='>=3',
      classifiers = [
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Environment :: Win32',
          'Intended Audience :: Information Technology',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Topic :: System :: Monitoring'
     ]
)
