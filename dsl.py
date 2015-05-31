#!/usr/bin/env python 

from arpeggiators import UpAndDownArpeggiator, RandomArpeggiator
from builders import NotesBuilder
import sys

example = """
updown: Cmaj7 -octave, 32 x 1
updown: Fmaj7 -octave, 32 x 1
updown: Cmaj7 -octave, 32 x 1
updown: Gdom7 -octave +octave, 32 x 1
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
    for s in string.split('\n'):
        if s.startswith("updown:"):
            arpeggio = UpAndDownArpeggiator()
            params = s[8:]
            comma = params.find(",")
            if comma != -1:
                notes = params[:comma]
                duration = params[comma + 1:]
                arpeggio.set_notes(parse_notes(notes))
                result.append((arpeggio, parse_duration(duration)))
    return result

