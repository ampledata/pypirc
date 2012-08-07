#!/usr/bin/env python
"""PyPiRC CLI Client"""
__author__ = 'Greg Albrecht <gba@splunk.com>'
__copyright__ = 'Copyright 2012 Splunk, Inc.'
__license__ = 'Apache License 2.0'


import optparse
import pprint
import sys

import pypirc


def main():
    """Main loop."""
    parser = optparse.OptionParser()
    parser.add_option(
        '-s', '--server', help='Index Server Name', metavar='SERVER')
    parser.add_option(
        '-r', '--repository', help='Repository URL', metavar='URL')
    parser.add_option(
        '-u', '--username', help='User Name', metavar='USERNAME')
    parser.add_option(
        '-p', '--password', help='Password', metavar='PASSWORD')

    options, _ = parser.parse_args()

    myrc = pypirc.PyPiRC()
    if options.server:
        if myrc.servers:
            # we're updating
            server = myrc.servers.get(options.server, {})
        else:
            server = {}

        if options.repository:
            server['repository'] = options.repository

        if options.username:
            server['username'] = options.username

        if options.password:
            server['password'] = options.password

        myrc.servers[options.server] = server
        myrc.save()

    if myrc.servers:
        pprint.pprint(myrc.servers)
    else:
        print '.pypirc Empty!'


if __name__ == '__main__':
    sys.exit(main())
