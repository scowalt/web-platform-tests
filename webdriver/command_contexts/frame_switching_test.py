import os
import sys
import random
import unittest

sys.path.insert(1, os.path.abspath(os.path.join(__file__, "../..")))
import base_test

repo_root = os.path.abspath(os.path.join(__file__, "../../.."))
sys.path.insert(1, os.path.join(repo_root, "tools", "webdriver"))
from webdriver import exceptions


class FrameSwitchingTest(base_test.WebDriverBaseTest):
    def setUp(self):
        self.driver.get(self.webserver.where_is("command_contexts/res/frames-page.html"))

    def test_can_retrieve_content_from_iframe(self):
        self.driver.switch_to_frame("iframe")
        self.assertEquals(self.driver.find_element_by_id("content").get_text(), "Frame content")
        
    def test_can_click_button_in_iframe(self):
        self.driver.switch_to_frame("iframe")
        frame_content = self.driver.find_element_by_id("frame_button").click()
        self.assertEquals(self.driver.find_element_by_id("content").get_text(), "Frame button clicked")

    def test_can_switch_to_parent_frame(self):
        self.driver.switch_to_frame("iframe")
        self.driver.switch_to_parent_frame()
        self.assertEquals(self.driver.find_element_by_id("content").get_text(), "Parent content")

    def test_can_switch_to_top_level_context(self):
        self.driver.switch_to_frame("iframe")
        self.driver.switch_to_frame(None)
        self.assertEquals(self.driver.find_element_by_id("content").get_text(), "Parent content")
        
    def test_can_switch_to_nonexistent_parent_frame(self):
        self.driver.switch_to_parent_frame()
        self.assertEquals(self.driver.find_element_by_id("content").get_text(), "Parent content")

    def test_attempt_switch_to_non_frame_element_throws(self):        
        self.assertRaises(exceptions.NoSuchFrameException, lambda: self.driver.switch_to_frame("nothing"))

    def test_attempt_switch_to_nonexistent_frame_throws(self):        
        self.assertRaises(exceptions.NoSuchFrameException, lambda: self.driver.switch_to_frame("content"))

if __name__ == "__main__":
    unittest.main()
