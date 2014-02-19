#!/usr/bin/python
# -*- coding: utf-8  -*-
"""Update page"""

__version__ = "1.0.1"
__author__ = "Sorawee Porncharoenwase"

import sys
import time
import init
import wp
import pywikibot
from wp import lre, lnotify, lthread, ltime

debug = False
allo = ""

def glob():
    lre.pats["entry"] = lre.lre(ur"(?sm)\{\{\s*แจ้งปรับปรุงหน้าอัตโนมัติ\s*"
                                ur"((?:\{\{.*?\}\}|.)*?)\s*\}\}")
    lre.pats["param"] = lre.lre(r"(?s)\|\s*((?:\{\{.*?\}\}|.)*?)\s*(?=\|)")
    lre.pats["num"] = lre.lre(r"\d+$")
    lre.pats["user0"] = lre.lre(r"\{\{User0\|(.*?)\}\}")
    lre.pats["trimComment"] = lre.lre(r"<!--#(.*?)#-->")

def checkparams(params):
    # NotImplemented
    return True

def error(e, desc=None):
    # NotImplemented
    pywikibot.output("E: " + e)
    if desc:
        pywikibot.output(">>> " + unicode(desc))

signal = False
def parse(text):
    global signal
    if not (text[0] == '"' and text[-1] == '"'):
        error("not begin or end with double quote", text)
        sys.exit()
    a = lre.pats["trimComment"].sub("", 
            (text[1:-1].replace("\\{", "{")
                        .replace("\\}", "}")
                        .replace("\\!", "|")
                        .replace('"', '\\"')))
    #print a
    #print "--------"
    if "\t" not in a or a.count('\n') == 1:
        a = a.replace('\n', '\\n')
    else:
        a = "\"\"\\\n" + a + "\"\""
        #print a
        #print "--------"
        signal = True
    return a            
                        
allpages = {}

def process(text, page_config):
    global putWithSysop

    params = {}
    for key in conf.seriesKey:
        params[conf.seriesKey[key]] = []

    errorlist = []
    deprecated = []
    checkcat = []
    try:
        for param in lre.pats["param"].finditer(text + "|"):
            param = param.group(1)
            key, dat = param.split("=", 1)
            key = key.strip()
            dat = dat.strip()
            if key in conf.translateKey:
                params[conf.translateKey[key]] = dat
            else:
                num = lre.pats["num"].find(key)
                key = lre.pats["num"].sub("", key)
                if key in conf.seriesKey:
                    params[conf.seriesKey[key]].append((num, dat))
                else:
                    error("unknown parameter", param)
    except:
        wp.error()
        if "source" in params:
            pywikibot.output(u"Error when updating %s" % params["source"])
        else:
            pywikibot.output(u"Error when processing page %s" % page_config)
        return

    """
    if not checkparams(params):
        error("something wrong")
        return
    """
    
    params["users"] = "'" + "', '".join([lre.pats["user0"].find(x.strip(), 1) for x in params["notifyuser"].split("\n")]) + "'"
    
    def changeYes(k): params[k] = u"    '{}': True,\n".format(k) if (k in params and params[k] == conf.yes) else ""
    def changeString(k): params[k] = u"    '{}': u'{}',\n".format(k, params[k]) if (k in params) else ""
    
    changeYes("disable")
    changeYes("sandbox")
    changeYes("stable")
    changeString("note")
    changeString("message")
    
    
    output1 = (
u"""\
###############################

page = u'{page}'

config[page] = {{
    'source': u'{source}',
{disable}{note}{sandbox}{stable}{message}    'users': [{users}],
    'findText': [],
    'addParam': [],
    'obsolete': [],
}}

""".format(**params))
    
    def space(a):
        a = unicode(a)
        return " " * (len(a) + 35)
    
    output = ""
    global signal
    for key in params:
        if key == "find":
            for kk, (i, j) in enumerate(params[key]):
                output += u"""config[page]['findText'].append(({}, u"{}",\n{}u"{}"))\n""".format(i, parse(j), space(i), parse(params['replace'][kk][1]))
                if signal:
                    #print output
                    #raw_input("...")
                    signal = False
    for key in params:
        if key == "param":
            for kk, (i, j) in enumerate(params[key]):
                output += u"""config[page]['addParam'].append(({}, u"{}",\n{}u"{}"))\n""".format(i, j, space(i), params['translate'][kk][1])
    for key in params:
        if key == "depr":
            for kk, (i, j) in enumerate(params[key]):
                output += u"""config[page]['obsolete'].append(({}, u"{}", u"{}", u"{}"))\n""".format(i, j, params['rdepr'][kk][1], params['errordepr'][kk][1])
    
        '''
        elif key == "param" or key == "translate":
            print ">>>", key
            for (i, j) in params[key]:
                print i, j
        elif key == "notifyuser":
            print ">>>", key
            for user in [lre.pats["user0"].find(x.strip(), 1)
                            for x in params["notifyuser"].split("\n")]:
                print user
        else:
            if isinstance(params[key], list):
                print ">>>", key, ":"
                for i in params[key]:
                    print i, params[key]
            else:
                print ">>>", key, params[key]
        '''
    
    if output: output += "\n"
    if page_config not in allpages:
        allpages[page_config] = wp.Page(page_config + '!')
        allpages[page_config].text = ""
    
    output = output1 + output + "###############################\n"
    #allpages[page_config].text += output
    #print output
    global allo
    allo += output

def main():
    pool = lthread.ThreadPool(30)
    gen = []
    page = wp.handlearg("page", args)
    if page is not None:
        gen = [wp.Page(page)]
    else:
        gen = site.allpages(prefix=conf.title, content=True, namespace=2)
    for page in gen:
        for req in lre.pats["entry"].finditer(page.get()):
            pool.add_task(process, req.group(1), page.title())
    pool.wait_completion()
    #print allo
    global allo
    allo =  '<source lang="python">\n' + allo + u'</source>{{คู่มือการใช้งาน}}'
    wp.Page(u'User:Nullzerobot/ปรับปรุงหน้าอัตโนมัติ/ปกติ').put(allo, u"ปรับปรุงหน้า")
    #for i in allpages:
    #    i.save(u"โรบอต: แปลงหน้า", async=True)

if __name__ == "__main__":
    args, site, conf = wp.pre(-2, lock=True)
    try:
        glob()
        wp.run(main)
    except:
        wp.posterror()
    else:
        wp.post()
