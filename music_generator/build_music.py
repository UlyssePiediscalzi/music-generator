import numpy as np
from music21 import note, chord, stream

def chords_n_notes(Snippet):
  Melody = []
  offset = 0  # Incremental
  for i in Snippet:
      #If it is chord
      if ("." in i or i.isdigit()):
          chord_notes = i.split(".")  # Seperating the notes in chord
          notes = []
          for j in chord_notes:
              inst_note = int(j)
              note_snip = note.Note(inst_note)
              notes.append(note_snip)
              chord_snip = chord.Chord(notes)
              chord_snip.offset = offset
              Melody.append(chord_snip)
      # pattern is a note
      else:
          note_snip = note.Note(i)
          note_snip.offset = offset
          Melody.append(note_snip)
      # increase offset each iteration so that notes do not stack
      offset += 0.5
  Melody_midi = stream.Stream(Melody)
  return Melody_midi
