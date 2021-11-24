import pypianoroll
import numpy as np
import IPython

def play_pianoroll(multitrack, pianoroll):
    track = pypianoroll.StandardTrack(program=0, is_drum=False, pianoroll=pianoroll)
    tempo = np.ones(pianoroll.shape[0]) * multitrack.tempo[0]
    mt = pypianoroll.Multitrack(tempo=tempo, tracks=[track])
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
