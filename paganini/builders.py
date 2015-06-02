
from mingus.containers import Bar, Track
import dsl

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

    def from_dsl(self, string):
        plan, bpm = dsl.parse_string(string)
        for arpeggio, duration in plan:
            self.fill_bars(arpeggio, duration[0], duration[1])
        return self.track, bpm


