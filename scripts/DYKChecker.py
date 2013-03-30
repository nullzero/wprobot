# -*- coding: utf-8  -*-
"""DYKChecker!"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import json
import init
import wp
import pywikibot

def glob():
    pass

def main():
    page = wp.Page(wp.toutf(raw_input()))
    dic = {}
    
    while True:
        try:
            text = page.get()
            break
        except pywikibot.NoPage:
            dic["error"] = "page not exist"
            break
        except pywikibot.IsRedirectPage:
            page = page.getRedirectTarget()
        except:
            dic["error"] = "unknown error"
            break
        
    if "error" not in dic:
        dic["len"] = len(text)
        
    print json.dumps(dic)
    
if __name__ == "__main__":
    args, site, conf = wp.pre("DYK Checker")
    try:
        glob()
        main()
    except:
        wp.posterror()
    else:
        wp.post()
