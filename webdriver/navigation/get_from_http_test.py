import os
import sys
import unittest

sys.path.insert(1, os.path.abspath(os.path.join(__file__, "../..")))
import base_test


class GetFromHttpTest(base_test.WebDriverBaseTest):
    def testGetUrlWithNoRedirectionOverHttp(self):
        page = self.webserver.where_is('navigation/res/empty.html')
        self.driver.get(page)
        url = self.driver.current_url
        self.assertEquals(page, url)

    def testGetWillFollowTheLocationHeader(self):
        page = self.webserver.where_is('navigation/redirect')
        self.driver.get(page)
        expected = self.webserver.where_is('navigation/res/empty.html')
        url = self.driver.current_url
        self.assertEquals(expected, url)

    def testGetWillFollowMetaRefreshThatRefreshesInstantly(self):
        page = self.webserver.where_is('navigation/res/instant-meta-redirect.html')
        self.driver.get(page)
        expected = self.webserver.where_is('navigation/res/empty.html')
        url = self.driver.current_url
        self.assertEquals(expected, url)

    def testGetWillFollowMetaRefreshThatRefreshesAfterOneSecond(self):
        page = self.webserver.where_is('navigation/res/1s-meta-redirect.html')
        self.driver.get(page)
        expected = self.webserver.where_is('navigation/res/empty.html')
        url = self.driver.current_url
        self.assertEquals(expected, url)


    def testGetWillNotFollowMetaRefreshThatRefreshesAfterMoreThanOneSecond(self):
        page = self.webserver.where_is('navigation/res/60s-meta-redirect.html')
        self.driver.get(page)
        url = self.driver.current_url
        self.assertEquals(page, url)

if __name__ == '__main__':
    unittest.main()
