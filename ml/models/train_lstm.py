import numpy as np
import tensorflow as tf
from tensorflow.keras import layers


class FXLSTMModel:
    def __init__(self, time_steps=30, feature_dim=11):
        self.time_steps = time_steps
        self.feature_dim = feature_dim
        self.model = self.build()
    def build_input(self, data):
        return np.array(data).reshape(1, self.time_steps, self.feature_dim)
    def build(self):
        model = tf.keras.Sequential([
            tf.keras.Input(shape=(self.time_steps, self.feature_dim)),
            layers.LSTM(64, return_sequences=True),
            layers.Dropout(0.2),
            layers.LSTM(32),
            layers.Dense(16, activation="relu"),
            layers.Dense(1)
        ])

        model.compile(optimizer="adam", loss="mse")
        return model

    def prepare_data(self, X, y):
        Xs, ys = [], []

        for i in range(len(X) - self.time_steps):
            Xs.append(X[i:i+self.time_steps])
            ys.append(y[i+self.time_steps])

        return np.array(Xs), np.array(ys)

    def create_sequences(self, data):
        import numpy as np

        X = []

        for i in range(len(data) - self.time_steps):
            X.append(data[i:i + self.time_steps])

        return np.array(X)
    def train(self, data, y):

        # 1. CREATE SEQUENCES (CRITICAL FIX)
        X = self.create_sequences(data)

        # 2. ALIGN TARGET
        y = y[self.time_steps:]   # shift to match sequence windows

        # 3. FINAL ALIGNMENT SAFETY
        min_len = min(len(X), len(y))
        X = X[:min_len]
        y = y[:min_len]

        # 4. TRAIN
        self.model.fit(
            X, y,
            epochs=15,
            batch_size=32,
            validation_split=0.2,
            verbose=1
        )

    def predict(self, sequence):
        import numpy as np

        seq = np.array(sequence)

        # ✅ FIX: ensure 3D input
        if len(seq.shape) == 2:
            seq = seq.reshape(1, self.time_steps, self.feature_dim)

        pred = self.model.predict(seq, verbose=0)

        return {
            "volatility": float(pred[0][0])
        }

    def predict_all(self, X):
        return self.model.predict(X, verbose=0).flatten()

    def predict_single(self, seq):
        seq = seq.reshape(1, self.time_steps, self.feature_dim)
        return float(self.model.predict(seq, verbose=0)[0][0])

    def save(self):
        self.model.save("ml/models/weights/lstm.keras")

    def load(self):
        self.model = tf.keras.models.load_model("ml/models/weights/lstm.keras")