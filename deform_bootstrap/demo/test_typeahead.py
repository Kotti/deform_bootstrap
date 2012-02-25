import unittest

from deformdemo import test

browser = None


def setUpModule():
    from deformdemo.selenium import selenium
    global browser
    browser = selenium("localhost", 4444, "*chrome", "http://localhost:8521/")
    browser.start()
    return browser


def tearDownModule():
    browser.stop()


class TypeaheadInputWidgetTests(test.Base, unittest.TestCase):
    url = "/typeahead_input/"

    def test_render_default(self):
        browser.open(self.url)
        browser.wait_for_page_to_load("30000")
        self.assertTrue(browser.is_text_present("Typeahead Input Widget"))
        self.assertEqual(browser.get_attribute("deformField1@name"), 'text')
        self.assertEqual(browser.get_attribute("deformField1@type"), 'text')
        self.assertEqual(browser.get_value("deformField1"), '')
        self.assertEqual(browser.get_text('css=.req'), '*')
        self.assertEqual(browser.get_text('css=#captured'), 'None')

    def test_submit_empty(self):
        browser.open(self.url)
        browser.wait_for_page_to_load("30000")
        browser.click('submit')
        browser.wait_for_page_to_load("30000")
        self.assertTrue(browser.is_element_present('css=.errorMsgLbl'))
        self.assertEqual(browser.get_text('css=#error-deformField1'),
                         'Required')
        captured = browser.get_text('css=#captured')
        self.assertEqual(captured, 'None')

    def test_submit_filled(self):
        browser.open(self.url)
        browser.wait_for_page_to_load("30000")
        browser.type_keys('deformField1', 'b')
        import time
        time.sleep(.2)
        self.assertTrue(browser.is_text_present('Bar'))
        self.assertTrue(browser.is_text_present('Baz'))
        browser.type_keys('deformField1', 'ba')
        browser.click('//li[@class="active"]/a')
        browser.click('submit')
        browser.wait_for_page_to_load("30000")
        self.assertFalse(browser.is_element_present('css=.errorMsgLbl'))
        captured = browser.get_text('css=#captured')
        self.assertSimilarRepr(
            captured,
            "{'text': u'Bar'}")
