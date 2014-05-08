from __future__ import print_function, unicode_literals

import unittest
import os

import subdown2.memegrab

base_resources = '{}/test/resources/'.format(os.getcwd())

class MemeGrabTest(unittest.TestCase):
    jake = 'http://www.quickmeme.com/meme/6n0y/'
    jake_html_path = 'test/resources/jake.html'

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get(self): 
       txt = subdown2.memegrab.read_url(self.jake)
       self.assertGreater(len(txt), 500)

    def test_resource(self):
        with open('{}{}'.format(base_resources, 'jake.html'), 'r') as fd:
            html = fd.read()
            self.assertGreater(len(html), 500)
                
