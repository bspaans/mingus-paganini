#!/usr/bin/env python 

from mingus.containers import NoteContainer, Bar, Note, Track
from mingus.midi import midi_file_out
from arpeggiators import UpAndDownArpeggiator, RandomArpeggiator
from builders import TrackBuilder, NotesBuilder
import dsl

def to_midi(filename, track, bpm = 120):
    midi_file_out.write_Track(filename, track, bpm)

plan, bpm = dsl.parse_string(dsl.example)
builder = TrackBuilder()
for arpeggio, duration in plan:
    builder.fill_bars(arpeggio, duration[0], duration[1])

to_midi("arpeggio_test.mid", builder.track, bpm)
