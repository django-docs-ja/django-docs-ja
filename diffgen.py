#!/usr/bin/env python

import sys
import commands
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--debug", dest="debug", default=False, action="store_true")
parser.add_option("-l", "--log", dest="log", default="5")
parser.add_option("--svk", dest="svk_basepath", default="//jk/django/docs/")
parser.add_option("-r", "--rev", dest="rev", default="")
parser.add_option("-p", "--path", dest="path", default="")
parser.add_option("-w", "--workspace", dest="workspace", default="works/")
(_options,  argv) = parser.parse_args()
options = _options.__dict__
options["-"] = ""

log_cmd = "svk log %(log_flag)s %(rev)s %(svk_basepath)s%(path)s"
diff_cmd = "svk diff %(diff_flag)s %(rev)s %(svk_basepath)s%(path)s \
 >%(workspace)s%(path)s%(-)s%(rev)s.diff"

if options.get("path"):
    options["-"] = "-"

rev = options.get("rev")
if ":" in rev:
    diff_flag = "-r"
elif rev:
    diff_flag = "-c"
else:
    diff_flag = None
options["diff_flag"] = diff_flag

if options["diff_flag"]:
    log_flag = "-r"
    cmd = "%s; %s" % (log_cmd, diff_cmd)
else:
    options["rev"] = "%s" % options["log"]
    log_flag = "-l"
    cmd = log_cmd
options["log_flag"] = log_flag

if _options.debug:
    print "DEBUG:", cmd % options
print commands.getoutput(cmd % options)

