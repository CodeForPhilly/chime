"""Temporary module for example visualization

In production, data should be provided outside the penn_chime.dash sub module
"""
import numpy as np
import pandas as pd

DATA = np.random.normal(size=100).reshape(20, 5)
COLS = ["A", "B", "C", "D", "E"]
DF = pd.DataFrame(DATA, columns=COLS, index=range(20))
