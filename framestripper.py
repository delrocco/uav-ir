#!/usr/bin/python
# -*- coding: utf-8 -*-
#====================================================================
# @author: Joe Del Rocco
# @since: 10/25/2016
# @summary: A script to strips frames from videos.
#====================================================================
import sys
import os
import argparse
import shutil
import ffmpy
# import subprocess
# import zipfile
# import xml.etree.ElementTree
# import uuid
# import shlex
# from threading import Timer


class GlobalInfo:
    def __init__(self):
        self.args = None
        self.startpath = sys.path[0]
        self.framespath = 'frames'
        self.logpath = "log.txt"
        self.loglvls = [-8, 8, 16, 24, 32, 40, 48, 56]

# globals
gSTUFF = GlobalInfo()

'''
@summary: Clamp a number to a range.
'''
def clamp(n, minval, maxval):
    return min(max(n, minval), maxval)

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
            log(ex.message)

# '''
# @summary: Helper function to try and extract student name from submission file, given Sidekick formatting.
# '''
# def getStudentNameFromSubmission(submission):
#     words = os.path.basename(submission).split('_')
#     if words and len(words) > 0:
#         return words[0]
#     else:
#         return ""
#
# '''
# @summary: Special kludge function to address a common student submission error.
#           Renames file to Submission.cs and zips it up.
# '''
# def fixSubmissionFile(filepath):
#     # zip it up, renamed
#     zipName = getStudentNameFromSubmission(filepath)
#     if len(zipName) <= 0: zipName = str(uuid.uuid4())
#     zipName += "_.zip"
#     zipName = os.path.join(os.path.dirname(filepath), zipName)
#     zipFile = zipfile.ZipFile(zipName, 'w', zipfile.ZIP_DEFLATED)
#     zipFile.write(filepath, "Submission.cs") # rename file in .zip archive
#     zipFile.close()
#     log( "Warning: Fixing '" + os.path.basename(filepath) + "' -> '" + os.path.basename(zipName) + "'")
#
# '''
# @summary: Special kludge function to address a common student submission error.
#           If submission is a single .cs file, renames it to Submission.cs and .zips it up.
#           If submission is a folder of submissions, any .cs files are fixed as described above.
# '''
# def fixSubmission(filepath):
#     # fix a single file
#     if os.path.isfile(filepath):
#         if gSTUFF.args.path.endswith(".cs"):
#             fixSubmissionFile(filepath)
#     # fix a whole directory of files
#     else:
#         for filename in os.listdir(filepath):
#             submission = os.path.join(filepath, filename)
#             if os.path.isfile(submission) and submission.endswith(".cs"):
#                 fixSubmissionFile(submission)

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
        log(ex.message)

# '''
# @summary: Helper function to extract an XML file's namespaces.
# '''
# def extractXMLNamespaces(filename):
#     namespaces = {}
#     for event, element in xml.etree.ElementTree.iterparse(filename, events=['start-ns']):
#         namespaces[element[0]] = element[1]
#     return namespaces
#
# '''
# @summary: Helper function to kill a process.
# '''
# def killProcess(process, timeout):
#   timeout["value"] = True
#   process.kill()
#
# '''
# @summary: Helper function to run a shell command with a support timeout.
# '''
# def runCMD(cmd, timeout_sec):
#   process = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#   timeout = {"value": False}
#   timer = Timer(timeout_sec, killProcess, [process, timeout])
#   timer.start()
#   stdout, stderr = process.communicate()
#   timer.cancel()
#   return process.returncode, stdout, stderr, timeout["value"]
#
# '''
# @summary: Build the specified solution with devenv.
# '''
# def build(solution):
#     global gSTUFF
#
#     if not os.path.exists(solution):
#         log( "Error: Could not find .sln '" + solution + "'" )
#         return
#
#     # execute 'devenv' to build the solution
#     cmd = [
#         gSTUFF.devenv,
#         solution,
#         "/Build"
#     ]
#     try:
#         output = subprocess.check_output(cmd)
#     except subprocess.CalledProcessError as ex:
#         output = ex.output
#
#     log( output )
#
# '''
# @summary: Run the specified executable, and display the output.
# '''
# def run(executable):
#     global gSTUFF
#     output = ""
#     timedout = False
#
#     if not os.path.exists(executable):
#         log( "Error: Could not find .exe '" + executable + "'" )
#         return
#
#     # execute the resulting lab .exe; forward any relevant command line arguments
#     #cmd = [ executable ]
#     cmd = "\"" + executable + "\""
#     if gSTUFF.args.llvl:
#         #cmd.append("-e")
#         #cmd.append(str(gSTUFF.args.llvl))
#         cmd += " -e " + str(gSTUFF.args.llvl)
#     if gSTUFF.args.runs:
#         #cmd.append("-r")
#         #cmd.append(str(gSTUFF.args.runs))
#         cmd += " -r " + str(gSTUFF.args.runs)
#     if gSTUFF.args.seed:
#         #cmd.append("-s")
#         #cmd.append(str(gSTUFF.args.seed))
#         cmd += " -s " + str(gSTUFF.args.seed)
#     try:
#         #output = subprocess.check_output(cmd, timeout=gSTUFF.args.timeout)
#         retcode, output, outerr, timedout = runCMD(cmd, gSTUFF.args.timeout)
#     except Exception as ex:
#         log( ex.message )
#
#     log(output)
#     if timedout:
#         log("Warning: Student submission timed-out after " + str(gSTUFF.args.timeout) + " seconds.")

'''
@summary: Given a .zip submission, do everything needed to autograde it.
'''
def process():
    global gSTUFF

    if gSTUFF.args.loglvl >= 32:
        log("Processing: " + gSTUFF.args.input)

    # create/clean folder for frames
    if not os.path.exists(gSTUFF.framespath):
        os.makedirs(gSTUFF.framespath)
    else:
        cleanFolder(gSTUFF.framespath)

    # ffmpeg options
    if gSTUFF.args.loglvl > 0:
        os.environ["FFREPORT"] = "file="+gSTUFF.logpath+":level="+str(gSTUFF.args.loglvl)
    ffmpegOptions = ' -loglevel ' + str(gSTUFF.args.loglvl)
    if gSTUFF.args.loglvl < 40:
        ffmpegOptions += ' -hide_banner'
    if gSTUFF.args.frate:
        ffmpegOptions += ' -r ' + str(gSTUFF.args.frate)
    #if gSTUFF.args.fcount:
    ffmpegOptions += ' -f image2'
    ffmpegOptions += ' "' + gSTUFF.framespath + '/frame-%04d.'
    if gSTUFF.args.ext:
        ffmpegOptions += gSTUFF.args.ext
    else:
        ffmpegOptions += 'jpg'
    ffmpegOptions += '"'

    # run ffmpeg
    ff = ffmpy.FFmpeg(inputs={gSTUFF.args.input: ffmpegOptions})
    # if gSTUFF.args.quiet:
    #     ff.run(stdout=os.devnull)
    # else:
    ff.run()

    # # copy over the appropriate lab files
    # copy(os.path.join(gSTUFF.dirLabs, "Lab" + str(gSTUFF.args.lab)), gSTUFF.dirGrade)
    #
    # # parse visual studio project file (XML) to find element with source files
    # projFilename = os.path.join(gSTUFF.dirGrade, "Lab" + str(gSTUFF.args.lab) + ".csproj")
    # # HACK - registering the default namespace before opening XML file, prevents writer from including namespaces per element
    # projNS = extractXMLNamespaces(projFilename)
    # for key, val in projNS.iteritems(): xml.etree.ElementTree.register_namespace(key, val)
    # projFile = xml.etree.ElementTree.parse(projFilename)
    # projRoot = projFile.getroot()
    # projSrcElement = None
    # for element in projRoot.findall('{'+projNS['']+'}ItemGroup'):
    #     for x in element.findall('{'+projNS['']+'}Compile'):
    #         projSrcElement = element
    #         break
    #
    # # copy over the submission file
    # copy(submission, gSTUFF.dirGrade)
    #
    # # unzip it
    # submissionUnzipped = os.path.join(gSTUFF.dirGrade, os.path.basename(submission) + ".unzipped")
    # with zipfile.ZipFile(submission) as zf:
    #     zf.extractall(submissionUnzipped)
    #
    # # copy over any submission .cs files
    # # (ignore the following: Program.cs, AssemblyInfo.cs, TemporaryGeneratedFile*.cs)
    # for dirpath, dnames, fnames in os.walk(submissionUnzipped):
    #     for f in fnames:
    #         if f.endswith(".cs"):
    #             if not f.startswith("Program") and not f.startswith("AssemblyInfo") and not f.startswith("TemporaryGeneratedFile"):
    #                 copy(os.path.join(dirpath, f), os.path.join(gSTUFF.dirGrade, f))
    #                 # add new Compile element into visual studio project file for any new src files found
    #                 if f != "Submission.cs": # already added to project
    #                     element = xml.etree.ElementTree.SubElement(projSrcElement, 'Compile')
    #                     element.attrib['Include'] = str(f)
    #
    # # write out the new visual studio XML project file
    # projFile.write(projFilename, encoding="utf-8", xml_declaration=True)
    #
    # # build the lab with visual studio
    # log("Building: " + os.path.join(gSTUFF.dirGrade, "Lab" + str(gSTUFF.args.lab) + ".sln"))
    # build(os.path.join(gSTUFF.dirGrade, "Lab" + str(gSTUFF.args.lab) + ".sln"))
    #
    # # run the lab
    # log("Running: " + os.path.join(gSTUFF.dirGrade, "bin", "Debug", "Lab" + str(gSTUFF.args.lab) + ".exe"))
    # run(os.path.join(gSTUFF.dirGrade, "bin", "Debug", "Lab" + str(gSTUFF.args.lab) + ".exe"))

    return

'''
@summary: A logging routine.
'''
def log(message=None, newline=True):
    global gSTUFF

    if not message:
        message = " "

    # stdout
    if not gSTUFF.args.quiet:
        if newline:
            print str(message)
        else:
            print str(message),

    # log
    if gSTUFF.args.loglvl > 0:
        logfile = open(gSTUFF.logpath, 'a')
        logfile.write(str(message))
        if newline: logfile.write('\n')
        logfile.close()

'''
@summary: This should be called instead of a direct exit to ensure proper cleanup,
'''
def shutdown(code):
    sys.exit(code)

'''
@summary: Main module entry point. Handles command line args and starts program.
'''
def main():
    global gSTUFF

    # handle command line args
    parser = argparse.ArgumentParser(description='A script that strips frames from videos.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_help = True
    parser.add_argument('input', help='input video file to process')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help='silent mode')
    parser.add_argument('-l', '--loglvl', dest='loglvl', type=int, help='ffmpeg log level', default=gSTUFF.loglvls[0])
    parser.add_argument('-c', '--clean', dest='clean', action='store_true', help='remove log and output files')
    parser.add_argument('-r', '--frate', dest='frate', type=float, help='number of frames per second (0.1-1000)')
    parser.add_argument('-n', '--fcount', dest='fcount', type=int, help='number of frames for whole video (1-1000000)')
    parser.add_argument('-x', '--ext', dest='ext', type=str, help='extension of output (jpg, png, tiff, etc.)')
    gSTUFF.args = parser.parse_args()

    # must specify an input video file to process
    if not gSTUFF.args.input:
        log("Error: No input video file specified.")
        shutdown(2)

    # handle relative paths
    if not os.path.isabs(gSTUFF.args.input):
        gSTUFF.args.input = os.path.join(os.getcwd(), gSTUFF.args.input)

    # must specify a valid input file
    if not os.path.exists(gSTUFF.args.input):
        log("Error: The filepath '" + gSTUFF.args.input + "' is invalid.")
        shutdown(2)
    # elif os.path.isfile(gSTUFF.args.input) and not gSTUFF.args.input.endswith(".mp4"):
    #     log( "Error: File path must be to a single .zip or folder of .zip files." )
    #     shutdown(2)

    # sanitize inputs
    if gSTUFF.args.loglvl:
        validloglvl = False
        for lvl in gSTUFF.loglvls:
            if gSTUFF.args.loglvl == lvl:
                validloglvl = True
                break
        if not validloglvl:
            log("Error: Invalid log level specified. Choices are: " + " ".join(str(i) for i in gSTUFF.loglvls))
            shutdown(2)
    if gSTUFF.args.frate:
        gSTUFF.args.frate = clamp(gSTUFF.args.frate, 0.1, 1000)
    if gSTUFF.args.fcount:
        gSTUFF.args.fcount = clamp(gSTUFF.args.fcount, 1, 1000000)

    # setup outputs
    gSTUFF.logpath = os.path.join(os.path.dirname(gSTUFF.args.input), gSTUFF.logpath)
    gSTUFF.framespath = os.path.join(os.path.dirname(gSTUFF.args.input), gSTUFF.framespath)
    # if gSTUFF.args.loglvl > 0:
    #     open(gSTUFF.logpath, 'w+').close()

    # debugging information
    if gSTUFF.args.loglvl >= 32:
        log("SYSTEM")
        log(sys.version)
        log()

    # handle clean
    if gSTUFF.args.clean:
        if os.path.exists(gSTUFF.logpath):
            os.unlink(gSTUFF.logpath)
        if os.path.exists(gSTUFF.framespath):
            cleanFolder(gSTUFF.framespath)
            os.removedirs(gSTUFF.framespath)
        shutdown(0)

    # process single submission
    if os.path.isfile(gSTUFF.args.input):
        process()

    # cleanup
    shutdown(0)


if __name__ == "__main__":
    main()