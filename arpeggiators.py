from mingus.containers import Note
import random

class Arpeggiator(object):
    def set_notes(self, notes):
        self.notes = notes
    def get_generator(self):
        yield Note('C-4')

class UpAndDownArpeggiator(Arpeggiator):

    def next_index_and_direction(self, index, up):
        index = index + 1 if up else index - 1
        if index == len(self.notes):
            index -= 2
            up = False
        if index < 0:
            index = 1
            up = True
        return index, up

    def get_generator(self):
        index = 0
        up = True
        while True:
            yield self.notes[index]
            index, up = self.next_index_and_direction(index, up)

class RandomArpeggiator(Arpeggiator):
    def get_generator(self):
        while True:
            yield random.choice(self.notes)
