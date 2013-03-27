# -*- coding: utf-8  -*-

def init():
    import sys
    
    def simplifypath(path):
        return os.path.abspath(
                os.path.expanduser(os.path.join(*path)))
    
    for ind, arg in enumerate(sys.argv):
        if arg.startswith("-bot:"):
            botName = arg[len("-bot:"):]
            sys.argv.pop(ind)
            break
            
    dirbot = simplifypath([os.environ["WPROBOT_DIR"], "bots", botName])
    sys.argv.append("-dir:" + dirbot)
    
    sys.path.append(simplifypath([os.environ["WPROBOT_DIR"]]))
            
    import conf.conf
    sys.path.append(simplifypath([conf.conf.pywikibotDir]))
    
    import wp.patch
    
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

import os

if "WPROBOT_DIR" not in os.environ:
    os.environ["WPROBOT_DIR"] = os.path.split(__file__)[0]
    init()