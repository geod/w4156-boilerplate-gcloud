import sys
import os

# sys.modules.pop('google')

from google.appengine.ext import vendor

# Add any libraries installed in the "lib" folder
# 'lib' added to sys.path by appengine_config.py
print(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))
vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))
