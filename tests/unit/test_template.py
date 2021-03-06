# -*- coding: utf-8 -*-
'''
    :codeauthor: :email: `Mike Place <mp@saltstack.com>`
'''

# Import Python libs
from __future__ import absolute_import

# Import Salt Testing libs
from tests.support.unit import TestCase

# Import Salt libs
from salt import template


class TemplateTestCase(TestCase):

    render_dict = {'jinja': 'fake_jinja_func',
               'json': 'fake_json_func',
               'mako': 'fake_make_func'}

    def test_compile_template_bad_type(self):
        '''
        Test to ensure that unsupported types cannot be passed to the template compiler
        '''
        ret = template.compile_template(['1', '2', '3'], None, None, None, None)
        self.assertDictEqual(ret, {})

    def test_check_render_pipe_str(self):
        '''
        Check that all renderers specified in the pipe string are available.
        '''
        ret = template.check_render_pipe_str('jinja|json', self.render_dict, None, None)
        self.assertIn(('fake_jinja_func', ''), ret)
        self.assertIn(('fake_json_func', ''), ret)
        self.assertNotIn(('OBVIOUSLY_NOT_HERE', ''), ret)

    def test_check_renderer_blacklisting(self):
        '''
        Check that all renderers specified in the pipe string are available.
        '''
        ret = template.check_render_pipe_str('jinja|json', self.render_dict, ['jinja'], None)
        self.assertListEqual([('fake_json_func', '')], ret)
        ret = template.check_render_pipe_str('jinja|json', self.render_dict, None, ['jinja'])
        self.assertListEqual([('fake_jinja_func', '')], ret)
        ret = template.check_render_pipe_str('jinja|json', self.render_dict, ['jinja'], ['jinja'])
        self.assertListEqual([], ret)
        ret = template.check_render_pipe_str('jinja|json', self.render_dict, ['jinja'], ['jinja', 'json'])
        self.assertListEqual([('fake_json_func', '')], ret)
