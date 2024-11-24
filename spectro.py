import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#Serial port configuration
ser = serial.Serial('COM5', 115200)  # Replace with your Arduino's serial port

#Parameters
SAMPLE_RATE = 1000  # Match this with Arduino's sampling rate
BUFFER_SIZE = 64  # Matches the number of samples sent per loop
SPECTROGRAM_HISTORY = 100  # Number of FFT windows in the spectrogram display

#Adjust spectrogram data to have 33 columns (BUFFER_SIZE // 2 + 1)
spectrogram_data = np.zeros((SPECTROGRAM_HISTORY, BUFFER_SIZE // 2 + 1))

#Set up the plot
fig, ax = plt.subplots()
im = ax.imshow(spectrogram_data, aspect='auto', origin='lower', cmap='viridis', extent=[0, BUFFER_SIZE // 2 + 1, 0, SPECTROGRAM_HISTORY])
plt.colorbar(im, ax=ax)
ax.set_xlabel('Frequency Bin')
ax.set_ylabel('Time (Slices)')

def update_spectrogram(frame):
    # Collect BUFFER_SIZE samples from serial
    data = []
    while len(data) < BUFFER_SIZE:
        try:
            line = ser.readline().decode('utf-8').strip()  # Read line from serial
            value = int(line)
            data.append(value)
        except ValueError:
            pass  # Skip any malformed data

    # Compute FFT of the collected data
    fft_values = np.fft.rfft(data * np.hanning(BUFFER_SIZE))  # Apply windowing to reduce spectral leakage
    fft_magnitude = np.abs(fft_values)

    # Update spectrogram data
    global spectrogram_data
    spectrogram_data = np.roll(spectrogram_data, -1, axis=0)
    spectrogram_data[-1, :] = fft_magnitude  # Insert new FFT result at the bottom

    #Update the plot with new data
    im.set_data(spectrogram_data)
    ax.set_ylim(0, SPECTROGRAM_HISTORY)
    im.set_clim(0, np.max(spectrogram_data))  # Adjust color scale

ani = animation.FuncAnimation(fig, update_spectrogram, interval=50, save_count=SPECTROGRAM_HISTORY)
plt.show()