#!/usr/bin/env python

"""Just used for testing while developing"""

# Hack to prefer local newsgrab
# UPDATE: not needed when installed in editable mode. pip -e
import sys, os
sys.path.insert (0, os.getcwd())

import newsgrab.__main__
