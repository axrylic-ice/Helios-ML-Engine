from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout

def build_lstm(input_shape):
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(50),
        Dropout(0.2),
        Dense(1, activation='sigmoid') # Probability output
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy')
    return model

def train_lstm(X_train_seq, y_train_seq):
    model = build_lstm((X_train_seq.shape[1], X_train_seq.shape[2]))
    model.fit(X_train_seq, y_train_seq, epochs=20, batch_size=16, verbose=1)
    model.save('ml/models/weights/lstm_helios.h5')
    return model