#!/usr/bin/env python 

import argparse
import sys

from mingus.midi import midi_file_out
from builders import TrackBuilder 
import dsl

class Options:
    def __init__(self, input, output = None):
        self.input = input
        self.output = output

    def get_output_file(self):
        if self.output is None:
            pass
        return self.output

def to_midi(filename, track, bpm = 120):
    midi_file_out.write_Track(filename, track, bpm)
    print "Written", filename

def get_args():
    parser = argparse.ArgumentParser(prog='paganini',
            description='The arpeggiator for the whole family')
    parser.add_argument('input', metavar='INPUT', nargs=1, 
            help='the input file path')
    parser.add_argument('output', metavar='OUTPUT', nargs='?', 
            help='the optional output file path. Default is ./INPUT.wav')
    args = parser.parse_args()
    return Options(args.input[0], args.output)


def read_input_file(opts):
    try:
        f = open(opts.input)
        result = f.read()
        f.close()
        return result
    except Exception, e:
        print "Couldn't read file '%s' because:" % opts.input
        print e
        sys.exit(1)

def main():
    options = get_args()
    input = read_input_file(options)
    track, bpm = TrackBuilder().from_dsl(input)
    to_midi(options.get_output_file(), track, bpm)

if __name__ == '__main__':
    main()
