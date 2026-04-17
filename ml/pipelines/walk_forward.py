def walk_forward_split(df, window=365):
    for i in range(window, len(df)):
        train = df.iloc[:i]
        test = df.iloc[i:i+1]
        yield train, test