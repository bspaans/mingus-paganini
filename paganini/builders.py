
from mingus.containers import NoteContainer, Bar, Note, Track
from mingus.core import chords

class TrackBuilder(object):
    def __init__(self):
        self.track = Track()

    def fill_bars(self, arpeggio, note_duration = 16, bars = 1):
        generator = arpeggio.get_generator()
        while bars > 0:
            b = Bar()
            b.key = 'C'
            while not b.is_full():
                b.place_notes(generator.next(), note_duration)
            self.track.add_bar(b)
            bars -= 1
        return self.track

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
