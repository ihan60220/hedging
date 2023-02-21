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
options = []
for index, share in enumerate(shares):
    if index == 0:
        options.append(shares[0])
    else:
        options.append((shares[index] - shares[index - 1]) * delta + options[index - 1])

time = np.linspace(0, data_points - 1, num=data_points)
plt.plot(time, shares, label="Shares")
plt.plot(time, options, label="Options")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.show()
