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
    if (options.server and options.repository and options.username
            and options.password):
        new_server = {
            options.server: {
                'repository': options.repository,
                'username': options.username,
                'password': options.password
            }
        }
        myrc.servers = new_server
        myrc.save()
    else:
        if myrc.servers:
            pprint.pprint(myrc.servers)
        else:
            print 'Empty!'


if __name__ == '__main__':
    sys.exit(main())
