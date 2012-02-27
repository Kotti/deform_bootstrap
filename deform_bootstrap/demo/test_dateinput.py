import unittest
import datetime

from deformdemo import test

browser = None
now = datetime.datetime.now()


def setUpModule():
    from deformdemo.selenium import selenium
    global browser
    browser = selenium("localhost", 4444, "*chrome", "http://localhost:8521/")
    browser.start()
    return browser


def tearDownModule():
    browser.stop()


class DateInputWidgetTests(test.Base, unittest.TestCase):

    url = '/dateinput/'

    def test_submit_tooearly(self):
        browser.open(self.url)
        browser.wait_for_page_to_load("30000")
        browser.focus('css=#deformField1')
        browser.click('css=#deformField1')
        browser.click('css=div[date=2010-05-04]')
        browser.click("submit")
        browser.wait_for_page_to_load("30000")
        self.assertTrue(browser.get_text('css=.errorMsgLbl'))
        error_node = 'css=#error-deformField1'
        self.assertEqual(browser.get_text(error_node),
                         '2010-05-04 is earlier than earliest date 2010-05-05')
        self.assertEqual(browser.get_text('css=#captured'), 'None')
        self.assertTrue(browser.is_element_present('css=.errorMsgLbl'))

    def test_submit_success(self):
        browser.open(self.url)
        browser.wait_for_page_to_load("30000")
        browser.focus('css=#deformField1')
        browser.click('css=#deformField1')
        browser.click('css=div[date=2010-05-06]')
        browser.click("submit")
        browser.wait_for_page_to_load("30000")
        self.assertFalse(browser.is_element_present('css=.errorMsgLbl'))
        self.assertEqual(browser.get_text('css=#captured'),
                         "{'date': datetime.date(2010, 5, 6)}")
        self.assertEqual(browser.get_value('deformField1'), '2010-05-06')


class SequenceOfDateInputs(test.Base, unittest.TestCase):

    url = '/sequence_of_dateinputs/'

    def test_submit_one_filled(self):
        browser.open(self.url)
        browser.wait_for_page_to_load("30000")
        browser.click('deformField1-seqAdd')
        added = 'dom=document.forms[0].date'
        browser.focus(added)
        browser.click(added)
        browser.click('css=div[date=%d-%02d-06]' % (now.year, now.month))
        browser.click("submit")
        browser.wait_for_page_to_load("30000")
        self.assertFalse(browser.is_element_present('css=.errorMsgLbl'))
        captured = browser.get_text('css=#captured')
        self.assertTrue(captured.startswith(u"{'dates': [datetime.date"))


class DateTimeInputWidgetTests(test.Base, unittest.TestCase):

    url = '/datetime_input/'

    def test_render_default(self):
        browser.open(self.url)
        self.assertEqual(browser.get_text('css=.req'), '*')
        self.assertEqual(browser.get_text('css=#captured'), 'None')
        self.assertEqual(browser.get_value('deformField1-date'), '2010-05-06')
        self.assertEqual(browser.get_value('deformField1-time'), '12:00:00')
        self.assertFalse(browser.is_element_present('css=.errorMsgLbl'))

    def test_submit_empty(self):
        browser.open(self.url)
        browser.wait_for_page_to_load("30000")
        browser.type('deformField1-date', '')
        browser.click("submit")
        browser.wait_for_page_to_load("30000")
        self.assertTrue(browser.get_text('css=.errorMsgLbl'))
        error_node = 'css=#error-deformField1'
        self.assertEqual(browser.get_text(error_node), 'Incomplete date')
        self.assertEqual(browser.get_text('css=#captured'), 'None')
        self.assertTrue(browser.is_element_present('css=.errorMsgLbl'))

    def test_submit_tooearly(self):
        browser.open(self.url)
        browser.wait_for_page_to_load("30000")
        browser.focus('css=#deformField1-date')
        browser.click('css=#deformField1-date')
        browser.click('css=div[date=2010-05-05]')
        browser.click("submit")
        browser.wait_for_page_to_load("30000")
        self.assertTrue(browser.get_text('css=.errorMsgLbl'))
        error_node = 'css=#error-deformField1'
        self.assertEqual(browser.get_text(error_node),
                         '2010-05-05 12:00:00+00:00 is earlier than earliest datetime 2010-05-05 12:30:00+00:00')
        self.assertEqual(browser.get_text('css=#captured'), 'None')
        self.assertTrue(browser.is_element_present('css=.errorMsgLbl'))

    def test_submit_success(self):
        browser.open(self.url)
        browser.wait_for_page_to_load("30000")
        browser.focus('css=#deformField1-date')
        browser.click('css=#deformField1-date')
        browser.click('css=div[date=2010-05-05]')
        browser.focus('css=#deformField1-time')
        browser.click('css=#deformField1-time')
        browser.type_keys('deformField1-time', '12:30:00')
        browser.click("submit")
        browser.wait_for_page_to_load("30000")
        self.assertFalse(browser.is_element_present('css=.errorMsgLbl'))
        self.assertTrue(browser.get_text('css=#captured').startswith(
            "{'date_time': datetime.datetime(2010, 5, 5, 12, 30, tzinfo"))
        self.assertEqual(browser.get_value('deformField1-date'), '2010-05-05')
        self.assertEqual(browser.get_value('deformField1-time'), '12:30:00')


if __name__ == '__main__':

    setUpModule()
    try:
        unittest.main()
    finally:
        tearDownModule()
