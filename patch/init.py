# -*- coding: utf-8  -*-

import os

if "WPROBOT_DIR" not in os.environ:
    import sys
    sys.path.append(os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")))
    import wprobot
