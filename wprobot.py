# -*- coding: utf-8  -*-

import os

def init():
    import sys

    def simplifypath(*path):
        return os.path.abspath(os.path.expanduser(os.path.join(*path)))

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
    sys.argv.append("-dir:" + dirbot)

    sys.path.append(simplifypath(os.environ["WPROBOT_DIR"]))
    #sys.path.append(simplifypath(os.environ["WPROBOT_DIR"], "externals/pyparsing"))

    import conf.conf
    sys.path.append(simplifypath(conf.conf.pywikibotDir))
    sys.path.append(simplifypath(conf.conf.pywikibotDir, "externals/httplib2"))

    patchPath = simplifypath(os.environ["WPROBOT_DIR"], "patch")
    for f in os.listdir(patchPath):
        execfile(os.path.join(patchPath, f))

    if __name__ == "__main__":
        sys.argv.pop(0)
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
        execfile(sys.argv[0])

if "WPROBOT_DIR" not in os.environ:
    os.environ["WPROBOT_DIR"] = os.path.split(__file__)[0]
    init()
