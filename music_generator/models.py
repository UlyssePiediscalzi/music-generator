import numpy as np
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.callbacks import EarlyStopping

from music_generator.midi import play_pianoroll, sample_multitrack, plot_pianoroll, create_multitrack, get_instrument, sample_roll

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

    def createRoll(self, input_roll):
        """Create song given a input pianoroll of same size"""
        assert input_roll.shape[1] == self.X.shape[1], f"Input roll needs to be split in steps of {self.X.shape[1]}"
        song = self.model.predict(input_roll).astype(np.uint8)
        return np.concatenate(song)
    
    def continueRoll(self, intervals=5, intro_roll=None):
        """Create song given an introduction. Song will have intervals time the introduction of length."""
        net_in = self.X[:3]
        if intro_roll is not None:
            assert intro_roll.shape[1] == self.X.shape[1], f"Intro roll needs to be split in steps of {self.X.shape[1]}"
            net_in = intro_roll
        roll = [net_in]
        for i in range(intervals-1):
            piece = self.model.predict(net_in).astype(np.uint8)
            net_in = piece
            roll.append(piece)
        roll = np.concatenate(roll)
        return roll

    def play(self, roll):
        return play_pianoroll(self.mtrack, roll)

    def plot(self, roll):
        plot_pianoroll(roll)


class DivideAndComposeBidirectional(DivideAndCompose):
    ''''
    Same as DivideAndCompose class but it builds a model using bidirectional
    layers and GRU
    '''
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

class MultiSongModel(DivideAndCompose):
    def __init__(self, pianorolls, rate=24):
        self.pianorolls = pianorolls
    
    def init_model(self, quarter_notes_window=8, model_layers=None):
        X = []
        y = []
        for roll in self.pianorolls:
            Xt, yt = sample_roll(24, roll, quarter_notes_window, quarter_notes_window)
            X.append(Xt)
            y.append(yt)
        X = np.concatenate(X)
        y = np.concatenate(y)
        self.X = X
        self.y = y
        input_shape = X[0].shape
        output_shape = y[0].shape[1]
        model = models.Sequential()
        if model_layers is None:
            model.add(layers.SimpleRNN(128, return_sequences=True, activation='tanh', input_shape=input_shape))
            model.add(layers.SimpleRNN(128 * 8, return_sequences=True, activation='tanh'))
            model.add(layers.Dense(output_shape * 8, activation='relu'))
            model.add(layers.Dense(output_shape * 4, activation='relu'))
            model.add(layers.Dense(output_shape, activation='relu'))
        else:
            for layer in model_layers:
                model.add(layer)
        model.compile(loss='mse', optimizer=RMSprop(learning_rate=0.005))
        model.summary()
        self.model = model
        return model

