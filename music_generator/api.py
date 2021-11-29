import pickle
import random
import numpy as np
from typing import Iterable
from music21 import note, chord, stream
from tensorflow.keras.models import load_model

loaded_models = {}

def get_model(name: str):
    # Cache loaded model in memory
    if name in loaded_models:
        return loaded_models[name]
    model = load_model(f'./models/{name}.h5')
    loaded_models[name] = model
    return model


def convert_stream(notes: Iterable[str]):
    melody = []
    offset = 0  # Incremental
    for i in notes:
        # If it is chord
        if ("." in i or i.isdigit()):
            chord_notes = i.split(".")  # Seperating the notes in chord
            notes = []
            for j in chord_notes:
                inst_note = int(j)
                note_snip = note.Note(inst_note)
                notes.append(note_snip)
                chord_snip = chord.Chord(notes)
                chord_snip.offset = offset
                melody.append(chord_snip)
        # pattern is a note
        else:
            note_snip = note.Note(i)
            note_snip.offset = offset
            melody.append(note_snip)
        # increase offset each iteration so that notes do not stack
        offset += 0.5
    return stream.Stream(melody)


def generate_melody(model_name: str, number_of_notes: int):
    model = get_model(model_name)
    network_input, note_to_int = pickle.load(
        f'./models/{model_name}.pickle')
    pitchnames = note_to_int.keys()
    n_vocab = len(pitchnames)
    sequence_length = network_input.shape[1]
    seed = network_input[np.random.randint(0, len(network_input)-1)]
    music = ""
    Notes_Generated = []
    int_to_note = dict((number, note)
                       for number, note in enumerate(pitchnames))
    for i in range(number_of_notes):
        seed = seed.reshape(1, sequence_length, 1)
        prediction = model.predict(seed, verbose=0)[0]
        prediction = np.log(prediction)  # diversity
        exp_preds = np.exp(prediction) / 1
        prediction = exp_preds / np.sum(exp_preds)
        index = np.argmax(prediction)
        index_N = index / float(n_vocab)
        Notes_Generated.append(index)
        music = [int_to_note[char] for char in Notes_Generated]
        seed = np.insert(seed[0], len(seed[0]), index_N)
        seed = seed[1:]
    midi = convert_stream(music)
    return music, midi
