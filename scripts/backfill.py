import numpy as np

def create_sequences(X, y, window=7):

    X_seq, y_seq = [], []

    for i in range(len(X) - window - 7):

        X_seq.append(X.iloc[i:i+window].values)

        # predict future devaluation
        y_seq.append(y.iloc[i + window + 7])

    return np.array(X_seq), np.array(y_seq)