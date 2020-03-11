#!/usr/bin/python

'''
Format stagged python files using black.
Call black executable on stagged python file, then add the changes via git add before commiting.
Must be used in a python virtual environnement with black installed.
'''

import os
import sys
import subprocess
import shlex
import re


def call(cmd, cwd=None):
    args = shlex.split(cmd)
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    out, err = p.communicate()
    return out.decode("utf-8"), err.decode("utf-8"), p.returncode


pyModified = re.compile("^(?:M|A).(?P<filename>.*\.py)")
out, _, _ = call("git status --porcelain")

sys.stdout.write("Start pre-commit hook black formatting ...\n")
sys.stdout.write("VIRTUAL_ENV=%s\n" % os.environ["VIRTUAL_ENV"])

for line in out.splitlines():

    match = pyModified.match(line.strip())
    if match:

        sys.stdout.write("File found : %s\n" % match.group("filename"))

        sys.stdout.write("\t> format with black ... ")
        call("black.exe %s" % match.group("filename"), cwd=os.environ["VIRTUAL_ENV"])
        sys.stdout.write("done.\n")

        sys.stdout.write('\t> stage the changes with "git add" ... ')
        call("git add %s" % match.group("filename"))
        sys.stdout.write("done.\n")

        sys.stdout.write("Formatting %s done.\n" % match.group("filename"))

sys.stdout.write("Black formatting done. Hoora !\n")
