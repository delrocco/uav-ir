#!/usr/bin/python
# -*- coding: utf-8 -*-
#====================================================================
# @author: Joe Del Rocco
# @since: 10/25/2016
# @summary: A script to strips frames from videos.
#           Requires 'ffmpeg' to be installed an accessible on PATH.
#====================================================================
import argparse
import logging
import sys
import os
import myutil
import ffmpy
import subprocess


class FrameStrip(object):
    def __init__(self, cmd_args):
        self.args = cmd_args

    def __repr__(self):
        return '<{0!r} {1!r}>'.format(self.__class__.__name__, self.args)

    def run(self):
        logging.info("Processing: " + self.args.input)

        # probe input for information
        ff = ffmpy.FFprobe(inputs={self.args.input: "-v error -show_entries stream=width,height -of default=noprint_wrappers=1:nokey=1"})
        output = ff.run(stdout=subprocess.PIPE)
        size_actual = output[0].split('\n')

        # output folder
        framespath = os.path.join(os.path.dirname(self.args.input), os.path.splitext(os.path.basename(self.args.input))[0])
        if self.args.size:
            size_requested = self.args.size.split('x')
            if size_requested[0] == "-1":
                size_requested[0] = str(int(size_actual[0]) * int(size_requested[1]) / int(size_actual[1]))
            elif size_requested[1] == "-1":
                size_requested[1] = str(int(size_requested[0]) * int(size_actual[1]) / int(size_actual[0]))
            framespath += '_' + size_requested[0] + 'x' + size_requested[1]
        else:
            framespath += '_' + size_actual[0] + 'x' + size_actual[1]

        # create/clean folder for frames
        if not os.path.exists(framespath):
            os.makedirs(framespath)
        else:
            myutil.cleanFolder(framespath)

        # ffmpeg cmd line options
        ffmpegOptions = ''
        #if self.args.loglvl > 0:
        #    os.environ["FFREPORT"] = "file="+logpath+":level="+str(args.loglvl)
        ffmpegOptions += ' -loglevel '
        if self.args.loglvl == "CRITICAL":
            ffmpegOptions += 'fatal'
        else:
            ffmpegOptions += self.args.loglvl.lower()
        if self.args.loglvl != "DEBUG":
            ffmpegOptions += ' -hide_banner'
        if self.args.frate:
            ffmpegOptions += ' -r ' + str(self.args.frate)
        #if args.fcount:
        ffmpegOptions += ' -f image2'
        if self.args.size:
            ffmpegOptions += ' -vf scale=' + self.args.size.replace('x', ':')
        ffmpegOptions += ' "' + framespath + '/frame-%04d.'
        if self.args.output:
            ffmpegOptions += self.args.output
        else:
            ffmpegOptions += 'jpg'
        ffmpegOptions += '"'

        # run ffmpeg
        ff = ffmpy.FFmpeg(inputs={self.args.input: ffmpegOptions})
        logging.info("Executing: " + ff.cmd)
        ff.run()

        return 0

'''
@summary: Main module entry point. Parses command line args and starts program.
'''
def main():
    # parse command line args
    parser = argparse.ArgumentParser(description='A script that strips frames from videos.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_help = True
    parser.add_argument('input', help='input video file to process')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-l', '--loglvl', dest='loglvl', type=str, help='log level (critical, error, warning, info, debug)', default='INFO')
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help='silent mode')
    parser.add_argument('-r', '--frate', dest='frate', type=float, help='number of frames per second (0.1-1000)')
    #parser.add_argument('-n', '--fcount', dest='fcount', type=int, help='number of frames for whole video (1-1000000)')
    parser.add_argument('-o', '--output', dest='output', type=str, help='output format (jpg, png, tiff, etc.)')
    parser.add_argument('-s', '--size', dest='size', type=str, help='output size (-1x600, 1024x768, 1980x-1, etc.)')
    args = parser.parse_args()

    # setup logger
    args.loglvl = args.loglvl.upper()
    loglvlnum = getattr(logging, args.loglvl, None)
    if not isinstance(loglvlnum, int):
        raise ValueError('Invalid log level: %s' % args.loglvl)
    logfile = os.path.join(os.path.dirname(args.input), "log.txt")
    logging.basicConfig(filename=logfile, filemode="w+", level=loglvlnum, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.debug("SYSTEM\n" + sys.version + '\n')

    # must specify an input video file to process
    if not args.input:
        logging.critical("No input file specified.")
        sys.exit(2)

    # handle relative paths
    if not os.path.isabs(args.input):
        args.input = os.path.join(os.getcwd(), args.input)

    # must specify a valid input file
    if not os.path.exists(args.input):
        logging.critical("'" + args.input + "' is missing.")
        sys.exit(2)
    elif not os.path.isfile(args.input):
        logging.critical("'" + args.input + "' is not a file.")
        sys.exit(2)
    # elif os.path.isfile(args.input) and not args.input.endswith(".mp4"):
    #     log( "Error: File path must be to a single .zip or folder of .zip files." )
    #     shutdown(2)

    # sanitize inputs
    if args.size and args.size == "-1x-1":
        args.size = None
    if args.frate:
        args.frate = myutil.clamp(args.frate, 0.1, 1000)
    #if args.fcount:
    #    args.fcount = myutil.clamp(args.fcount, 1, 1000000)

    # do it!
    fs = FrameStrip(args)
    status = fs.run()
    sys.exit(status)

if __name__ == "__main__":
    main()