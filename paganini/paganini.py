#!/usr/bin/env python 

import argparse

from mingus.midi import midi_file_out
from builders import TrackBuilder 
import dsl

def to_midi(filename, track, bpm = 120):
    midi_file_out.write_Track(filename, track, bpm)

def main():
    track, bpm = TrackBuilder().from_dsl(dsl.example)
    to_midi("arpeggio_test.mid", track, bpm)
    print("Written arpeggio_test.mid")

if __name__ == '__main__':
    main()
