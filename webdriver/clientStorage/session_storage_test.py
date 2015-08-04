import os
import sys
import unittest
import selenium.webdriver.remote.command as cmd

sys.path.insert(1, os.path.abspath(os.path.join(__file__, "../..")))
import base_test


class SessionStorageTest(base_test.WebDriverBaseTest):
    def test_set_get(self):
        self.driver.get(self.webserver.where_is("javascript/res/execute_script_test.html"))
        self.driver.execute(cmd.Command.SET_SESSION_STORAGE_ITEM, {'key': 'a', 'value': 'b'})
        val = self.driver.execute(cmd.Command.GET_SESSION_STORAGE_ITEM, {'key': 'a'})
        self.assertEquals("b", val['value'])
        val = self.driver.execute_script("return sessionStorage.getItem('a');")
        self.assertEquals("b", val)

    def test_clear(self):
        self.driver.get(self.webserver.where_is("javascript/res/execute_script_test.html"))
        self.driver.execute(cmd.Command.SET_SESSION_STORAGE_ITEM, {'key': 'a', 'value': 'b'})
        self.driver.execute(cmd.Command.CLEAR_SESSION_STORAGE)
        val = self.driver.execute(cmd.Command.GET_SESSION_STORAGE_ITEM, {'key': 'a'})
        self.assertEquals(None, val['value'])

    def test_remove(self):
        self.driver.get(self.webserver.where_is("javascript/res/execute_script_test.html"))
        self.driver.execute(cmd.Command.SET_SESSION_STORAGE_ITEM, {'key': 'a', 'value': 'b'})
        self.driver.execute(cmd.Command.REMOVE_SESSION_STORAGE_ITEM, {'key': 'a'})
        val = self.driver.execute(cmd.Command.GET_SESSION_STORAGE_ITEM, {'key': 'a'})
        self.assertEquals(None, val['value'])

    def test_keys(self):
        self.driver.get(self.webserver.where_is("javascript/res/execute_script_test.html"))
        self.driver.execute(cmd.Command.SET_SESSION_STORAGE_ITEM, {'key': 'a', 'value': 'b'})
        self.driver.execute(cmd.Command.SET_SESSION_STORAGE_ITEM, {'key': 'b', 'value': 'b'})
        self.driver.execute(cmd.Command.SET_SESSION_STORAGE_ITEM, {'key': 'c', 'value': 'b'})
        keys = self.driver.execute(cmd.Command.GET_SESSION_STORAGE_KEYS)
        self.assertEquals(['a', 'b', 'c'], keys['value'])

    def test_size(self):
        self.driver.get(self.webserver.where_is("javascript/res/execute_script_test.html"))
        self.driver.execute(cmd.Command.CLEAR_SESSION_STORAGE)
        self.driver.execute(cmd.Command.SET_SESSION_STORAGE_ITEM, {'key': 'a', 'value': 'b'})
        val = self.driver.execute(cmd.Command.GET_SESSION_STORAGE_SIZE)
        self.assertEquals(1, val['value'])
        self.driver.execute(cmd.Command.SET_SESSION_STORAGE_ITEM, {'key': 't', 'value': 'b'})
        val = self.driver.execute(cmd.Command.GET_SESSION_STORAGE_SIZE)
        self.assertEquals(2, val['value'])
        self.driver.execute(cmd.Command.SET_SESSION_STORAGE_ITEM, {'key': 't', 'value': 'b'})
        val = self.driver.execute(cmd.Command.GET_SESSION_STORAGE_SIZE)
        self.assertEquals(2, val['value'])

if __name__ == "__main__":
    unittest.main()
