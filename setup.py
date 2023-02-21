from setuptools import setup

setup(
    name='personnummer',
    version='3.0.3',
    description='Validate Swedish personal identity numbers',
    url='http://github.com/personnummer/python',
    author='Personnummer and Contributors',
    author_email='hello@personnummer.dev',
    license='MIT',
    packages=['personnummer'],
    test_suite='nose.collector',
    tests_require=['nose', 'mock'],
    entry_points = {
        'console_scripts' : ['personnummer = personnummer.main:main']
        },
)
