# -*- coding: utf-8  -*-

import os
import sys

def appendif(arr, val):
    if val not in arr:
        arr.append(val)

def simplifypath(*path):
    return os.path.abspath(os.path.expanduser(os.path.join(*path)))
    
def init():
    if "WPROBOT_BOT" not in os.environ:
        for ind, arg in enumerate(sys.argv):
            if arg.startswith("-bot:"):
                os.environ["WPROBOT_BOT"] = arg[len("-bot:"):]
                sys.argv.pop(ind)
                break
        else:
            print "Please specify bot's name by parameter -bot:"
            sys.exit()

    dirbot = simplifypath(os.environ["WPROBOT_DIR"], "bots",
                          os.environ["WPROBOT_BOT"])
    appendif(sys.argv, "-dir:" + dirbot)

firsttime = False

if "WPROBOT_DIR" not in os.environ:
    firsttime = True
    os.environ["WPROBOT_DIR"] = os.path.split(__file__)[0]
    init()
    
appendif(sys.path, simplifypath(os.environ["WPROBOT_DIR"]))

import conf.conf
appendif(sys.path, simplifypath(conf.conf.pywikibotDir))
appendif(sys.path, simplifypath(conf.conf.pywikibotDir, "externals"))

import patch

if firsttime:
    if __name__ == "__main__":
        sys.argv.pop(0)
        if sys.argv:
            if not os.path.exists(sys.argv[0]):
                testpath = os.path.join(os.path.split(__file__)[0],
                                        "scripts",
                                        sys.argv[0])
                if os.path.exists(testpath):
                    sys.argv[0] = testpath
                else:
                    testpath = testpath + ".py"
                    if os.path.exists(testpath):
                        sys.argv[0] = testpath
                    else:
                        raise Exception("%s not found!" % sys.argv[0])
            sys.path.append(os.path.split(sys.argv[0])[0])
            sys.argv.append("-main")
            execfile(sys.argv[0])

