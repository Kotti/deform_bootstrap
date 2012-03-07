import unittest
import time

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


class ChosenSingleWidgetTests(test.Base, unittest.TestCase):

    url = '/chosen_single/'

    def test_render(self):
        browser.open(self.url)
        browser.wait_for_page_to_load("30000")
        self.assertTrue(browser.is_text_present("Country"))
        self.assertTrue(browser.is_text_present("Select a country"))   # placeholder
        self.assertEqual(browser.get_attribute("deformField1@name"), 'country')
        self.assertEqual(browser.get_selected_index('deformField1'), '0')
        options = browser.get_select_options('deformField1')
        self.assertEqual(
            options,
            ['', u'Austria', u'Belgium', u'Bulgaria', u'Cyprus', u'Czech Republic',
             u'Denmark', u'Estonia', u'Finland', u'France', u'Germany', u'Greece',
             u'Hungary', u'Ireland', u'Italy', u'Latvia', u'Lithuania', u'Luxembourg',
             u'Malta', u'Netherlands', u'Poland', u'Portugal', u'Romania', u'Slovakia',
             u'Slovenia', u'Spain', u'Sweden', u'United Kingdom'])
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

    def test_submit_selected(self):
        browser.open(self.url)
        browser.wait_for_page_to_load("30000")
        browser.select('deformField1', 'index=1')
        browser.click('submit')
        browser.wait_for_page_to_load("30000")
        self.assertFalse(browser.is_element_present('css=.errorMsgLbl'))
        self.assertEqual(browser.get_selected_index('deformField1'), '1')
        captured = browser.get_text('css=#captured')
        self.assertSimilarRepr(
            captured, 
            u"{'country': 'AT'}")




class ChosenMultipleWidgetTests(test.Base, unittest.TestCase):

    url = '/chosen_multiple/'

    def test_render(self):
        browser.open(self.url)
        browser.wait_for_page_to_load("30000")
        self.assertTrue(browser.is_text_present("Countries"))
        self.assertTrue(browser.is_text_present("Select countries"))   # placeholder
        self.assertEqual(browser.get_attribute("deformField1@name"), 'countries')
        self.assertRaises(Exception, browser.get_selected_index, 'deformField1')   # ERROR: No option selected
        options = browser.get_select_options('deformField1')
        self.assertEqual(
            options,
            ['', u'Austria', u'Belgium', u'Bulgaria', u'Cyprus', u'Czech Republic',
             u'Denmark', u'Estonia', u'Finland', u'France', u'Germany', u'Greece',
             u'Hungary', u'Ireland', u'Italy', u'Latvia', u'Lithuania', u'Luxembourg',
             u'Malta', u'Netherlands', u'Poland', u'Portugal', u'Romania', u'Slovakia',
             u'Slovenia', u'Spain', u'Sweden', u'United Kingdom'])
        self.assertEqual(browser.get_text('css=#captured'), 'None')

    def test_submit_empty(self):
        """
        An empty, non mandatory selection gives an empty set.
        """
        browser.open(self.url)
        browser.wait_for_page_to_load("30000")
        browser.click('submit')
        browser.wait_for_page_to_load("30000")
        captured = browser.get_text('css=#captured')
        self.assertSimilarRepr(
                captured,
                u"{'countries': set([])}")

    def test_submit_filled(self):
        """
        Selects several options, with arrow keys.
        """
        browser.open(self.url)
        browser.wait_for_page_to_load("30000")
        el = 'css=#deformField1 + div li.search-field input'
        # type_keys() seems not to work here
        for op in [2, 5, 10]:
            browser.click(el)
            time.sleep(.2)
            for i in range(op):
                browser.key_down(el, "\\40")
                browser.key_up(el, "\\40")
            browser.key_down(el, "\\13")
            browser.key_up(el, "\\13")
            time.sleep(.2)
        browser.click('submit')
        browser.wait_for_page_to_load("30000")
        captured = browser.get_text('css=#captured')
        self.assertEqual(eval(captured), {'countries': set([u'EE', u'BG', u'IE'])})



if __name__ == '__main__':

    setUpModule()
    try:
        unittest.main()
    finally:
        tearDownModule()

