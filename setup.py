from setuptools import setup

setup(
      name='personnummer',
      version='3.0.2',
      description='Validate Swedish personal identity numbers',
      url='http://github.com/personnummer/python',
      author='Personnummer and Contributors',
      author_email='fredrik.forsmo+personnummer@gmail.com',
      license='MIT',
      packages=['personnummer'],
      test_suite='nose.collector',
      tests_require=['nose', 'mock'],
)
