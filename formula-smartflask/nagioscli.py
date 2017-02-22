from flask_script import Manager
import os

manager = Manager(usage="Perform Nagios stuff")

create_manager = Manager(usage="Create Nagios resources")
manager.add_command("create", create_manager)


@create_manager.option('-n', '--name', dest='name', default='joe')
@create_manager.option('-c', '--clue', dest='clue', default='clue')
def hello(name, clue):
    name = name.upper()
    clue = clue.upper()
    print("hello {0}, get a {1}!".format(name, clue))


@create_manager.option('-n', '--name', dest='hostname', default='hostname')
@create_manager.option('-a', '--alias', dest='hostalias', default='alias')
@create_manager.option('-d', '--address', dest='hostaddress', default='address')
def host(hostname, hostalias, hostaddress):
    "Prints out host definition for nagios"
    print("Let's create a nagios resource!")
    output = """%s:         { hostalias: "%s",     hostaddress: %s     }""" % \
             (hostname, hostalias, hostaddress)
    print(output)

