#!/usr/bin/python
# -*- coding: utf-8 -*-
#====================================================================
# @author: Joe Del Rocco
# @since: 10/25/2016
# @summary: A module with general useful functionality.
#====================================================================
import os
import shutil
import subprocess
import shlex
import logging
from threading import Timer


'''
@summary: Clamp a number to a range.
'''
def clamp(n, minval, maxval):
    return min(max(n, minval), maxval)

'''
@summary: Normalize a number between 0-1.
'''
def normalize(n, minval, maxval):
    return float(n-minval)/float(maxval-minval)

'''
@summary: Helper function delete all files and folders given a folder.
'''
def cleanFolder(dirpath):
    for filename in os.listdir(dirpath):
        filepath = os.path.join(dirpath, filename)
        try:
            if os.path.isfile(filepath):
                os.unlink(filepath)
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath)
        except Exception as ex:
            logging.error(ex.message)

'''
@summary: Helper function to copy a single file or filetree from one location to another.
'''
def copy(src, dest):
    try:
        if os.path.isfile(src):
            shutil.copy(src, dest)
        else:
            for filename in os.listdir(src):
                srcfile = os.path.join(src, filename)
                destfile = os.path.join(dest, filename)
                if os.path.isfile(srcfile):
                    shutil.copy(srcfile, destfile)
                else:
                    shutil.copytree(srcfile, destfile)
    except Exception as ex:
        logging.error(ex.message)

'''
@summary: Helper function to kill a process.
'''
def killProcess(process, timeout):
    timeout["value"] = True
    process.kill()

'''
@summary: Helper function to run a shell command with timeout support.
'''
def runCMD(cmd, timeout_sec):
    process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    timeout = {"value": False}
    timer = Timer(timeout_sec, killProcess, [process, timeout])
    timer.start()
    stdout, stderr = process.communicate()
    timer.cancel()
    return process.returncode, stdout, stderr, timeout["value"]
