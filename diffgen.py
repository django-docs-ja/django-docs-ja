#!/usr/bin/env python

from optparse import OptionParser
import commands
import re
import sys
import cPickle as pickle

parser = OptionParser()
parser.add_option("--debug", dest="debug", default=False, action="store_true")
parser.add_option("--svk", dest="svk_basepath", default="//jk/django/docs/",
    help="default `%default`.")
parser.add_option("--sync", dest="sync", default=False, action="store_true",
    help="update revision map.")
parser.add_option("-l", "--log", dest="log", default="5",
    help="default `%default`.")
parser.add_option("-p", "--path", dest="path", default="")
parser.add_option("-r", "--rev", dest="rev", default="")
parser.add_option("-w", "--workspace", dest="workspace", default="works/",
    help="default `%default`.")
(_options,  argv) = parser.parse_args()
options = _options.__dict__
options["-"] = ""

log_cmd = "svk log %(log_flag)s %(rev)s %(svk_basepath)s%(path)s"
diffoutput_path = "%(workspace)s%(path)s%(-)s%(rev)s.diff"
diff_cmd = "svk diff %(diff_flag)s %(rev)s %(svk_basepath)s%(path)s >" + diffoutput_path
sync_cmd = "svk sync %(svk_basepath)s"
loghead_cmd = "svk log -q %(svk_basepath)s"


def dump_revs():
    revs = dict()
    rev = re.compile(ur"r\d+")
    for line in commands.getoutput(loghead_cmd % options).splitlines():
        if line.startswith("-"):
            continue
        try:
            (local, orig) = rev.findall(line)[:2]
        except ValueError:
            continue
        revs[int(orig[1:])] = int(local[1:])
    pickle.dump(revs, open("%(workspace)s_revs" % options, "w"))

def conv_rev(rev, revs=dict()):
    if not revs:
        try:
            revs.update(pickle.load(open("%(workspace)s_revs" % options)))
        except IOError, e:
            print "%s: Does not saved revision map. rerun with `--sync` option." % e
    result = revs.get(int(rev))
    if result is None:
        revs_keys = sorted(revs.keys())
        result = revs[filter(lambda x: x > int(rev), revs_keys)[0] or revs_keys[-1]]
    return str(result)


if options.get("path"):
    options["-"] = "-"

rev = options.get("rev")
if ":" in rev:
    diff_flag = "-r"
    options["rev"] = ":".join(map(conv_rev, rev.split(":")))
elif rev:
    diff_flag = "-c"
    options["rev"] = conv_rev(rev)
else:
    diff_flag = None
options["diff_flag"] = diff_flag


log_flag = "-r"
if options.get("sync"):
    cmd = sync_cmd
elif options["diff_flag"]:
    cmd = "%s; %s" % (log_cmd, diff_cmd)
    print "Writing to", diffoutput_path % options
else:
    options["rev"] = "%s" % options["log"]
    log_flag = "-l"
    cmd = log_cmd
options["log_flag"] = log_flag

if _options.debug:
    print "DEBUG:", cmd % options
print commands.getoutput(cmd % options)
if options.get("sync"):
    dump_revs()
