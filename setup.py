from distutils.core import setup

setup(
    name='smart',
    version='0.0.1',
    requires=['Flask-Script>=2.0.5',
              'Flask>=0.12',
              'werkzeug>=0.11.15',],
    packages=['smartflask'],
    url='https://github.com/smartcundo/smartflask',
    license='',
    author='SMART',
    author_email='fnishiwaki@smarttech.com',
    description='Command and subcommand line tools for a fun DevOps World.'
)
