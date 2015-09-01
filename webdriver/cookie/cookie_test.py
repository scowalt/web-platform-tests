import os
import sys
import unittest

sys.path.insert(1, os.path.abspath(os.path.join(__file__, "../..")))
import base_test
from selenium.common import exceptions


class CookieTest(base_test.WebDriverBaseTest):
    def setUp(self):
        self.driver.get(self.webserver.where_is("cookie/res/cookie_container.html"))

    def test_can_create_a_well_formed_cookie( self ):
        self.driver.add_cookie({'name': 'foo', 'value': 'bar'})

    def test_should_throw_an_exception_when_semicolon_exists_in_the_cookie_attribute(self):
        invalid_name = 'foo;bar'
        try:
            self.driver.add_cookie({'name': invalid_name, 'value': 'foobar'})
            self.fail( 'should have thrown exceptions.' )

        except exceptions.UnableToSetCookieException:
            pass
        except exceptions.InvalidCookieDomainException:
            pass

    def test_should_throw_an_exception_the_name_is_null(self):
        try:
            self.driver.add_cookie({'name': None, 'value': 'foobar'})
            self.fail( 'should have thrown exceptions.' )

        except exceptions.UnableToSetCookieException:
            pass
        except exceptions.InvalidCookieDomainException:
            pass


if __name__ == '__main__':
    unittest.main()
