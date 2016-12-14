#!/usr/bin/python
# -*- coding: utf-8 -*-
#====================================================================
# @author: Joe Del Rocco
# @since: 12/07/2016
# @summary: A helper program for .pgm files
#====================================================================
import argparse
import logging
import sys
import os
import myutil
import numpy
from PIL import Image


class PGMHelper(object):
    def __init__(self, cmd_args):
        self.args = cmd_args

    def __repr__(self):
        return '<{0!r} {1!r}>'.format(self.__class__.__name__, self.args)

    def bad(self):
        # handle a single file
        if os.path.isfile(self.args.input):
            if self.__isBadData(self.args.input):
                print self.args.input

        # handle a folder
        else:
            for filename in os.listdir(self.args.input):
                if filename.endswith(".pgm"):
                    filepath = os.path.join(self.args.input, filename)
                    if self.__isBadData(filepath):
                        print filepath

    def range(self):
        actualRange = [65536, 1]

        # handle a single file
        if os.path.isfile(self.args.input):
            actualRange = self.__readActualRange(self.args.input)

        # handle a folder
        else:
            for filename in os.listdir(self.args.input):
                if filename.endswith(".pgm"):
                    filepath = os.path.join(self.args.input, filename)
                    range = self.__readActualRange(filepath)
                    if range[0] < actualRange[0]:
                        actualRange[0] = range[0]
                    if range[1] > actualRange[1]:
                        actualRange[1] = range[1]

        print str(actualRange[0]) + "-" + str(actualRange[1])

    def scale(self):
        # handle a single file
        if os.path.isfile(self.args.input):
            self.__scaleFile(self.args.input, self.args.output)

        # handle a folder
        else:
            for filename in os.listdir(self.args.input):
                if filename.endswith(".pgm"):
                    srcpath = os.path.join(self.args.input, filename)
                    destpath = os.path.join(self.args.output, filename)
                    self.__scaleFile(srcpath, destpath)

    def convert(self):
        # handle a single file
        if os.path.isfile(self.args.input):
            self.__convertFile(self.args.input, self.args.output)

        # handle a folder
        else:
            for filename in os.listdir(self.args.input):
                if filename.endswith(".pgm"):
                    srcpath = os.path.join(self.args.input, filename)
                    destpath = os.path.join(self.args.output, filename)
                    self.__convertFile(srcpath, destpath)


        data = numpy.random.randint(0, 255, (10, 10)).astype(numpy.uint8)
        im = Image.fromarray(data)
        im.save('test.tif')

    def __isBadData(self, input):
        logging.debug("Testing: " + input)

        with open(input, "r") as file:
            # read magic number
            file.readline()
            # read dimensions
            file.readline()
            # read gray value max range
            line = file.readline()
            fileMaxVal = int(line)
            # read each row
            for line in file:
                values = line.split()
                if len(values) > 0:
                    # convert string to ints
                    values = [int(i) for i in values]
                    if len(values) > 0:
                        minval = min(values)
                        maxval = max(values)
                        if minval < 1 or maxval > fileMaxVal:
                            return True

        return False

    def __readActualRange(self, input):
        logging.debug("Reading: " + input)

        currRange = [65536, 1]

        with open(input, "r") as file:
            # read magic number
            file.readline()
            # read dimensions
            file.readline()
            # read gray value max range
            line = file.readline()
            fileMaxVal = int(line)
            # read each row
            for line in file:
                values = line.split()
                if len(values) > 0:
                    # convert string to ints
                    # also IGNORE values greater than file max gray value - these values are considered bad data!
                    values = [int(i) for i in values if int(i) <= fileMaxVal and int(i) > 0]
                    if len(values) > 0:
                        minval = min(values)
                        maxval = max(values)
                        if minval < currRange[0]:
                            currRange[0] = minval
                        if maxval > currRange[1]:
                            currRange[1] = maxval

        return currRange

    def __scaleFile(self, src, dest):
        logging.debug("Scaling: " + src + " to " + dest)

        # create all directories needed for output file
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))

        with open(src, "r") as srcfile:
            with open(dest, "w+") as destfile:
                # magic number
                line = srcfile.readline()
                destfile.write(line)
                # dimensions
                line = srcfile.readline()
                destfile.write(line)
                # gray value max range
                line = srcfile.readline()
                srcFileMaxValue = int(line)
                range = int(self.args.scale[1]) - int(self.args.scale[0])
                destfile.write(str(range) + "\n")
                # each row
                for line in srcfile:
                    values = line.split()
                    if len(values) > 0:
                        # convert strings to ints
                        values = [int(i) for i in values]
                        # correct values outside bounds of file max gray value - they are considered bad data!
                        values = [myutil.clamp(i, 0, srcFileMaxValue) for i in values]
                        for number in values:
                            scaled = number - self.args.scale[0]
                            destfile.write(str(scaled) + " ")
                    destfile.write("\n")

    def __convertFile(self, src, dest):
        logging.debug("Converting: " + src + " to " + dest)

        # create all directories needed for output file
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))

        dimensions = []
        pixeldata = []
        rangemax = 1

        # open and read the src file
        with open(src, "r") as srcfile:
            # magic number
            srcfile.readline()
            # dimensions
            line = srcfile.readline()
            dimensions = line.split()
            dimensions = [int(x) for x in dimensions]
            pixeldata = numpy.zeros((dimensions[1], dimensions[0], 3), dtype=numpy.uint8)
            # gray value max range
            rangemax = int(srcfile.readline())
            # each row
            for line in srcfile:
                values = line.split()
                if len(values) > 0:
                    # convert strings to numbers and normalize
                    values = [int(i) for i in values]
                    values = [myutil.normalize(i, 0, 1) for i in values]
                    #print values
                    # for i in range(0, 4): #number in values:
                    #     #scaled = (number * range) / srcFileMaxValue
                    #     #destfile.write(str(scaled) + " ")
                    #     print values[i],
                    # print '\n'

        # save out new image from pixel data
        # data[256, 256] = [255, 0, 0]
        #image = Image.fromarray(pixeldata, 'RGB')
        #image.save(dest)

'''
@summary: A safe program shutdown before exit.
'''
def shutdown(status):
    logging.shutdown()
    sys.exit(status)

'''
@summary: Main module entry point. Parses command line args and starts program.
'''
def main():
    # parse command line args
    parser = argparse.ArgumentParser(description='A helper program for .pgm files.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_help = True
    parser.add_argument('input', help='input file or folder to process')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-l', '--loglvl', dest='loglvl', type=str, help='log level (critical, error, warning, info, debug)', default='INFO')
    parser.add_argument('-q', '--quiet', dest='quiet', action='store_true', help='silent mode')
    parser.add_argument('-b', '--bad', dest='bad', action='store_true', help='find files with bad data')
    parser.add_argument('-r', '--range', dest='range', action='store_true', help='find actual min-max range of values')
    parser.add_argument('-s', '--scale', dest='scale', type=str, help='use min-max range (1-65536)')
    parser.add_argument('-f', '--format', dest='format', type=str, help='jpg, tiff, png, etc.')
    parser.add_argument('-c', '--color', dest='color', type=str, help='grayscale, ironbow, etc.', default="grayscale")
    parser.add_argument('-o', '--output', dest='output', type=str, help='output file or folder')
    args = parser.parse_args()

    # setup logger
    args.loglvl = args.loglvl.upper()
    loglvlnum = getattr(logging, args.loglvl, None)
    if not isinstance(loglvlnum, int):
        raise ValueError('Invalid log level: %s' % args.loglvl)
    logging.basicConfig(stream=sys.stdout, level=loglvlnum, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.debug("SYSTEM\n" + sys.version + '\n')

    # must specify an input file or folder to process
    if not args.input:
        logging.critical("No input file or folder specified.")
        shutdown(2)

    # handle relative paths
    if not os.path.isabs(args.input):
        args.input = os.path.join(os.getcwd(), args.input)

    # must specify a valid input file
    if not os.path.exists(args.input):
        logging.critical("'" + args.input + "' is missing.")
        shutdown(2)
    elif (args.scale or args.format) and not args.output:
        logging.critical("Argument -o required when using -s or -f.")
        shutdown(2)
    elif args.scale:
        range = args.scale.split("-")
        if len(range) != 2:
            logging.critical("Invalid scale range specified.")
            shutdown(2)
    # elif args.output:
    #     if not os.path.exists(args.output):
    #         logging.critical("Cannot file file " + args.output)
    #         shutdown(2)
    #     elif os.path.isfile(args.input) and not os.path.isfile(args.output):
    #         logging.critical("Input and Output args must both be files or directories.")
    #         shutdown(2)
    #     elif os.path.isdir(args.input) and not os.path.isdir(args.output):
    #         logging.critical("Input and Output args must both be files or directories.")
    #         shutdown(2)
    # elif args.convert:
    #     args.convert = args.convert.upper()
    #     if args.convert != "P2" and args.convert != "P5":
    #         logging.critical("Unrecognized convert argument '" + args.convert + "'.")
    #         shutdown(2)

    # sanitize inputs
    if args.scale:
        args.scale = args.scale.split("-")
        args.scale[0] = myutil.clamp(int(args.scale[0]), 1, 65536)
        args.scale[1] = myutil.clamp(int(args.scale[1]), 1, 65536)

    # do it!
    pgm = PGMHelper(args)
    if args.bad:
        pgm.bad()
    elif args.range:
        pgm.range()
    elif args.scale:
        pgm.scale()
    elif args.format:
        pgm.convert()

    logging.shutdown()
    shutdown(0)

if __name__ == "__main__":
    main()