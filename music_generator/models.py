import numpy as np
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.callbacks import EarlyStopping

from music_generator.midi import play_pianoroll, sample_multitrack, plot_pianoroll, create_multitrack, get_instrument

class DivideAndCompose:
    def __init__(self, mtrack, instrument='Piano'):
        self.mtrack = mtrack
        self.track = get_instrument(mtrack, instrument)
        plot_pianoroll(self.track.pianoroll)

    def init_model(self, quarter_notes_window=6):
        X, y = sample_multitrack(self.mtrack, self.track, quarter_notes_window, quarter_notes_window)
        self.X = X
        self.y = y
        input_shape = X[0].shape
        output_shape = y[0].shape[1]
        model = models.Sequential()
        model.add(layers.SimpleRNN(128 * 4, return_sequences=True, activation='tanh', input_shape=input_shape))
        model.add(layers.SimpleRNN(128 * 4, return_sequences=True, activation='tanh'))
        model.add(layers.Dense(output_shape*4, activation='relu'))
        model.add(layers.Dense(output_shape*2, activation='relu'))
        model.add(layers.Dense(output_shape, activation='relu'))
        model.compile(loss='mse', optimizer=RMSprop(learning_rate=0.005))
        model.summary()
        self.model = model
        return model

    def fit(self, epochs=300, batch_size=16, patience=10, **kwargs):
        assert self.model, "Model is not initialized"
        callback = EarlyStopping(monitor='loss', patience=patience)
        history = self.model.fit(self.X, self.y, validation_split=0.2, epochs=epochs, batch_size=batch_size, use_multiprocessing=True, callbacks=[callback], **kwargs)
        return history

    def createSong(self, quarter_notes=5):
        l = int(self.X.shape[0] / quarter_notes)
        song = self.model.predict(self.X[::l]).astype(np.uint8)
        return create_multitrack(self.mtrack, song)

    def play(self, song):
        return play_pianoroll(self.mtrack, song.tracks[0].pianoroll)

    def plot(self, song):
        plot_pianoroll(song.tracks[0].pianoroll)

class DivideAndComposeBidirectional(DivideAndCompose):
    def init_model(self, quarter_notes_window=12):
        X, y = sample_multitrack(self.mtrack, self.track, quarter_notes_window, quarter_notes_window)
        self.X = X
        self.y = y
        input_shape = X[0].shape
        model = models.Sequential()
        model.add(layers.Bidirectional(layers.GRU(512, return_sequences=True, activation='tanh'),input_shape=input_shape))
        model.add(layers.Bidirectional(layers.GRU(512, return_sequences=True, activation='tanh')))
        model.add(layers.Dense(256, activation='relu'))
        model.add(layers.Dense(128, activation='relu'))
        model.compile(loss='mse', optimizer=RMSprop(learning_rate=0.005))
        model.summary()
        self.model = model
        return model
