import math 
import pandas as pd
import numpy as np

try:
    from . import profileGenerator as pg
except ImportError:
    # Handle relative import when running as a script
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    import profileGenerator as pg

class CoolingNewton:
    def __init__(self, T0, k):
        self.T0 = T0
        self.k = k

    def simulate(self, t, func_T_env, func_k ,dt, t_end):
        T = self.T0
        t = 0
        wyniki = []

        while t < t_end:

            T_env = func_T_env(t)
            k_val = func_k(t)

            if T_env > T:
                T = T_env - (T_env - T) * math.exp(-k_val * dt)
            else:
                
                T = T_env + (T - T_env) * math.exp(-k_val * dt)

            wyniki.append({"time": t, "temperature": T})
            t += dt

        return pd.DataFrame(wyniki)
