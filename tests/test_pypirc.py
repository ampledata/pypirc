#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for PyPiRC."""


import os
import random
import tempfile
import unittest

from context import pypirc


class TestPyPiRC(unittest.TestCase):
    """Tests for PyPiRC."""

    def setUp(self):
        base_fn = 'test_pypirc_'
        self.rands = ''.join(
            [random.choice('unittest0123456789') for xyz in range(8)])
        self.rand_server = {
            self.rands: {
                'repository': "http://%s.example.com" % self.rands,
                'username': "username-%s" % self.rands,
                'password': "password-%s" % self.rands,
            }
        }
        self.tmpf = tempfile.mkstemp
        self.rc_file = self.tmpf('.cfg', base_fn)[1]

    def test_add_server(self):
        """Tests adding an index-server to pypirc."""
        rc_file = self.tmpf('.cfg', 'test_add_server_')[1]
        cur_rc = pypirc.PyPiRC(rc_file)
        cur_rc.servers = self.rand_server
        self.assertTrue(cur_rc.servers == self.rand_server)

    def test_save(self):
        """Tests adding an index-server to pypirc and saving to a file."""
        rc_file = self.tmpf('.cfg', 'test_save_')[1]
        cur_rc = pypirc.PyPiRC(rc_file)
        cur_rc.servers = self.rand_server
        self.assertTrue(cur_rc.servers == self.rand_server)
        cur_rc.save()
        self.assertTrue(cur_rc.servers == self.rand_server)

    def test_add_two_servers(self):
        """Tests adding two index-servers to pypirc and saving to a file."""
        rc_file = self.tmpf('.cfg', 'test_add_two_servers_')[1]
        new_server_name = "%s_new" % self.rands
        new_server = {
            new_server_name: {
                'repository': "http://%s_new.example.com" % self.rands,
                'username': "username-%s_new" % self.rands,
                'password': "password-%s_new" % self.rands
            }
        }

        cur_rc = pypirc.PyPiRC(rc_file)
        cur_rc.servers = self.rand_server
        cur_rc.servers = new_server
        cur_rc.save()

        # Test 'new' server.
        self.assertTrue(new_server_name in cur_rc.servers)
        self.assertTrue(
            cur_rc.servers[new_server_name] == new_server[new_server_name])

        # Test existing server.
        self.assertTrue(self.rands in cur_rc.servers)
        self.assertTrue(
            cur_rc.servers[self.rands] == self.rand_server[self.rands])

    def test_existing(self):
        """Tests reading existing pypirc."""
        rc_file = self.tmpf('.cfg', 'test_existing_')[1]
        cur_rc = pypirc.PyPiRC(rc_file)
        cur_rc.servers = self.rand_server
        self.assertTrue(cur_rc.servers == self.rand_server)
        cur_rc.save()
        cur_rc2 = pypirc.PyPiRC(rc_file)
        self.assertTrue(cur_rc2.servers == self.rand_server)

    def test_update(self):
        """Tests updating existing pypirc."""
        rc_file = self.tmpf('.cfg', 'test_update_')[1]
        cur_rc = pypirc.PyPiRC(rc_file)
        cur_rc.servers = self.rand_server
        self.assertTrue(cur_rc.servers == self.rand_server)
        cur_rc.save()
        cur_rc2 = pypirc.PyPiRC(rc_file)

        updated_server = cur_rc2.servers[self.rands]
        updated_server.update({
            'repository': updated_server['repository'] + '/update'})
        cur_rc2.servers[self.rands] = updated_server

        self.assertTrue(cur_rc2.servers[self.rands] == updated_server)

    def tearDown(self):
        if os.path.exists(self.rc_file):
            os.remove(self.rc_file)


if __name__ == '__main__':
    unittest.main()
