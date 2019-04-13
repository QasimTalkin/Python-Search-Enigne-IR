import matplotlib.pyplot as plt
plt.style.use('classic')

import numpy as np
import pandas as pd
import json

df = pd.read_json("reuters_theaurus.json")

# Create some data
rng = np.random.RandomState(0)
x = np.linspace(0, 10, 500)
y = np.cumsum(rng.randn(500, 6), 0)

# Plot the data with Matplotlib defaults
plt.plot(x, y)
plt.legend('ABCDEF', ncol=2, loc='upper left');

plt.show