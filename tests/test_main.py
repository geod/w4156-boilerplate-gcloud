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
# from user import *
# from validation import *
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

    def test_listings(self):
        rv = self.app.get("/listings/index.html")
        self.check_culunch(rv)

    def test_settings(self):
        rv = self.app.get("/settings/index.html")
        self.check_culunch(rv)

'''# user creation validation
class ValidTest(unittest.TestCase)

    def test_form(self, form):
        
        # good
        form = Form("Shelley", "S", "sks2209", "lunch657")
        self.assertTrue = form_input_valid(form)

        # good
        form = Form ("Shelley", "S", "sks2209", "Lunch")
        self.assertTrue = form_input_valid (form)

        # good
        form = Form ("Shelley", "S", "sks2209", "LUNCH657")
        self.assertTrue = form_input_valid (form)

        # no name
        form = Form ("", "S", "sks2209", "Lunch657")
        self.assertFalse = form_input_valid(form)

        # no last
        form = Form ("Shelley", "", "sks2209", "Lunch657")
        self.assertFalse = form_input_valid (form)

        # no uni
        form = Form ("Shelley", "S", "", "Lunch657")
        self.assertFalse = form_input_valid (form)

        # no pass
        form = Form ("Shelley", "S", "sks2209", "")
        self.assertFalse = form_input_valid (form)

        # pass all lower
        form = Form ("Shelley", "S", "sks2209", "lunch")
        self.assertFalse = form_input_valid (form)

        # pass all upper
        form = Form ("Shelley", "S", "sks2209", "LUNCH")
        self.assertFalse = form_input_valid (form)

        # pass all numbers
        form = Form ("Shelley", "S", "sks2209", "1234")
        self.assertFalse = form_input_valid (form)'''


if __name__ == '__main__':
    unittest.main()
