from distutils.core import setup

setup(
    name='smart',
    version='0.0.5',
    install_requires=['flask-script>=2.0.5',
              'flask>=0.12',
              'werkzeug>=0.11.15',
              ],
    packages=['smartflask'],
    url='https://github.com/smartcundo/smartflask',
    license='',
    author='SMART',
    author_email='fnishiwaki@smarttech.com',
    description='Command and subcommand line tools for a fun DevOps World.'
)
