import pypianoroll
import numpy as np
import matplotlib.pyplot as plt
import IPython

def flatten(pianorolls):
    """Automatically joins multiple pianorolls into a single sequence."""

    rolls, steps, pitch  = pianorolls.shape
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
    fig, ax = plt.subplots(figsize=(14,4))
    return pypianoroll.plot_pianoroll(ax=ax, pianoroll=pianoroll);

def create_multitrack(basemultitrack, pianoroll):
    if len(pianoroll.shape) == 3:
      pianoroll = flatten(pianoroll)
    track = pypianoroll.StandardTrack(program=0, is_drum=False, pianoroll=pianoroll)
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
        X_start = i*x_qnotes *qnote
        X_end = ((i+1)*x_qnotes) *qnote
        y_start = X_end
        y_end = ((i+1)*x_qnotes + y_qnotes) *qnote
        X.append(pianoroll[X_start:X_end])
        y.append(pianoroll[y_start:y_end])
    return np.array(X), np.array(y)


def multi_sample_pianorolls(pianorolls, qnote=24, x_qnotes=4, y_qnotes=4):
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
