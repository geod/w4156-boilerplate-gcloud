# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir, 'code')))


import main
from user import *
import unittest


class MainTest(unittest.TestCase):
    """This class uses the Flask tests app to run an integration test against a
    local instance of the server."""

    def check_culunch(self, rv):
        print(rv.data)
        assert ("cu@lunch" in rv.data.lower())

    def setUp(self):
        self.app = main.app.test_client()

    def test_index(self):
        rv = self.app.get('/index.html')
        self.check_culunch(rv)

    def test_listform(self):
        rv = self.app.get("/listform/index.html")
        self.check_culunch(rv)

    """

    def test_listings(self):
        rv = self.app.get("/listings/index.html")
        self.check_culunch(rv)

    def test_settings(self):
        rv = self.app.get("/settings/index.html")
        self.check_culunch(rv)
    """

# user creation validation
class ValidTest(unittest.TestCase):

    def test_form(self):
        
        # good
        form = Form("Shelley", "S", "sks2209", "lunch657", "school", "year", "interests")
        self.assertTrue = form.form_input_valid()

        # good
        form = Form("Shelley", "S", "sks2209", "Lunch", "school", "year", "interests")
        self.assertTrue = form.form_input_valid()

        # good
        form = Form("Shelley", "S", "sks2209", "LUNCH657", "school", "year", "interests")
        self.assertTrue = form.form_input_valid()

        # no name
        form = Form("", "S", "sks2209", "Lunch657", "school", "year", "interests")
        self.assertFalse = form.form_input_valid()

        # no last
        form = Form("Shelley", "", "sks2209", "Lunch657", "school", "year", "interests")
        self.assertFalse = form.form_input_valid()

        # no uni
        form = Form("Shelley", "S", "", "Lunch657", "school", "year", "interests")
        self.assertFalse = form.form_input_valid()

        # no pass
        form = Form("Shelley", "S", "sks2209", "", "school", "year", "interests")
        self.assertFalse = form.form_input_valid()

        # pass all lower
        form = Form("Shelley", "S", "sks2209", "lunch", "school", "year", "interests")
        self.assertFalse = form.form_input_valid()

        # pass all upper
        form = Form("Shelley", "S", "sks2209", "LUNCH", "school", "year", "interests")
        self.assertFalse = form.form_input_valid()

        # pass all numbers
        form = Form("Shelley", "S", "sks2209", "1234", "school", "year", "interests")
        self.assertFalse = form.form_input_valid()

# check database


if __name__ == '__main__':
    unittest.main()
