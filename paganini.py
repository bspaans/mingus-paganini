#!/usr/bin/env python 

from mingus.containers import NoteContainer, Bar, Note, Track
from mingus.core import chords
from mingus.midi import midi_file_out
from arpeggiators import UpAndDownArpeggiator, RandomArpeggiator

class TrackBuilder(object):
    def __init__(self):
        self.track = Track()

    def fill_bars(self, arpeggio, note_duration = 16, bars = 1):
        generator = arpeggio.get_generator()
        while bars > 0:
            b = Bar()
            b.key = Note('C-4')
            while not b.is_full():
                b.place_notes(generator.next(), note_duration)
            self.track.add_bar(b)
            bars -= 1
        return self.track

def get_notes(chord = 'Cmaj7'):
    notes = []
    for n in chords.from_shorthand(chord):
        note = Note(n)
        notes.append(note)
    return notes

def to_midi(filename, track, bpm = 120):
    midi_file_out.write_Track(filename, track, bpm)

arpeggio = UpAndDownArpeggiator()
arpeggio.set_notes(get_notes('Cmaj7'))

arpeggio2 = UpAndDownArpeggiator()
arpeggio2.set_notes(get_notes('Fmaj7'))

arpeggio3 = UpAndDownArpeggiator()
arpeggio3.set_notes(get_notes('Gdom7'))

builder = TrackBuilder()
builder.fill_bars(arpeggio, note_duration = 16, bars = 1)
builder.fill_bars(arpeggio2, note_duration = 16, bars = 1)
builder.fill_bars(arpeggio, note_duration = 16, bars = 1)
builder.fill_bars(arpeggio3, note_duration = 16, bars = 1)
to_midi("arpeggio_test.mid", builder.track, 120)
