#!/usr/bin/env python

import sys
import commands

rev = int(sys.argv[1])
cmd = "svk log -r %(rev)d //jk/django/docs; svk diff -c %(rev)d //jk/django/docs >%(rev)d.diff"

print commands.getoutput(cmd % vars())

