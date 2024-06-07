import numpy as np
import matplotlib.pyplot as plt

data  = np.load('sample_groundroll.npy')

print(f"Data shape: {data.shape}")

# Visualize the data
plt.imshow(data, aspect='auto', cmap='viridis')
plt.colorbar(label='Amplitude')
plt.title('Synthetic Ground Roll Data')
plt.xlabel('Trace Index')
plt.ylabel('Time Sample')
plt.show()