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
        val = self.driver.execute(cmd.Command.GET_LOCAL_STORAGE_ITEM, {'key': 'a'})
        self.assertEquals("b", val['value'])
        self.driver.execute_script("localStorage.getItem('a');")
        self.assertEquals("b", val['value'])

    def test_clear(self):
        self.driver.get(self.webserver.where_is("ecmascript/res/ecmascript_test.html"))
        self.driver.execute(cmd.Command.SET_LOCAL_STORAGE_ITEM, {'key': 'a', 'value': 'b'})
        self.driver.execute(cmd.Command.CLEAR_LOCAL_STORAGE)
        val = self.driver.execute(cmd.Command.GET_LOCAL_STORAGE_ITEM, {'key': 'a'})
        self.assertEquals(None, val['value'])

    def test_remove(self):
        self.driver.get(self.webserver.where_is("ecmascript/res/ecmascript_test.html"))
        self.driver.execute(cmd.Command.SET_LOCAL_STORAGE_ITEM, {'key': 'a', 'value': 'b'})
        self.driver.execute(cmd.Command.REMOVE_LOCAL_STORAGE_ITEM, {'key': 'a'})
        val = self.driver.execute(cmd.Command.GET_LOCAL_STORAGE_ITEM, {'key': 'a'})
        self.assertEquals(None, val['value'])

    def test_keys(self):
        self.driver.get(self.webserver.where_is("ecmascript/res/ecmascript_test.html"))
        self.driver.execute(cmd.Command.SET_LOCAL_STORAGE_ITEM, {'key': 'a', 'value': 'b'})
        self.driver.execute(cmd.Command.SET_LOCAL_STORAGE_ITEM, {'key': 'b', 'value': 'b'})
        self.driver.execute(cmd.Command.SET_LOCAL_STORAGE_ITEM, {'key': 'c', 'value': 'b'})
        keys = self.driver.execute(cmd.Command.GET_LOCAL_STORAGE_KEYS)
        self.assertEquals(['a', 'b', 'c'], keys['value'])

    def test_size(self):
        self.driver.get(self.webserver.where_is("ecmascript/res/ecmascript_test.html"))
        self.driver.execute(cmd.Command.CLEAR_LOCAL_STORAGE)
        self.driver.execute(cmd.Command.SET_LOCAL_STORAGE_ITEM, {'key': 'a', 'value': 'b'})
        val = self.driver.execute(cmd.Command.GET_LOCAL_STORAGE_SIZE)
        self.assertEquals(1, val['value'])
        self.driver.execute(cmd.Command.SET_LOCAL_STORAGE_ITEM, {'key': 't', 'value': 'b'})
        val = self.driver.execute(cmd.Command.GET_LOCAL_STORAGE_SIZE)
        self.assertEquals(2, val['value'])
        self.driver.execute(cmd.Command.SET_LOCAL_STORAGE_ITEM, {'key': 't', 'value': 'b'})
        val = self.driver.execute(cmd.Command.GET_LOCAL_STORAGE_SIZE)
        self.assertEquals(2, val['value'])

if __name__ == "__main__":
    unittest.main()
