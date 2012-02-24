# -*- coding: utf-8 -*-

import unittest

from deformdemo import test

browser = None


def patch_test_render_default(self):
    browser.open(self.url)
    browser.wait_for_page_to_load("30000")

    self.assertTrue(browser.is_text_present(u"По оживлённым берегам"))
    # self.assertEqual(browser.get_attribute("item-deformField1@title"),
    #                  description)
    # self.assertEqual(browser.get_attribute("css=label@title"),
    #                  description)
    self.assertEqual(browser.get_attribute("deformField1@name"), 'field')
    self.assertEqual(browser.get_value("deformField1"), u'☃')
    self.assertEqual(browser.get_text('css=#captured'), 'None')


def _patch():
    test.UnicodeEverywhereTests.test_render_default = patch_test_render_default

if __name__ == '__main__':
    test.setUpModule()
    browser = test.browser
    _patch()
    try:
        unittest.main(test)
    finally:
        test.tearDownModule()
