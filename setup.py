from setuptools import setup

setup(name='personnummer',
      version='1.0.2',
      description='Validate Swedish social security numbers',
      url='http://github.com/personnummer/python',
      author='Fredrik Forsmo',
      author_email='fredrik.forsmo@gmail.com',
      license='MIT',
      packages=['personnummer'],
      test_suite='nose.collector',
      tests_require=['nose'],
)