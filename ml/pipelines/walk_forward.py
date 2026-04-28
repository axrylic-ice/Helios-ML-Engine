# walk_forward.py

import numpy as np

class WalkForwardEngine:
    def __init__(self, train_size=500, test_size=100, step=100):
        self.train_size = train_size
        self.test_size = test_size
        self.step = step

    def split(self, data):
        n = len(data)

        start = 0

        while start + self.train_size + self.test_size < n:

            train_start = start
            train_end = start + self.train_size

            test_start = train_end
            test_end = train_end + self.test_size

            yield (
                train_start, train_end,
                test_start, test_end
            )

            start += self.step