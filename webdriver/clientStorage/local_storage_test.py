import os
import sys
import unittest
import selenium.webdriver.remote.command as cmd

sys.path.insert(1, os.path.abspath(os.path.join(__file__, "../..")))
import base_test


class LocalStorageTest(base_test.WebDriverBaseTest):
    def test_set_get(self):
        self.driver.get(self.webserver.where_is("ecmascript/res/ecmascript_test.html"))
        self.driver.execute(cmd.Command.SET_LOCAL_STORAGE_ITEM, {'key': 'a', 'value': 'b'})
        self.assertEquals("b", self.driver.execute(cmd.Command.GET_LOCAL_STORAGE_ITEM, {'key': 'a'})['value'])

    def test_clear(self):
        self.driver.get(self.webserver.where_is("ecmascript/res/ecmascript_test.html"))
        self.driver.execute(cmd.Command.SET_LOCAL_STORAGE_ITEM, {'key': 'a', 'value': 'b'})
        self.driver.execute(cmd.Command.CLEAR_LOCAL_STORAGE)
        self.assertEquals(None, self.driver.execute(cmd.Command.GET_LOCAL_STORAGE_ITEM, {'key': 'a'})['value'])


if __name__ == "__main__":
    unittest.main()
