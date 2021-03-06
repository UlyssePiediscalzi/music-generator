import pypianoroll
import numpy as np
import matplotlib.pyplot as plt
import IPython
from music21 import converter, instrument, note, chord, stream

from music_generator.data import get_npz_data


def flatten(pianorolls):
    """Automatically joins multiple pianorolls into a single sequence."""

    rolls, steps, pitch = pianorolls.shape
    return pianorolls.reshape(rolls*steps, pitch)


def get_instrument(mtrack, name):
    return [track for track in mtrack.tracks if track.name == name and type(track) is pypianoroll.track.StandardTrack][0]


def plot_pianoroll(pianoroll):
    """Plots pianoroll pitches through time for given pianoroll.
    Automatically joins multiple pianorolls if an array of pianorolls is passed.

    Example
    -------

        plot_pianoroll(mtrack, track.pianoroll)

        plot_pianoroll(mtrack, flatten(pred[10:20]))
    """

    if len(pianoroll.shape) == 3:
        pianoroll = flatten(pianoroll)
    fig, ax = plt.subplots(figsize=(14, 4))
    return pypianoroll.plot_pianoroll(ax=ax, pianoroll=pianoroll)


def create_multitrack(basemultitrack, pianoroll):
    if len(pianoroll.shape) == 3:
        pianoroll = flatten(pianoroll)
    track = pypianoroll.StandardTrack(
        program=0, is_drum=False, pianoroll=pianoroll)
    tempo = basemultitrack.tempo[:pianoroll.shape[0]]
    return pypianoroll.Multitrack(tempo=tempo, tracks=[track])


def play_pianoroll(multitrack, pianoroll):
    """Returns an IPython player for given pianoroll.
    Automatically joins multiple pianorolls if an array of pianorolls is passed.

    Example
    -------

        play_pianoroll(mtrack, track.pianoroll)

        play_pianoroll(mtrack, flatten(pred[10:20]))
    """

    mt = create_multitrack(multitrack, pianoroll)
    return IPython.display.Audio(data=mt.to_pretty_midi().synthesize(), rate=44100)


def sample_multitrack(multitrack, track, x_qnotes=4, y_qnotes=2):
    pianoroll = track.pianoroll
    qnote = multitrack.resolution
    quarter_notes = int(pianoroll.shape[0]/qnote)
    X = []
    y = []
    for i in range(int(np.floor(quarter_notes/(x_qnotes+y_qnotes)))):
        X_start = i*x_qnotes * qnote
        X_end = ((i+1)*x_qnotes) * qnote
        y_start = X_end
        y_end = ((i+1)*x_qnotes + y_qnotes) * qnote
        X.append(pianoroll[X_start:X_end])
        y.append(pianoroll[y_start:y_end])
    return np.array(X), np.array(y)


def sample_roll(resolution, roll, x_qnotes=4, y_qnotes=2):
    pianoroll = roll
    qnote = resolution
    quarter_notes = int(pianoroll.shape[0]/qnote)
    X = []
    y = []
    for i in range(int(np.floor(quarter_notes/(x_qnotes+y_qnotes)))):
        X_start = i*x_qnotes * qnote
        X_end = ((i+1)*x_qnotes) * qnote
        y_start = X_end
        y_end = ((i+1)*x_qnotes + y_qnotes) * qnote
        X.append(pianoroll[X_start:X_end])
        y.append(pianoroll[y_start:y_end])
    return np.array(X), np.array(y)


def multi_sample_pianorolls(pianorolls, qnote=4, x_qnotes=4, y_qnotes=4):
    '''pianorolls = output of 'fetching_instrument_pianorolls' function in data.py.
    Returns an array concatenating all the samples of n songs.'''
    X = []
    y = []
    for pianoroll in pianorolls:
        quarter_notes = int(pianoroll.shape[0] / qnote)
        for i in range(int(np.floor(quarter_notes / (x_qnotes + y_qnotes)))):
            X_start = i * x_qnotes * qnote
            X_end = ((i + 1) * x_qnotes) * qnote
            y_start = X_end
            y_end = ((i + 1) * x_qnotes + y_qnotes) * qnote
            X.append(pianoroll[X_start:X_end])
            y.append(pianoroll[y_start:y_end])
    return np.array(X), np.array(y)


def multi_track_train_test(n_tracks, n_steps):
    ''' returns X_train, y_train, X_test, y_test and multitracks
    You can decide how many tracks you want to train your model with.
    As some tracks are binary or have not enough steps, you won't have the
    exact n_tracks number'''
    multitracks = get_npz_data(n_tracks)
    valid_track = []
    X_final = []
    y_final = []

    for multi in multitracks:
        for standard in multi:
            if standard.name in 'Piano' and standard.pianoroll.shape[
                    0] > n_steps * 2:
                valid_track.append(standard)
    for i in valid_track[:-1]:
        X, y = sample_multitrack(multitracks[2], i, x_qnotes=12, y_qnotes=12)
        X = X.reshape(X.shape[0] * X.shape[1], 128)[:n_steps]
        y = y.reshape(y.shape[0] * y.shape[1], 128)[:n_steps]
        X_final.append(X)
        y_final.append(y)
    X_test, y_test = sample_multitrack(multitracks[2],
                                       valid_track[-1],
                                       x_qnotes=12,
                                       y_qnotes=12)
    X_test = X_test.reshape(1, X_test.shape[0] * X_test.shape[1],
                            128)[:, :n_steps]
    y_test = y_test.reshape(y_test.shape[0] * y_test.shape[1], 128)[:n_steps]
    return np.array(X_final), np.array(y_final), np.array(X_test), np.array(
        y_test), multitracks


def parseNote(element):
    if isinstance(element, note.Note):
        return f"{element.pitch} for {element.duration.quarterLength}"
    elif isinstance(element, chord.Chord):
        c = '.'.join(f"{n}" for n in element.normalOrder)
        return f"{c} for {element.duration.quarterLength}"


def get_notes(midi):
    instruments = instrument.partitionByInstrument(midi)
    piano = [i for i in instruments if i.id == 'Piano'][0]
    notes = [parseNote(n) for n in piano.recurse() if type(n)
             is note.Note or type(n) is chord.Chord]
    return notes

def render_midi(notes):
    output_notes = []
    offset = 0
    for pattern in notes:
        pattern, duration = pattern.split(' for ')
        duration = float(duration)
        # if pattern is a chord
        if ('.' in pattern) or pattern.isdigit():
            notes_in_chord = pattern.split('.') # split the chord into number that each represent a note
            
            notes = []
            for current_note in notes_in_chord:
                new_note = note.Note(int(current_note)) # transform the number into a note object
                new_note.storedInstrument = instrument.Piano() # set the instrument as piano
                notes.append(new_note) # append the note to the list
            new_chord = chord.Chord(notes) # transform the indivual notes into chord object
            new_chord.offset = offset # set the offset
            new_note.quarterLength = duration
            output_notes.append(new_chord) # append the chord object to the output_notes
        
        # if pattern is a note
        else:
            new_note = note.Note(pattern) # transform the number into a note object
            new_note.offset = offset # set the offset
            new_note.quarterLength = duration
            new_note.storedInstrument = instrument.Piano() # set the instrument as piano
            output_notes.append(new_note) # append the note object to the output_notes

        # increase offset each iteration so that notes do not stack
        offset += duration
    return stream.Stream(output_notes)
