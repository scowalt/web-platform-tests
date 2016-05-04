import os
import sys
import unittest

sys.path.insert(1, os.path.abspath(os.path.join(__file__, "../..")))
import base_test
from selenium.webdriver.remote.webelement import WebElement


class ExecuteScriptAsyncTest(base_test.WebDriverBaseTest):
    def test_ecmascript_translates_null_return_to_none(self):
        self.driver.get(self.webserver.where_is("javascript/res/execute_script_test.html"))
        result = self.driver.execute_async_script("arguments[0](null);")
        self.assertIsNone(result)

    def test_ecmascript_translates_undefined_return_to_none(self):
        self.driver.get(self.webserver.where_is("javascript/res/execute_script_test.html"))
        result = self.driver.execute_async_script("var undef; arguments[0](undef);")
        self.assertIsNone(result)

    def test_can_return_numbers_from_scripts(self):
        self.driver.get(self.webserver.where_is("javascript/res/execute_script_test.html"))
        self.assertEquals(1, self.driver.execute_async_script("arguments[0](1);"))
        self.assertEquals(3.14, self.driver.execute_async_script("arguments[0](3.14);"))

    def test_can_return_strings_from_scripts(self):
        self.driver.get(self.webserver.where_is("javascript/res/execute_script_test.html"))
        self.assertEquals("hello, world!",
        				  self.driver.execute_async_script("arguments[0]('hello, world!');"))

    def test_can_return_booleans_from_scripts(self):
        self.driver.get(self.webserver.where_is("javascript/res/execute_script_test.html"))
        self.assertTrue(self.driver.execute_async_script("arguments[0](true);"))
        self.assertFalse(self.driver.execute_async_script("arguments[0](false);"))

    def test_can_return_an_array_of_primitives(self):
        self.driver.get(self.webserver.where_is("javascript/res/execute_script_test.html"))

        result = self.driver.execute_async_script("arguments[0]([1, false, null, 3.14])")
        self.assertListEqual([1, False, None, 3.14], result)

    def test_can_return_nested_arrays(self):
        self.driver.get(self.webserver.where_is("javascript/res/execute_script_test.html"))
        result = self.driver.execute_async_script("arguments[0]([[1, 2, [3]]])")

        self.assertIsInstance(result, list)
        self.assertEquals(1, len(result))

        result = result[0]
        self.assertListEqual([1, 2], result[:2])
        self.assertListEqual([3], result[2])

    def test_can_return_object_literals(self):
        self.driver.get(self.webserver.where_is("javascript/res/execute_script_test.html"))

        result = self.driver.execute_async_script("arguments[0]({})")
        self.assertDictEqual({}, result)

        result = self.driver.execute_async_script("arguments[0]({a: 1, b: false, c: null})")
        self.assertDictEqual({
            "a": 1,
            "b": False,
            "c": None
        }, result)

    def test_arguments(self):
        self.driver.get(self.webserver.where_is("javascript/res/return_document_body.html"))
        body = self.driver.execute_script("return document.body;")
        result = self.driver.execute_async_script("arguments[2]({a: arguments[0], b: arguments[1]})", [456], "asdf")
        self.assertDictEqual({
            "a": [456],
            "b": "asdf"
        }, result)
        result = self.driver.execute_async_script("""
            var retFunc = arguments[1];
            var elem = arguments[0];
            window.setTimeout(
                    function () {
                        retFunc(elem.textContent);}, 100);
            """, body)
        self.assertEquals(result, "Hello, world!\n")

    def test_can_return_complex_object_literals(self):
        self.driver.get(self.webserver.where_is("javascript/res/execute_script_test.html"))
        result = self.driver.execute_async_script("arguments[0]({a:{b: 'hello'}})")
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result['a'], dict)
        self.assertDictEqual({"b": "hello"}, result["a"])

    def test_dom_element_return_value_is_translated_to_a_web_element(self):
        self.driver.get(self.webserver.where_is(
       			"javascript/res/return_document_body.html"))

        result = self.driver.execute_async_script("""
            var retFunc = arguments[0];
            window.setTimeout(
                    function () {
                        retFunc(document.body);}, 100);
            """)
        self.assertEquals(result.text, "Hello, world!")

    def test_return_an_array_of_dom_elements(self):
        self.driver.get(self.webserver.where_is(
       			"javascript/res/return_array_of_dom_elements.html"))

        result = self.driver.execute_async_script(
        	    "var nodes = document.getElementsByTagName('div');"
        	    "arguments[0]([nodes[0], nodes[1]]);")

        self.assertIsInstance(result, list)
        self.assertEquals(2, len(result))
        self.assertEquals("a", result[0].text)
        self.assertEquals("b", result[1].text)

    def test_node_list_return_value_is_translated_to_list_of_web_elements(self):
        self.driver.get(self.webserver.where_is(
       			"javascript/res/return_array_of_dom_elements.html"))

        result = self.driver.execute_async_script(
        	    "arguments[0](document.getElementsByTagName('div'));")

        self.assertIsInstance(result, list)
        self.assertEquals(2, len(result))
        self.assertEquals("a", result[0].text)
        self.assertEquals("b", result[1].text)

    def test_return_object_literal_with_dom_element_property(self):
        self.driver.get(self.webserver.where_is("javascript/res/execute_script_test.html"))
        result = self.driver.execute_async_script("arguments[0]({a: document.body});")
        self.assertIsInstance(result, dict)
        self.assertEquals("body", result["a"].tag_name)

    def test_scripts_execute_in_anonymous_function_and_do_not_pollute_global_scope(self):
        self.driver.get(self.webserver.where_is("javascript/res/execute_script_test.html"))
        self.driver.execute_async_script("var x = 1;arguments[0]();")
        self.assertEquals("undefined", self.driver.execute_async_script("arguments[0](typeof x);"));

    def test_scripts_can_modify_context_window_object(self):
        self.driver.get(self.webserver.where_is("javascript/res/execute_script_test.html"))
        self.driver.execute_async_script("window.x = 1;arguments[0]()")
        self.assertEquals("number", self.driver.execute_async_script("arguments[0](typeof x);"));
        self.assertEquals(1, self.driver.execute_async_script("arguments[0](x);"));

    def test_that_ecmascript_returns_document_title(self):
        self.driver.get(self.webserver.where_is("javascript/res/execute_script_test.html"))
        result = self.driver.execute_async_script("arguments[0](document.title);")
        self.assertEquals("executeScript test", result)


if __name__ == "__main__":
    unittest.main()
