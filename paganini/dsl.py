#!/usr/bin/env python 

from arpeggiators import UpAndDownArpeggiator, RandomArpeggiator
from builders import NotesBuilder
import sys

example = """
bpm: 150
updown: Cmaj7 -octave, 64 x 1
updown: Fmaj7 -octave, 64 x 1
updown: Cmaj7 -octave, 64 x 1
updown: Gdom7 -octave +octave, 64 x 1
"""

def parse_notes(notes):
    parts = notes.split()
    chord = parts[0]
    octaves_below = 0
    octaves_above = 0
    for p in parts[1:]:
        if p == '-octave':
            octaves_below += 1
        elif p == '+octave':
            octaves_above += 1
        else:
            print "Warning: unknown option", p
    return NotesBuilder().get_notes_from_chord(chord, octaves_above, octaves_below)

def parse_duration(duration):
    times = duration.find('x')
    if times == -1:
        print "Error: missing number of bars"
        sys.exit(1)
    note_duration = duration[:times].strip()
    bars = duration[times + 1:].strip()
    if not note_duration.isdigit():
        print "Error: note duration is not an integer:", note_duration
        sys.exit(1)
    if not bars.isdigit():
        print "Error: number of bars is not an integer:", bars
        sys.exit(1)
    return (int(note_duration), int(bars))

def parse_string(string):
    result = []
    bpm = 120
    for s in string.split('\n'):
        if s.strip() == '' or s.startswith('#') or s.startswith('//'):
            continue
        elif s.startswith("updown:"):
            arpeggio = UpAndDownArpeggiator()
        elif s.startswith("random:"):
            arpeggio = RandomArpeggiator()
        elif s.startswith("bpm:"):
            bpm_str = s[5:]
            if not bpm_str.isdigit():
                print "Error: bpm is not an integer:", bpm_str
                sys.exit(1)
            bpm = int(bpm_str)
            continue
        else:
            print "Warning: unknown command:", s
            continue
        params = s[8:]
        comma = params.find(",")
        if comma != -1:
            notes = params[:comma]
            duration = params[comma + 1:]
            arpeggio.set_notes(parse_notes(notes))
            result.append((arpeggio, parse_duration(duration)))
    return result, bpm

