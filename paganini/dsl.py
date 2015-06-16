#!/usr/bin/env python 

from mingus.core import chords
from mingus.containers import Note
from arpeggiators import UpAndDownArpeggiator, RandomArpeggiator
import sys


class NotesBuilder(object):

    def get_notes_from_chord(self, chord = 'Cmaj7', octaves_above = 0, octaves_below = 0):
        notes = []
        for n in chords.from_shorthand(chord):
            note = Note(n)
            notes.append(note)
            for i in xrange(octaves_above):
                note = Note(n)
                note.octave += i + 1
                notes.append(note)
            for i in xrange(octaves_below):
                note = Note(n)
                note.octave -= i + 1
                notes.append(note)
        return sorted(notes)

def parse_notes(notes, quit_on_error = True):
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
            if quit_on_error:
                sys.exit(1)
    return NotesBuilder().get_notes_from_chord(chord, octaves_above, octaves_below)

def parse_duration(duration, quit_on_error = True):
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

def parse_string(string, quit_on_error = True):
    result = []
    bpm = 120
    loop = 1
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
        elif s.startswith("loop:"):
            loop_str = s[6:]
            if not loop_str.isdigit():
                print "Error: loop is not an integer:", loop_str
                sys.exit(1)
            loop = int(loop_str)
            continue
        else:
            print "Warning: unknown command:", s
            if quit_on_error:
                sys.exit(1)
            continue
        params = s[8:]
        comma = params.find(",")
        if comma != -1:
            notes = params[:comma]
            duration = params[comma + 1:]
            arpeggio.set_notes(parse_notes(notes, quit_on_error))
            result.append((arpeggio, parse_duration(duration, quit_on_error)))
    return result, bpm, loop

