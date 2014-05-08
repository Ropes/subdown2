from __future__ import print_function, unicode_literals

import unittest
import os

from subdown2 import memegrab

base_resources = '{}/subdown2/test/resources/'.format(os.getcwd())

class MemeGrabTest(unittest.TestCase):
    jake = 'http://www.quickmeme.com/meme/6n0y/'
    jake_html_path = 'test/resources/jake.html'

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get(self): 
       txt = memegrab.read_url(self.jake)
       self.assertGreater(len(txt), 500)

    def test_image_parsing(self):
        with open('{}{}'.format(base_resources, 'jake.html'), 'r') as fd:
            html = fd.read()
            img_meta = memegrab.img_details(html)
            found = ('http://s2.quickmeme.com/img/fd/fd3d970c53aa6ae1dfdda0c2aa7c344c883bf5455bf924fdb6e3d8b1f4983385.jpg', 'sucking at something  is the first step to becoming sorta good at something')
            self.assertEqual(img_meta[0], found[0])
            self.assertEqual(img_meta[1], found[1])


                
