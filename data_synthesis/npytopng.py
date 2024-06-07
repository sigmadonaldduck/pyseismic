import os
import numpy as np
import matplotlib.pyplot as plt

# Path to the folder containing .npy files
npy_folder = '.\syn_data'
# Path to the folder where .png files will be saved
png_folder = '.\syn_data\png'

# Create the png_folder if it does not exist
os.makedirs(png_folder, exist_ok=True)


# Get a list of all .npy files in the npy_folder
npy_files = [f for f in os.listdir(npy_folder) if f.endswith('.npy')]

# Loop through each .npy file
for npy_file in npy_files:
    # Load the .npy file
    npy_path = os.path.join(npy_folder, npy_file)
    data = np.load(npy_path)

    # Create a plot from the data
    plt.imshow(data, aspect='auto', cmap='viridis')  # You can change the colormap if needed

    # Save the plot as a .png file
    png_file = npy_file.replace('.npy', '.png')
    png_path = os.path.join(png_folder, png_file)
    plt.savefig(png_path)
    plt.close()  # Close the plot to free memory

    print(f"Saved {png_path}")

print("Conversion completed.")
