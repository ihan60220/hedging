# plotting option prices when delta held constant

import numpy as np
import matplotlib.pyplot as plt

delta = float(input("Delta: "))
shares = []
data_points = 0

while True:
    value = float(input("Share prices: "))
    if value == -1:
        break
    else:
        shares.append(value)
        data_points += 1

shares = np.array(shares)
options = shares / delta    # shares = options * delta
time = np.linspace(0, data_points - 1, num=data_points)
plt.plot(time, shares, label="shares")
plt.plot(time, options, label="options")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.show()
