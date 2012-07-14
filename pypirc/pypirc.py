#!/usr/bin/env python
"""PyPi Configuration File Manager."""
__author__ = 'Greg Albrecht <gba@splunk.com>'
__copyright__ = 'Copyright 2012 Splunk, Inc.'
__license__ = 'Apache License 2.0'


import ConfigParser
import os


class PyPiRC(object):
    """
    PyPi Configuration File Manager.

    Can be used for updating ~/.pypirc file programatically.

    Example::
        >>> a = PyPiRC('doctest_pypi.cfg')
        >>> new_server = {'pypi': {'repository': 'http://pypi.example.com'}}
        >>> new_server2 = {'pypi2': {'repository': 'http://pypi2.example.com'}}
        >>> a.servers.update(new_server)
        >>> a.servers.update(new_server2)
        >>> a.save()
        >>> 'pypi' in a.servers
        True
        >>> 'pypi2' in a.servers
        True
    """

    RC_FILE = os.path.join(os.path.expanduser('~'), '.pypirc')

    def __init__(self, rc_file=None):
        if rc_file is None:
            self.rc_file = self.RC_FILE
        else:
            self.rc_file = rc_file

        self.conf = ConfigParser.ConfigParser()

        if os.path.exists(self.rc_file):
            self.conf.read(self.rc_file)

        self._create_distutils()

        self._servers = {}
        for server in self._get_index_servers():
            if self.conf.has_section(server):
                server_conf = {server: dict(self.conf.items(server))}
                self.servers.update(server_conf)

    def _create_distutils(self):
        """Creates top-level distutils stanza in pypirc."""
        if not self.conf.has_section('distutils'):
            self.conf.add_section('distutils')

    def save(self):
        """Saves pypirc file with new configuration information."""
        for server, conf in self.servers.iteritems():
            self._add_index_server()
            for conf_k, conf_v in conf.iteritems():
                if not self.conf.has_section(server):
                    self.conf.add_section(server)
                self.conf.set(server, conf_k, conf_v)

        with open(self.rc_file, 'wb') as configfile:
            self.conf.write(configfile)
        self.conf.read(self.rc_file)

    def _get_index_servers(self):
        """Gets index-servers current configured in pypirc."""
        idx_srvs = []
        if 'index-servers' in self.conf.options('distutils'):
            idx = self.conf.get('distutils', 'index-servers')
            idx_srvs = [srv.strip() for srv in idx.split('\n') if srv.strip()]
        return idx_srvs

    def _add_index_server(self):
        """Adds index-server to 'distutil's 'index-servers' param."""
        index_servers = '\n\t'.join(self.servers.keys())
        self.conf.set('distutils', 'index-servers', index_servers)

    @property
    def servers(self):
        """index-servers configured in pypirc."""
        return self._servers

    @servers.setter
    def servers(self, server):
        """Adds index-servers to pypirc."""
        self._servers.update(server)
