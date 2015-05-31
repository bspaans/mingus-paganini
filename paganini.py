#!/usr/bin/env python 

from mingus.containers import NoteContainer, Bar, Note
from mingus.core import chords
from mingus.midi import midi_file_out

def get_notes(chord = 'Cmaj7'):
    notes = []
    for n in chords.from_shorthand(chord):
        note = Note(n)
        notes.append(note)
    return notes

def up_and_down_generator(notes):
    index = 0
    up = True
    while True:
        yield notes[index]
        if up:
            index += 1
            if index == len(notes):
                index -= 2
                up = False
        else:
            index -= 1
            if index == -1:
                index = 1
                up = True
        
def fill_bar(generator, duration = 16):
    b = Bar()
    while not b.is_full():
        b.place_notes(generator.next(), duration)
    return b

def to_midi(filename, bar, bpm = 120):
    bar.key = Note('C-4')
    midi_file_out.write_Bar(filename, bar, bpm)

notes = get_notes()
gen = up_and_down_generator(notes)
bar = fill_bar(gen)
to_midi("arpeggio_test.mid", bar, 120)
