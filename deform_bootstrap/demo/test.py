# -*- coding: utf-8 -*-

import unittest

from deformdemo import test as test_deformdemo
from deform_bootstrap.demo import test_typeahead
from deform_bootstrap.demo import test_dateinput

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


def patch_disable_test(self):
    pass


def _patch_deform_tests():
    test_deformdemo.UnicodeEverywhereTests.test_render_default = patch_test_render_default
    test_deformdemo.RedirectingAjaxFormTests.test_submit_success = patch_disable_test
    test_deformdemo.AjaxFormTests.test_submit_success = patch_disable_test
    
    # some of the default DateInputWidgetTests are replaced by our own tests,
    # because the dates are divs in bootstrap_datepicker
    # (and not links like in jQueryUI)
    test_deformdemo.DateInputWidgetTests.test_submit_tooearly = patch_disable_test
    test_deformdemo.DateInputWidgetTests.test_submit_success = patch_disable_test
    test_deformdemo.SequenceOfDateInputs.test_submit_one_filled = patch_disable_test
    test_deformdemo.DateTimeInputWidgetTests.test_submit_tooearly = patch_disable_test
    test_deformdemo.DateTimeInputWidgetTests.test_submit_success = patch_disable_test

if __name__ == '__main__':
    _patch_deform_tests()
    for test in test_deformdemo, test_typeahead, test_dateinput:
        test.setUpModule()
        browser = test.browser
        try:
            unittest.main(test)
        finally:
            test.tearDownModule()
